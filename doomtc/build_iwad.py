from pathlib import Path
import re, struct, sys, zipfile

ROOT = Path(__file__).resolve().parent
MAP_WAD = ROOT / "sam-and-the-mopoke-map.wad"
OUT = ROOT / "build" / "sam-and-the-mopoke.wad"
MUSIC_NAMES = [f"MUSIC{i:02d}" for i in range(1, 11)]

if len(sys.argv) != 2:
    raise SystemExit("usage: build_iwad.py /path/to/freedoom2.wad")
BASE = Path(sys.argv[1])
if not BASE.is_file():
    raise SystemExit(f"missing free Doom II base IWAD: {BASE}")

MAP_LUMPS = {
    "THINGS","LINEDEFS","SIDEDEFS","VERTEXES","SEGS","SSECTORS","NODES",
    "SECTORS","REJECT","BLOCKMAP","BEHAVIOR","SCRIPTS","DIALOGUE",
    "TEXTMAP","ENDMAP","ZNODES"
}
OVERRIDES = {
    "IWADINFO","ZSCRIPT","MAPINFO","LANGUAGE","MENUDEF","SBARINFO","SNDINFO",
    "TITLEPIC","INTERPIC","STBAR","SAMMPK","SAMLIC","SAMMUS"
}
OVERRIDES.update(MUSIC_NAMES)

SOUND_LUMPS = {
    "punch.wav":"SSPUNCH",
    "scratch.wav":"SSSCRAT",
    "door.wav":"SSDOOR",
    "doorbell.wav":"SSDBELL",
    "pickup.wav":"SSPICKUP",
    "secret.wav":"SSSECRET",
    "goat1.wav":"SSGOAT1",
    "goat2.wav":"SSGOAT2",
    "zombie1.wav":"SSZOMB1",
    "zombie2.wav":"SSZOMB2",
    "survivor.wav":"SSSURV",
    "loot.wav":"SSLOOT",
    "step1.wav":"SSSTEP1",
    "step2.wav":"SSSTEP2",
    "rain.wav":"SSRAIN",
    "wind.wav":"SSWIND",
    "forest.wav":"SSFOREST",
    "station.wav":"SSSTATN",
    "mallhum.wav":"SSMALL",
    "whisper1.wav":"SSWHSP1",
    "whisper2.wav":"SSWHSP2",
    "mopokecry.wav":"SSMPOKE",
    "stafffire.wav":"SSSTAFF",
    "cursefire.wav":"SSCURSE",
    "gauntlet.wav":"SSGAUNT",
    "jandal.wav":"SSJANDAL",
    "hitflesh.wav":"SSHFLESH",
    "key.wav":"SSKEY",
    "samfar.wav":"SSSAMFAR",
    "heartbeat.wav":"SSHEART",
}

def read_wad(path):
    b = Path(path).read_bytes()
    if len(b) < 12:
        raise ValueError(f"{path}: too small for WAD")
    ident = b[:4]
    if ident not in (b"IWAD", b"PWAD"):
        raise ValueError(f"{path}: invalid WAD header {ident!r}")
    count, directory = struct.unpack_from("<II", b, 4)
    if directory + count * 16 > len(b):
        raise ValueError(f"{path}: corrupt directory")
    lumps = []
    for i in range(count):
        pos, size, rawname = struct.unpack_from("<II8s", b, directory + i * 16)
        if pos + size > len(b):
            raise ValueError(f"{path}: corrupt lump {i}")
        name = rawname.rstrip(b"\0").decode("ascii", "replace").upper()
        lumps.append((name, b[pos:pos+size]))
    return ident, lumps

def write_wad(path, lumps, ident=b"IWAD"):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = bytearray(ident + struct.pack("<II", len(lumps), 0))
    directory = []
    for name, body in lumps:
        name = name.upper()
        if len(name.encode("ascii")) > 8:
            raise ValueError(f"WAD lump name too long: {name}")
        pos = len(data)
        data += body
        directory.append((pos, len(body), name.encode("ascii").ljust(8, b"\0")))
    dirpos = len(data)
    for entry in directory:
        data += struct.pack("<II8s", *entry)
    data[8:12] = struct.pack("<I", dirpos)
    path.write_bytes(data)

def strip_base_maps_and_overrides(lumps):
    out = []
    skipping_map = False
    for name, body in lumps:
        if re.fullmatch(r"(?:MAP\d\d|E\dM\d)", name):
            skipping_map = True
            continue
        if skipping_map:
            if name in MAP_LUMPS:
                continue
            skipping_map = False
        if name in OVERRIDES:
            continue
        out.append((name, body))
    return out

def add_namespace(lumps, start, end, folder):
    files = sorted((ROOT / folder).glob("*.png"))
    if not files:
        raise ValueError(f"no generated assets in {folder}/")
    names = []
    lumps.append((start, b""))
    for p in files:
        name = p.stem.upper()
        if len(name) > 8:
            raise ValueError(f"{folder}/{p.name}: lump name exceeds 8 chars")
        if name in names:
            raise ValueError(f"duplicate {folder} lump: {name}")
        names.append(name)
        lumps.append((name, p.read_bytes()))
    lumps.append((end, b""))

base_ident, base_lumps = read_wad(BASE)
if base_ident != b"IWAD":
    raise ValueError("Freedoom Phase 2 base must itself be an IWAD")

_, map_lumps = read_wad(MAP_WAD)
try:
    map_start = next(i for i,(n,_) in enumerate(map_lumps) if n == "MAP01")
except StopIteration:
    raise ValueError("custom map WAD has no MAP01")
map_lumps = map_lumps[map_start:]

lumps = strip_base_maps_and_overrides(base_lumps)

