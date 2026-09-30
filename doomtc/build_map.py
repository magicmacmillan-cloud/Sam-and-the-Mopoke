from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"sam-and-the-mopoke-map.wad"

def lump(name,data=b""):
    return name.encode("ascii")[:8].ljust(8,b"\0"),data

def tex8(s):
    return s.encode("ascii")[:8].ljust(8,b"\0")

def norm_edge(a,b):
    return tuple(sorted((tuple(a),tuple(b))))

# Each map is built from overlapping architectural rectangles. The compiler turns
# the union into many connected Doom sectors, so maps form rooms, branches, loops
# and voids instead of one long rectangular arena.
STYLE={
 "HOUSE":   (0,128,"HCARPET","HCEIL",176,"HOUSE"),
 "KITCHEN": (0,128,"KTILE","HCEIL",184,"KITCHEN"),
 "BATH":    (0,128,"PBATH","HCEIL",168,"PINKBATH"),
 "YARD":    (0,192,"GRASS","F_SKY1",176,"CORRUG"),
 "PLAY":    (0,224,"GRASS","F_SKY1",168,"PLAYGRND"),
 "FOREST":  (-8,256,"DIRT","F_SKY1",126,"FOREST"),
 "GRAVE":   (0,208,"GRAVEFL","F_SKY1",136,"GRAVE"),
 "TOMB":    (-16,112,"TOMBFL","TOMBCE",96,"TOMB"),
 "STATION": (0,160,"STNFLR","STNCEIL",144,"STATION"),
 "MALL":    (0,176,"MALLFLR","MALLCEIL",168,"MALL"),
 "LIB":     (0,144,"LIBFLR","LIBCEIL",104,"LIBRARY"),
}

def A(x0,y0,x1,y1,style):
    assert x0<x1 and y0<y1
    return (x0,y0,x1,y1,style)

