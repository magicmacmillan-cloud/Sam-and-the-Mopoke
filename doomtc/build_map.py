from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"sam-test-map.wad"

def lump(name,data=b""):
    return name.encode("ascii")[:8].ljust(8,b"\0"),data

def tex8(s):
    return s.encode("ascii")[:8].ljust(8,b"\0")

# Simple rectangular Doom-format weapon/sprite test arena.
verts=[(-1024,-768),(1024,-768),(1024,768),(-1024,768)]
sidedefs=[]
linedefs=[]
for i in range(4):
    sidedefs.append((0,0,tex8("-"),tex8("-"),tex8("STARTAN3"),0))
    linedefs.append((i,(i+1)%4,1,0,0,i,0xFFFF))

# floor, ceiling, floor flat, ceiling flat, light, special, tag
sectors=[(0,192,tex8("FLOOR0_1"),tex8("CEIL1_1"),192,0,0)]

# player, 13 weapons, ammo, Sam, Mopoke.
things=[
    (0,0,0,1,7),
    (-800,-500,0,15001,7),(-550,-500,0,15002,7),(-300,-500,0,15003,7),
    (-50,-500,0,15004,7),(200,-500,0,15005,7),(450,-500,0,15006,7),
    (700,-500,0,15007,7),
    (-800,500,180,15008,7),(-550,500,180,15009,7),(-300,500,180,15010,7),
    (-50,500,180,15011,7),(200,500,180,15012,7),(450,500,180,15013,7),
    (700,500,180,15200,7),
    (-700,0,0,15101,7),
    (700,0,180,15102,7)
]

lumps=[
    lump("SAMMPK",b"Sam and the Mopoke Doom II mod"),
    lump("MAP01"),
    lump("THINGS",b"".join(struct.pack("<hhhhh",*t) for t in things)),
    lump("LINEDEFS",b"".join(struct.pack("<HHHHHHH",*x) for x in linedefs)),
    lump("SIDEDEFS",b"".join(struct.pack("<hh8s8s8sH",*x) for x in sidedefs)),
    lump("VERTEXES",b"".join(struct.pack("<hh",*x) for x in verts)),
    lump("SEGS"),lump("SSECTORS"),lump("NODES"),
    lump("SECTORS",b"".join(struct.pack("<hh8s8shhh",*x) for x in sectors)),
    lump("REJECT"),lump("BLOCKMAP")
]

data=bytearray(b"PWAD"+struct.pack("<II",len(lumps),0))
entries=[]
for name,body in lumps:
    pos=len(data); data+=body; entries.append((pos,len(body),name))
dirpos=len(data)
for pos,size,name in entries:
    data+=struct.pack("<II8s",pos,size,name)
data[8:12]=struct.pack("<I",dirpos)
OUT.write_bytes(data)
print(OUT)
