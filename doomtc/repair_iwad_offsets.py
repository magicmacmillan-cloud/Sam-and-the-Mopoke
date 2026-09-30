"""Repair Doom art origins in the final IWAD (not the Android overlay).

A PNG's grAb chunk changes its rendering anchor without altering its pixels.
Weapon canvases that are already centred at 320x200 must not also have a
horizontal half-width grAb. HUD art and mugshots must not be lifted by their
own height; SBARINFO already supplies their screen position.
"""
from pathlib import Path
import re
import struct
import sys
import zlib

WEAPONS = {"ZHND", "DMST", "AMUL", "VIRS", "DOLL", "BLOD", "FEEB",
           "DACR", "SCOT", "GAUN", "FEAT", "SAUS", "TOES", "JAND"}
FACE = re.compile(r"^DAD(?:ST|TR|TL|OUCH|EVL|KILL|GOD|DEAD)")
PNG = b"\x89PNG\r\n\x1a\n"


def origin(data):
    assert data.startswith(PNG)
    position = 8
    while position + 12 <= len(data):
        size = struct.unpack_from(">I", data, position)[0]
        kind = data[position + 4:position + 8]
        if kind == b"grAb":
            assert size == 8
            return position, struct.unpack_from(">ii", data, position + 8)
        position += size + 12
    raise ValueError("artwork PNG missing grAb placement")


def repair(path):
    buf = bytearray(Path(path).read_bytes())
    assert buf[:4] == b"IWAD"
    count, directory = struct.unpack_from("<II", buf, 4)
    fixed = {"STBAR": 0, "faces": 0, "firstperson": 0}
    bar_height = None
    config = None
    for i in range(count):
        start, length, raw = struct.unpack_from("<II8s", buf, directory + 16*i)
        assert start + length <= len(buf)
        name = raw.rstrip(b"\x00").decode("ascii")
        if name == "SBARINFO":
            config = bytes(buf[start:start+length]).decode("utf-8")
        data = bytes(buf[start:start + length])
        if not data.startswith(PNG):
            continue
        if name == "STBAR":
            bar_height = struct.unpack_from(">I", data, 20)[0]
            destination, category = (0, 0), "STBAR"
        elif FACE.match(name):
            destination, category = (0, 0), "faces"
        elif (name[:4] in WEAPONS and len(name) == 6
              and name[4] in "ABCDEFGH" and name[5] == "0"
              and struct.unpack_from(">II", data, 16) == (320, 200)):
            anchor, old = origin(data)
            destination, category = (0, old[1]), "firstperson"
        else:
            continue
        anchor, old = origin(data)
        if old == destination:
            continue
        # Only grAb data and its PNG CRC change. Width, pixels and frame names
        # remain byte-identical. Lump sizes and WAD directory never change.
        struct.pack_into(">ii", buf, start + anchor + 8, *destination)
        crc = zlib.crc32(buf[start + anchor + 4:start + anchor + 16])
        struct.pack_into(">I", buf, start + anchor + 16, crc & 0xffffffff)
        fixed[category] += 1
    assert config is not None and bar_height is not None
    height = re.search(r"\bheight\s+(\d+)", config)
    draw = re.search(r'drawimage\s+"STBAR"\s*,\s*\d+\s*,\s*(\d+)', config)
    assert height and draw
    assert int(height.group(1)) == bar_height
    assert int(draw.group(1)) == 200 - bar_height
    Path(path).write_bytes(buf)
    print("Final IWAD HUD origin repair:", fixed, "status bar height:", bar_height)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: repair_iwad_offsets.py path/to/IWAD.wad")
    repair(sys.argv[1])
