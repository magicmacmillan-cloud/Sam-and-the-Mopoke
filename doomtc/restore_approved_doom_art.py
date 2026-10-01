from pathlib import Path
import re, struct, sys, hashlib

PNG_SIG=b"\x89PNG\r\n\x1a\n"

# Restore ONLY the approved gameplay art from the known-good Samsung/DOOM build.
# MAP01 geometry, H42 house/street textures, new clues and v16 scenery stay untouched.
WEAPON_PREFIXES=("ZHND","DMST","AMUL","VIRS","DOLL","BLOD","FEEB","DACR","SCOT","GAUN","FEAT","SAUS","TOES","JAND")
MONSTER_PREFIXES=("MPKE","GOAT","ROTP","CROW","SHAM","CGHL","HUSK","BRUT","SHAD")
KEY_PREFIXES=("GTFG","CRFG","PSFG","GTGT","CRGT","PSGT")
WORLD_PLAYER_PREFIXES=("ZDAD",)
PICKUP_PREFIXES=("WSTA","WAMU","WVIR","WDOL","WBLO","WFEE","WDAC","WSCO","WGAU","WFEA","WSAU","WTOE","WJAN")

EXACT_GRAPHICS={"STBAR"}
EXCLUDED_PREFIXES=("H42","STLP","TREE","CARW","CARD","BNCH","SWNG","SLID","CLMB","WBIN","SNOT","LNOT","FNOT","COLA","BPAK","DBEL")

def parse(path):
    b=Path(path).read_bytes()
    ident=b[:4]
    if ident not in (b"IWAD",b"PWAD"):
        raise ValueError(f"{path}: not a WAD")
    count,diroff=struct.unpack_from("<II",b,4)
    entries=[]
    for i in range(count):
        pos,size,raw=struct.unpack_from("<II8s",b,diroff+i*16)
        name=raw.rstrip(b"\0").decode("ascii")
        body=b[pos:pos+size]
        entries.append([name,body])
    return ident,entries

def write(path,ident,entries):
    data=bytearray(); directory=[]; pos=12
    for name,body in entries:
        directory.append((pos,len(body),name))
        data.extend(body); pos+=len(body)
    diroff=12+len(data)
    out=bytearray(ident)+struct.pack("<II",len(entries),diroff)+data
    for pos,size,name in directory:
        out+=struct.pack("<II8s",pos,size,name.encode("ascii")[:8].ljust(8,b"\0"))
    Path(path).write_bytes(out)

def protected(name,body):
    if not body.startswith(PNG_SIG):
        return False
    if any(name.startswith(p) for p in EXCLUDED_PREFIXES):
        return False
    if name in EXACT_GRAPHICS or name.startswith("DAD"):
        return True
    if any(name.startswith(p) for p in WEAPON_PREFIXES):
        return True
    if any(name.startswith(p) for p in MONSTER_PREFIXES):
        return True
    if any(name.startswith(p) for p in WORLD_PLAYER_PREFIXES):
        return True
    if any(name.startswith(p) for p in PICKUP_PREFIXES):
        return True
    if any(name.startswith(p) for p in KEY_PREFIXES):
        return True
    # Preserve approved Sam character animation, but not unrelated SAM-prefixed data.
    if name.startswith("SAM") and len(name)>=5:
        return True
    return False

def png_wh(body):
    if not body.startswith(PNG_SIG): return None
    return struct.unpack(">II",body[16:24])

src,dst=sys.argv[1:3]
sid,se=parse(src)
did,de=parse(dst)

approved={}
for n,b in se:
    if protected(n,b):
        approved[n]=b

replaced=[]
for e in de:
    n,b=e
    if protected(n,b) and n in approved:
        e[1]=approved[n]
        replaced.append(n)

# The specific regression that caused the "green oval" complaint: all approved
# first-person frames must be large 320x200 canvases, not regenerated 128x128 art.
weapon_names=[]
for p in WEAPON_PREFIXES:
    for fr in "ABCDEFGH":
        weapon_names.append(f"{p}{fr}0")
missing=[n for n in weapon_names if n not in approved]
if missing:
    raise RuntimeError(f"approved baseline missing weapon frames: {missing[:12]} ({len(missing)} total)")
bad_dims=[(n,png_wh(approved[n])) for n in weapon_names if png_wh(approved[n])!=(320,200)]
if bad_dims:
    raise RuntimeError(f"approved baseline is not the detailed 320x200 art: {bad_dims[:8]}")

if len(set(replaced).intersection(weapon_names)) != 112:
    raise RuntimeError(f"target did not replace all 112 approved weapon/hand frames: {len(set(replaced).intersection(weapon_names))}")

write(dst,did,de)

# Re-read and verify every protected first-person frame is byte-identical to baseline.
_,check=parse(dst)
out={n:b for n,b in check}
mismatch=[n for n in weapon_names if out.get(n)!=approved[n]]
if mismatch:
    raise RuntimeError(f"restored art mismatch: {mismatch[:8]}")

print(f"Restored {len(set(replaced))} approved Doom art lumps from known-good build")
print("Approved first-person art: 14 families x 8 frames = 112, all 320x200 and byte-identical")
print("Protected examples:")
for n in ("ZHNDA0","DMSTA0","GAUNA0","STBAR","SAMRA0","MPKEA1"):
    if n in out:
        print(n, png_wh(out[n]), hashlib.sha256(out[n]).hexdigest()[:16])
