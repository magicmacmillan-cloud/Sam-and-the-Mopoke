from pathlib import Path
import struct, zlib

# Final stability pass for first-person sprite anchoring.
# The earlier builds mixed Doom sprite origins from several generators, which
# made the hands/weapons jump around the screen despite the artwork itself being good.

WEAPON_PREFIXES=("ZHND","DMST","AMUL","VIRS","DOLL","BLOD","FEEB","DACR","SCOT","GAUN","FEAT","SAUS","TOES","JAND")

def _set_grab(path, offx=0, offy=32):
    path=Path(path)
    if not path.exists():
        return
    b=path.read_bytes()
    if not b.startswith(b"\x89PNG\r\n\x1a\n"):
        return
    pos=8
    chunks=[]
    had=False
    while pos+12 <= len(b):
        n=struct.unpack(">I",b[pos:pos+4])[0]
        typ=b[pos+4:pos+8]
        data=b[pos+8:pos+8+n]
        pos += 12+n
        if typ==b"grAb":
            data=struct.pack(">ii",int(offx),int(offy))
            had=True
        chunks.append((typ,data))
        if typ==b"IEND":
            break
    if not had:
        out=[]
        for typ,data in chunks:
            out.append((typ,data))
            if typ==b"IHDR":
                out.append((b"grAb",struct.pack(">ii",int(offx),int(offy))))
        chunks=out
    out=bytearray(b"\x89PNG\r\n\x1a\n")
    for typ,data in chunks:
        out += struct.pack(">I",len(data))+typ+data+struct.pack(">I",zlib.crc32(typ+data)&0xffffffff)
    path.write_bytes(out)

def apply_visual_stability(root: Path):
    sprites=Path(root)/"sprites"

    # Keep every first-person frame on the same Doom HUD origin.
    for prefix in WEAPON_PREFIXES:
        for fr in "ABCDEFGH":
            # Polished weapon art is a centred 128x128 canvas, so the native
            # anchor is its horizontal midpoint (64), not its left edge (0).
            # The approved bottom-of-screen vertical anchor is 112.
            _set_grab(sprites/f"{prefix}{fr}0.png",64,112)

    # The world actors use full 8-direction sprite sets. Never leave a rotation-0
    # fallback beside them or GZDoom can select visually incompatible frames.
    for prefix in ("MPKE","GOAT","ROTP","CROW","SHAM","CGHL","HUSK","BRUT","SHAD"):
        for fr in "ABCDEFGHIJKLMNOP":
            p=sprites/f"{prefix}{fr}0.png"
            if p.exists():
                p.unlink()

    # POSS is a stock Doom/Freedoom sprite namespace. Remove any old generated
    # custom POSS frames so the Rot Possum cannot collide with the base IWAD.
    for p in sprites.glob("POSS*.png"):
        p.unlink()

    print("Visual stability pass applied: fixed HUD weapon anchors, unique possum namespace and stable monster rotations")