MAPS=[
 dict(name="MAP01", title="ARNOLD STREET", areas=[
   A(0,-256,512,256,"HOUSE"),
   A(448,-96,1184,96,"HOUSE"),
   A(480,96,832,448,"HOUSE"),
   A(864,96,1216,448,"HOUSE"),
   A(448,-448,800,-96,"HOUSE"),
   A(1120,-352,1568,96,"KITCHEN"),
   A(1184,96,1440,384,"BATH"),
   A(1440,96,1696,384,"HOUSE"),
   A(1504,-96,1824,160,"HOUSE"),
   A(1760,-384,2240,384,"YARD"),
   A(2016,160,2240,448,"YARD"),
 ], exit=((2240,-96),(2240,96)), things=[
   (128,0,0,1,7),
   (640,300,180,15105,7),
   (704,-260,0,15103,7),(1030,300,0,15104,7),
   (1330,-180,0,15301,7),(1600,250,0,15301,7),
   (1840,200,0,15106,7),
   (1940,-180,0,15401,7),
   (2140,300,0,15108,7),
 ]),
 dict(name="MAP02", title="THE PLAYGROUND", areas=[
   A(0,-576,448,576,"PLAY"), A(384,-576,1216,-224,"PLAY"),
   A(384,224,1216,576,"PLAY"), A(1152,-576,1664,576,"PLAY"),
   A(704,-224,960,224,"PLAY"),
   A(1600,-288,2016,288,"PLAY"),
 ], exit=((2016,-224),(2016,224)), things=[
   (96,0,0,1,7),(420,420,0,15105,7),(620,-420,0,15101,7),
   (760,0,0,15301,7),(1080,430,0,15403,7),(1220,-430,0,15404,7),
   (1500,320,0,15403,7),(1720,-120,0,15107,7),
 ]),
 dict(name="MAP03", title="BLACK-GUM WOODS", areas=[
   A(0,-160,448,160,"FOREST"),
   A(384,-544,768,160,"FOREST"),
   A(384,-160,832,544,"FOREST"),
   A(704,-544,1088,-256,"FOREST"),
   A(768,256,1216,544,"FOREST"),
   A(1024,-416,1408,416,"FOREST"),
   A(1344,-640,1664,-96,"FOREST"),
   A(1344,96,1792,640,"FOREST"),
   A(1600,-160,1984,256,"FOREST"),
   A(1920,-384,2304,384,"FOREST"),
   A(2240,-128,2624,128,"FOREST"),
 ], exit=((2624,-96),(2624,96)), things=[
   (96,0,0,1,7),(520,-420,0,15403,7),(640,360,0,15404,7),
   (900,-360,0,15106,7),(1040,320,0,15101,7),(1180,0,0,15403,7),
   (1480,-520,0,15110,7),(1510,480,0,15108,7),(1670,480,0,15404,7),
   (1760,80,0,15410,7),(2060,-250,0,15302,7),(2180,230,0,15501,7),
   (2380,0,0,15001,7),(2500,0,0,15301,7),
 ]),
 dict(name="MAP04", title="CEMETERY", areas=[
   A(0,-192,384,192,"GRAVE"),
   A(320,-608,736,608,"GRAVE"),
   A(672,-608,1152,-320,"GRAVE"), A(672,320,1152,608,"GRAVE"),
   A(736,-128,1216,128,"GRAVE"),
   A(1088,-608,1536,608,"GRAVE"),
   A(1472,-224,1856,224,"GRAVE"),
   A(1664,-544,2048,-224,"GRAVE"),
   A(1792,224,2176,544,"GRAVE"),
   A(1792,-160,2304,160,"GRAVE"),
 ], exit=((2304,-96),(2304,96)), things=[
   (96,0,0,1,7),(520,-470,0,15408,7),(560,470,0,15408,7),
   (900,500,0,15109,7),(980,-500,0,15301,7),(1240,0,0,15408,7),
   (1510,420,0,15408,7),(1690,-360,0,15502,7),
   (1870,360,0,15111,7),
   (2040,0,0,15108,7),(2190,0,0,15002,7),
 ]),
 dict(name="MAP05", title="THE TOMB", areas=[
   A(0,-128,384,128,"TOMB"), A(320,-384,704,384,"TOMB"),
   A(640,-384,1024,-128,"TOMB"), A(640,128,1024,384,"TOMB"),
   A(896,-128,1280,128,"TOMB"),
   A(1152,-512,1536,-128,"TOMB"), A(1152,128,1536,512,"TOMB"),
   A(1408,-128,1792,128,"TOMB"),
   A(1664,-416,2048,416,"TOMB"),
   A(1984,-128,2368,128,"TOMB"),
 ], exit=((2368,-96),(2368,96)), things=[
   (96,0,0,1,7),(500,-260,0,15409,7),(520,260,0,15409,7),
   (820,-250,0,15301,7),(820,250,0,15109,7),
   (1060,0,0,15601,7),(1310,-350,0,15409,7),(1320,350,0,15003,7),
   (1580,0,0,15602,7),(1820,-260,0,15409,7),(1880,260,0,15106,7),
   (2150,0,0,15004,7),
 ]),
 dict(name="MAP06", title="UNDERGROUND STATION", areas=[
   A(0,-160,448,160,"STATION"),
   A(384,-512,896,512,"STATION"),
   A(832,-640,1536,-352,"STATION"),
   A(832,352,1536,640,"STATION"),
   A(896,-160,1408,160,"STATION"),
   A(1344,-512,1792,-192,"STATION"),
   A(1344,192,1792,512,"STATION"),
   A(1728,-192,2112,192,"STATION"),
   A(2048,-448,2496,-96,"STATION"),
   A(2048,96,2496,448,"STATION"),
   A(2432,-160,2816,160,"STATION"),
 ], exit=((2816,-96),(2816,96)), things=[
   (96,0,0,1,7),(470,0,0,15112,7),
   (720,-380,0,15405,7),(760,380,0,15405,7),
   (1080,-500,0,15405,7),(1120,500,0,15405,7),
   (1480,-350,0,15301,7),(1520,350,0,15109,7),
   (1800,0,0,15602,7),(2180,-280,0,15405,7),(2200,280,0,15405,7),
   (2400,300,0,15503,7),(2580,0,0,15005,7),
 ]),
 dict(name="MAP07", title="DIDDY MART", areas=[
   A(0,-192,448,192,"MALL"),
   A(384,-704,896,704,"MALL"),
   A(832,-704,1536,-352,"MALL"), A(832,352,1536,704,"MALL"),
   A(896,-224,1600,224,"MALL"),
   A(1472,-704,1984,-320,"MALL"),
   A(1472,320,1984,704,"MALL"),
   A(1792,-256,2368,256,"MALL"),
   A(2112,-704,2560,-320,"MALL"),
   A(2112,320,2560,704,"MALL"),
   A(2496,-224,3008,224,"MALL"),
   A(2944,-480,3392,480,"MALL"),
   A(3328,-160,3712,160,"MALL"),
 ], exit=((3712,-96),(3712,96)), things=[
   (96,0,0,1,7),(300,100,0,15112,7),(560,-520,0,15406,7),(600,520,0,15406,7),
   (1040,-500,0,15301,7),(1120,500,0,15108,7),(1360,0,0,15406,7),
   (1680,-520,0,15406,7),(1710,520,0,15406,7),(2050,0,0,15006,7),
   (2280,-520,0,15406,7),(2290,520,0,15301,7),(2700,0,0,15603,7),
   (3100,-300,0,15406,7),(3160,300,0,15007,7),(3500,0,0,15008,7),
 ]),
 dict(name="MAP08", title="THE IMPOSSIBLE LIBRARY", areas=[
   A(0,-160,448,160,"LIB"),
   A(384,-576,768,576,"LIB"),
   A(704,-576,1088,-256,"LIB"), A(704,256,1088,576,"LIB"),
   A(896,-192,1344,192,"LIB"),
   A(1280,-640,1664,-192,"LIB"), A(1280,192,1664,640,"LIB"),
   A(1536,-160,1984,160,"LIB"),
   A(1920,-576,2304,576,"LIB"),
   A(2240,-576,2688,-256,"LIB"), A(2240,256,2688,576,"LIB"),
   A(2496,-192,2944,192,"LIB"),
   A(2880,-640,3264,-192,"LIB"), A(2880,192,3264,640,"LIB"),
   A(3136,-160,3584,160,"LIB"),
   A(3520,-480,3968,480,"LIB"),
 ], exit=None, things=[
   (96,0,0,1,7),(250,80,0,15112,7),
   (560,-420,0,15407,7),(600,420,0,15407,7),(960,0,0,15109,7),
   (1420,-480,0,15407,7),(1440,480,0,15407,7),(1780,0,0,15410,7),
   (2080,-420,0,15407,7),(2100,420,0,15106,7),(2600,0,0,15009,7),
   (3000,-470,0,15407,7),(3040,470,0,15010,7),(3380,0,0,15301,7),
   (3740,0,180,15102,7),
 ]),
]