iwadinfo = b'''IWad
{
  Name = "Sam and the Mopoke"
  Autoname = "samandthemopoke"
  Game = "Doom"
  Config = "Doom"
  IWADName = "sam-and-the-mopoke.wad"
  Mapinfo = "mapinfo/doom2.txt"
  MustContain = "SAMMPK", "MAP01"
  BannerColors = "18 18 1c", "d8 b0 58"
}
'''

zscript_parts = ['version "4.10"\n']
for rel in [
    "zscript/weapons.zs",
    "zscript/keys.zs",
    "zscript/clues.zs",
    "zscript/world.zs",
    "zscript/actors.zs",
    "zscript/story.zs",
    "zscript/player.zs",
]:
    zscript_parts.append(f"\n// --- {rel} ---\n")
    zscript_parts.append((ROOT / rel).read_text(encoding="utf-8"))
zscript = "".join(zscript_parts).encode("utf-8")

lumps += [
    ("SAMMPK", b"Sam and the Mopoke standalone IWAD"),
    ("SAMLIC", b"Built on Freedoom Phase 2 free game data. Freedoom is distributed under its project license; see repository attribution."),
    ("IWADINFO", iwadinfo),
    ("ZSCRIPT", zscript),
    ("MAPINFO", (ROOT/"MAPINFO").read_bytes()),
    ("LANGUAGE", (ROOT/"LANGUAGE").read_bytes()),
    ("MENUDEF", (ROOT/"MENUDEF").read_bytes()),
    ("SBARINFO", (ROOT/"SBARINFO").read_bytes()),
    ("SNDINFO", (ROOT/"SNDINFO").read_bytes()),
]

# Custom graphics in the global namespace.
for p in sorted((ROOT/"graphics").glob("*.png")):
    name = p.stem.upper()
    if len(name) > 8:
        raise ValueError(f"graphics/{p.name}: lump name exceeds 8 chars")
    lumps.append((name, p.read_bytes()))

# GZDoom namespaces for custom PNG resources.
add_namespace(lumps, "S_START", "S_END", "sprites")
add_namespace(lumps, "F_START", "F_END", "flats")
add_namespace(lumps, "TX_START", "TX_END", "textures")

# Original custom sounds, addressed from SNDINFO by WAD lump name.
for filename, lumpname in SOUND_LUMPS.items():
    p = ROOT/"sounds"/filename
    if not p.is_file():
        raise ValueError(f"missing generated sound: {filename}")
    lumps.append((lumpname, p.read_bytes()))

bundle = ROOT/"music"/"music_bundle.zip"
if not bundle.is_file():
    raise ValueError("missing numeric MIDI bundle")
with zipfile.ZipFile(bundle, "r") as z:
    members = set(z.namelist())
    for music_name in MUSIC_NAMES:
        member = f"{music_name}.mid"
        if member not in members:
            raise ValueError(f"music bundle missing {member}")
        body = z.read(member)
        if not body.startswith(b"MThd"):
            raise ValueError(f"{member} is not a MIDI file")
        lumps.append((music_name, body))

music = ROOT/"music"/"sam-mopoke.mid"
if not music.is_file():
    raise ValueError("missing generated fallback music")
lumps.append(("SAMMUS", music.read_bytes()))

# Append the complete eight-map custom campaign.
lumps.extend(map_lumps)

write_wad(OUT, lumps, ident=b"IWAD")

# Self-check the shipped file, not just the source inputs.
ident, verify = read_wad(OUT)
names = [n for n,_ in verify]
required = {
    "SAMMPK","IWADINFO","ZSCRIPT","MAPINFO","MAP01","THINGS","LINEDEFS",
    "SIDEDEFS","VERTEXES","SECTORS","S_START","S_END","TX_START","TX_END",
    "F_START","F_END","SAMMUS","GTFGA0","CRFGA0","PSFGA0","WGAUA0","SAMRA0",
    "MPKEA1","GOATA1","SHAMA1","CGHLA1","ZDADA0","HOUSE","KITCHEN","PINKBATH","CORRUG","PLAYGRND","FOREST","GRAVE","TOMB","STATION","MALL","LIBRARY",
    "HCARPET","KTILE","PBATH","GRASS","DIRT","GRAVEFL","TOMBFL","STNFLR","MALLFLR","LIBFLR",
    "HCEIL","TOMBCE","STNCEIL","MALLCEIL","LIBCEIL","GTGTA0","CRGTA0","PSGTA0",
    "ROTPA1","CROWA1","HUSKA1","BRUTA1","SHADA1",
    "DBELA0","SSDBELL",
    "H42WALL","H42PANL","H42KTCH","H42BATH","H42SIDN","H42BRIK",
    "H42SHED","H42FENC","H42GATE","H42WIND","H42BLND","H42DOOR",
    "H42WDR","H42FRNT","H42SOFA","H42APPL","H42CURB","H42PLAY",
    "H42CARP","H42WOOD","H42VNYL","H42TILF","H42CONC","H42ASPH",
    "H42GRAS","H42PAVE","H42CEIL","H42ROOF"
}
required.update(MUSIC_NAMES)
missing = sorted(required - set(names))
if ident != b"IWAD" or missing:
    raise ValueError(f"IWAD validation failed: header={ident!r} missing={missing}")
maps = [n for n in names if re.fullmatch(r"MAP\d\d", n)]
expected_maps=[f"MAP{i:02d}" for i in range(1,9)]
if maps != expected_maps:
    raise ValueError(f"standalone IWAD should ship the eight-map campaign, got {maps}")
print(f"Built standalone IWAD: {OUT} ({OUT.stat().st_size} bytes, {len(verify)} lumps)")