def build_map(md):
    areas=md["areas"]
    xs=sorted({v for a in areas for v in (a[0],a[2])})
    ys=sorted({v for a in areas for v in (a[1],a[3])})

    def covering(cx,cy):
        hit=None
        for a in areas:
            if a[0] <= cx < a[2] and a[1] <= cy < a[3]:
                hit=a
        return hit

    cells={}
    sectors=[]
    cell_style={}
    for ix in range(len(xs)-1):
        for iy in range(len(ys)-1):
            x0,x1=xs[ix],xs[ix+1]
            y0,y1=ys[iy],ys[iy+1]
            a=covering((x0+x1)/2,(y0+y1)/2)
            if a is None:
                continue
            st=a[4]
            fz,cz,ff,cf,light,wall=STYLE[st]
            sec=len(sectors)
            sectors.append((fz,cz,tex8(ff),tex8(cf),light,0,0))
            cells[(ix,iy)]=sec
            cell_style[(ix,iy)]=st

    verts=[]
    vmap={}
    def vid(x,y):
        k=(int(x),int(y))
        if k not in vmap:
            vmap[k]=len(verts)
            verts.append(k)
        return vmap[k]

    sidedefs=[]
    linedefs=[]
    def side(sec,upper="-",lower="-",middle="-"):
        i=len(sidedefs)
        sidedefs.append((0,0,tex8(upper),tex8(lower),tex8(middle),sec))
        return i

    exit_norm=norm_edge(*md["exit"]) if md.get("exit") else None

    def add_boundary(p1,p2,sec0,sec1=None,st0=None,st1=None):
        key=norm_edge(p1,p2)
        if sec1 is None:
            wall=STYLE[st0][5]
            special=11 if exit_norm==key else 0
            linedefs.append((vid(*p1),vid(*p2),1,special,0,side(sec0,middle=wall),0xFFFF))
        else:
            w0=STYLE[st0][5]
            w1=STYLE[st1][5]
            linedefs.append((vid(*p1),vid(*p2),4,0,0,
                             side(sec0,upper=w0,lower=w0),
                             side(sec1,upper=w1,lower=w1)))

    # Vertical grid boundaries. For a northward line, the east sector is side 0.
    for bx in range(len(xs)):
        x=xs[bx]
        for iy in range(len(ys)-1):
            left=cells.get((bx-1,iy))
            right=cells.get((bx,iy))
            y0,y1=ys[iy],ys[iy+1]
            if left is None and right is None:
                continue
            if left is not None and right is not None:
                add_boundary((x,y0),(x,y1),right,left,
                             cell_style[(bx,iy)],cell_style[(bx-1,iy)])
            elif right is not None:
                add_boundary((x,y0),(x,y1),right,None,cell_style[(bx,iy)])
            else:
                add_boundary((x,y1),(x,y0),left,None,cell_style[(bx-1,iy)])

    # Horizontal grid boundaries. For an eastward line, the south sector is side 0.
    for by in range(len(ys)):
        y=ys[by]
        for ix in range(len(xs)-1):
            below=cells.get((ix,by-1))
            above=cells.get((ix,by))
            x0,x1=xs[ix],xs[ix+1]
            if below is None and above is None:
                continue
            if below is not None and above is not None:
                add_boundary((x0,y),(x1,y),below,above,
                             cell_style[(ix,by-1)],cell_style[(ix,by)])
            elif below is not None:
                add_boundary((x0,y),(x1,y),below,None,cell_style[(ix,by-1)])
            else:
                add_boundary((x1,y),(x0,y),above,None,cell_style[(ix,by)])

    things=md["things"]
    bad=[t for t in things if covering(t[0],t[1]) is None]
    if bad:
        raise ValueError(f'{md["name"]}: things outside authored geometry: {bad}')

    return [
      lump(md["name"]),
      lump("THINGS",b"".join(struct.pack("<hhhhh",*x) for x in things)),
      lump("LINEDEFS",b"".join(struct.pack("<HHHHHHH",*x) for x in linedefs)),
      lump("SIDEDEFS",b"".join(struct.pack("<hh8s8s8sH",*x) for x in sidedefs)),
      lump("VERTEXES",b"".join(struct.pack("<hh",*x) for x in verts)),
      lump("SEGS"),lump("SSECTORS"),lump("NODES"),
      lump("SECTORS",b"".join(struct.pack("<hh8s8shhh",*x) for x in sectors)),
      lump("REJECT"),lump("BLOCKMAP")
    ],(len(sectors),len(linedefs),len(things))

L=[lump("SAMMPK",b"Sam and the Mopoke multi-map Doom II horror campaign")]
stats={}
for md in MAPS:
    ml,st=build_map(md)
    L.extend(ml)
    stats[md["name"]]=st

data=bytearray(b"PWAD"+struct.pack("<II",len(L),0))
entries=[]
for name,body in L:
    pos=len(data)
    data+=body
    entries.append((pos,len(body),name))
dirpos=len(data)
for pos,size,name in entries:
    data+=struct.pack("<II8s",pos,size,name)
data[8:12]=struct.pack("<I",dirpos)
OUT.write_bytes(data)

for m,(s,l,t) in stats.items():
    if s < 12:
        raise ValueError(f"{m}: not enough authored sectors ({s})")
    print(f"{m}: sectors={s} linedefs={l} things={t}")
print(OUT)
