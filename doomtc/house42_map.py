import struct

# Detailed classic-Doom MAP01 reconstruction of the 42 Arnold house/street block.
# Coordinate convention: north/backyard = +Y, east/driveway = +X.
# Approximate scale: 64 map units ~= 1 metre.

def lump(name,data=b""):
    return name.encode("ascii")[:8].ljust(8,b"\0"),data

def tex8(s):
    return s.encode("ascii")[:8].ljust(8,b"\0")

def norm_edge(a,b):
    return tuple(sorted((tuple(a),tuple(b))))

# floor z, ceiling z, floor flat, ceiling flat, light, wall texture
STYLE = {
    "ENTRY":   (0,128,"H42TILF","H42CEIL",176,"H42WALL"),
    "HALL":    (0,128,"H42TILF","H42CEIL",164,"H42WALL"),
    "LOUNGE":  (0,128,"H42CARP","H42CEIL",156,"H42WALL"),
    "BED":     (0,128,"H42CARP","H42CEIL",152,"H42WALL"),
    "BEDWOOD": (0,128,"H42WOOD","H42CEIL",156,"H42WALL"),
    "BATH":    (0,128,"H42TILF","H42CEIL",176,"H42BATH"),
    "MEALS":   (0,128,"H42VNYL","H42CEIL",164,"H42PANL"),
    "KITCH":   (0,128,"H42VNYL","H42CEIL",180,"H42KTCH"),
    "LAUNDRY": (0,128,"H42WOOD","H42CEIL",168,"H42PANL"),
    "SUNROOM": (0,120,"H42CONC","H42CEIL",148,"H42WALL"),
    "PORCH":   (0,112,"H42CONC","H42CEIL",160,"H42SIDN"),
    "DRIVE":   (0,192,"H42CONC","F_SKY1",168,"H42FENC"),
    "YARD":    (0,192,"H42GRAS","F_SKY1",156,"H42FENC"),
    "PATIO":   (0,192,"H42PAVE","F_SKY1",160,"H42FENC"),
    "SHED":    (0,128,"H42CONC","H42CEIL",132,"H42SHED"),
    "FOOT":    (0,192,"H42CONC","F_SKY1",168,"H42CURB"),
    "VERGE":   (0,192,"H42GRAS","F_SKY1",160,"H42CURB"),
    "ROAD":    (0,192,"H42ASPH","F_SKY1",152,"H42CURB"),
    "RESERVE": (0,224,"H42GRAS","F_SKY1",144,"H42FENC"),
    "PLAY":    (0,224,"H42PAVE","F_SKY1",160,"H42PLAY"),
    "LOT":     (0,192,"H42GRAS","F_SKY1",150,"H42FENC"),
    # Zero-height sectors form solid neighbour-house massing while keeping
    # the site legible in automap/node builders.
    "NBR1":    (128,128,"H42ROOF","H42ROOF",128,"H42NBR1"),
    "NBR2":    (128,128,"H42ROOF","H42ROOF",128,"H42NBR2"),
}

def A(x0,y0,x1,y1,style):
    assert x0 < x1 and y0 < y1
    return (x0,y0,x1,y1,style)

# Area order matters: later rectangles override earlier ones.
AREAS = [
    # --- west reserve / playground context ---
    A(-2400,-1408,-1248,1800,"RESERVE"),
    A(-2200,-1216,-1600,-768,"PLAY"),
    A(-1600,-1024,-1248,-704,"FOOT"),

    # --- Collenso Street ---
    A(-1248,-1408,-960,1800,"ROAD"),
    A(-960,-1408,-912,1800,"VERGE"),

    # --- Arnold Street public realm ---
    A(-2400,-704,2000,-608,"FOOT"),
    A(-2400,-608,2000,-256,"ROAD"),
    A(-2400,-256,2000,-96,"VERGE"),
    A(-2400,-96,2000,0,"FOOT"),

    # --- opposite lots / houses 39, 37, 35 ---
    A(-944,-1408,-48,-720,"LOT"),
    A(16,-1408,960,-720,"LOT"),
    A(1008,-1408,1920,-720,"LOT"),
    A(-816,-1328,-160,-896,"NBR2"),
    A(96,-1328,800,-896,"NBR1"),
    A(1104,-1328,1776,-896,"NBR2"),

    # --- immediate neighbours 44 and 40 ---
    A(-944,16,-48,2944,"LOT"),
    A(1008,16,1920,2944,"LOT"),
    A(-816,320,-160,1110,"NBR1"),
    A(1104,320,1776,1088,"NBR2"),
    # rear sheds / outbuildings as solid massing
    A(-720,1450,-256,2080,"NBR1"),
    A(1260,1350,1740,2150,"NBR1"),

    # --- 42 Arnold yard / driveway / rear ---
    A(16,16,960,320,"YARD"),
    A(16,320,96,1312,"YARD"),
    A(704,320,960,1312,"YARD"),
    A(16,1312,960,1600,"YARD"),
    A(16,1600,960,2944,"YARD"),
    A(384,16,448,320,"FOOT"),
    A(736,16,928,1600,"DRIVE"),
    A(704,1312,928,1750,"PATIO"),
    A(560,1750,896,2350,"SHED"),

    # Front porch/covered entry from facade photo.
    A(320,256,704,368,"PORCH"),

    # --- house rooms, separated by real wall gaps ---
    # Front-left projecting room.
    A(96,320,336,624,"BED"),
    # Central tiled entry and hall.
    A(352,384,448,544,"ENTRY"),
    A(352,544,448,960,"HALL"),
    # Front-right lounge with large front window/chimney.
    A(464,384,704,688,"LOUNGE"),
    # Middle-left second bedroom.
    A(96,640,336,800,"BED"),
    # Bathroom shown in walkthrough, including toilet.
    A(96,816,320,960,"BATH"),
    # Third bedroom with polished boards / robe.
    A(464,704,704,960,"BEDWOOD"),
    # Rear meals/kitchen/laundry.
    A(96,976,336,1152,"MEALS"),
    A(352,976,544,1152,"KITCH"),
    A(560,976,704,1152,"LAUNDRY"),
    # Enclosed rear veranda/sunroom strip.
    A(96,1168,704,1312,"SUNROOM"),

    # --- door openings / room connectors ---
    A(384,352,416,400,"ENTRY"),      # porch -> front entry
    A(320,448,368,512,"HALL"),       # entry -> front-left room
    A(432,448,480,512,"HALL"),       # entry -> lounge
    A(320,688,368,752,"HALL"),       # hall -> bed 2
    A(304,848,368,912,"HALL"),       # hall -> bathroom
    A(432,752,480,816,"HALL"),       # hall -> bed 3
    A(384,944,416,992,"HALL"),       # hall -> rear
    A(320,1024,368,1088,"MEALS"),    # meals <-> kitchen
    A(528,1040,576,1104,"KITCH"),    # kitchen <-> laundry
    A(416,1136,480,1184,"KITCH"),    # kitchen -> sunroom
    A(608,1136,656,1184,"LAUNDRY"),  # laundry -> sunroom
    A(320,1296,384,1344,"PATIO"),    # sunroom -> backyard
    A(688,1216,752,1280,"DRIVE"),    # sunroom -> carport side

    # Front fence openings. The 16-unit front boundary gap becomes the fence;
    # these two bridges are the pedestrian and driveway gates.
    A(384,-16,448,32,"FOOT"),
    A(736,-16,928,32,"DRIVE"),

    # Neighbour front driveway hints.
    A(-352,-16,-160,32,"DRIVE"),
    A(1600,-16,1792,32,"DRIVE"),
]

# Explicit windows/detail panels. These coordinates are also injected as grid cuts.
LINE_TEX = {
    norm_edge((144,320),(288,320)):"H42WIND",   # front-left room
    norm_edge((512,384),(672,384)):"H42WIND",   # lounge/front
    norm_edge((96,688),(96,768)):"H42WIND",     # bedroom 2 west
    norm_edge((96,848),(96,928)):"H42WIND",     # bathroom/frosted read
    norm_edge((704,768),(704,896)):"H42WIND",   # bedroom 3 east
    norm_edge((96,1024),(96,1104)):"H42WIND",   # meals/rear side
    norm_edge((704,1024),(704,1104)):"H42WIND", # laundry side
    norm_edge((128,1312),(288,1312)):"H42WIND", # sunroom rear glazing
    norm_edge((400,1312),(560,1312)):"H42WIND",
    norm_edge((704,432),(704,608)):"H42BRIK",   # chimney mass on right facade
    # neighbour facade windows for context
    norm_edge((-640,320),(-384,320)):"H42WIND",
    norm_edge((1260,320),(1516,320)):"H42WIND",
}

HOUSE_STYLES={"ENTRY","HALL","LOUNGE","BED","BEDWOOD","BATH","MEALS","KITCH","LAUNDRY","SUNROOM"}

def _is_house_exterior(p1,p2,st):
    if st not in HOUSE_STYLES:
        return False
    x1,y1=p1; x2,y2=p2
    if x1==x2:
        x=x1; lo,hi=sorted((y1,y2))
        if x==96 and 320 <= lo and hi <= 1312: return True
        if x==704 and 384 <= lo and hi <= 1312: return True
        if x==336 and 320 <= lo and hi <= 384: return True
        if x==352 and 368 <= lo and hi <= 384: return True
        if x==448 and 368 <= lo and hi <= 384: return True
    if y1==y2:
        y=y1; lo,hi=sorted((x1,x2))
        if y==320 and 96 <= lo and hi <= 336: return True
        if y==384 and 352 <= lo and hi <= 704: return True
        if y==1312 and 96 <= lo and hi <= 704: return True
    return False

def _segment_inside(seg,whole):
    (a1,a2)=seg; (b1,b2)=whole
    if a1[0]==a2[0]==b1[0]==b2[0]:
        alo,ahi=sorted((a1[1],a2[1])); blo,bhi=sorted((b1[1],b2[1]))
        return blo <= alo and ahi <= bhi
    if a1[1]==a2[1]==b1[1]==b2[1]:
        alo,ahi=sorted((a1[0],a2[0])); blo,bhi=sorted((b1[0],b2[0]))
        return blo <= alo and ahi <= bhi
    return False

def _boundary_texture(p1,p2,st):
    key=norm_edge(p1,p2)
    for whole,tex in LINE_TEX.items():
        if _segment_inside(key,whole):
            return tex
    x1,y1=p1; x2,y2=p2
    # Black metal front rail/gate appearance seen in facade photo.
    if y1==y2==16:
        lo,hi=sorted((x1,x2))
        if 16 <= lo and hi <= 960:
            return "H42GATE"
    if _is_house_exterior(p1,p2,st):
        return "H42SIDN"
    return STYLE[st][5]

OUTDOOR_STYLES={"PORCH","DRIVE","YARD","PATIO","FOOT","VERGE","ROAD","RESERVE","PLAY","LOT"}

def _solid_boundary(p1,p2,st0,st1):
    pair={st0,st1}
    # House envelope is physically walled from exterior sectors. Door connector
    # rectangles already replace the wall exactly where passage is intended.
    if (st0 in HOUSE_STYLES and st1 in OUTDOOR_STYLES) or (st1 in HOUSE_STYLES and st0 in OUTDOOR_STYLES):
        return True
    # Shed is solid except its south-facing doorway.
    if "SHED" in pair and (st0 in OUTDOOR_STYLES or st1 in OUTDOOR_STYLES):
        (x1,y1),(x2,y2)=p1,p2
        if y1==y2==1750:
            lo,hi=sorted((x1,x2))
            if 640 <= lo and hi <= 768:
                return False
        return True
    return False

def build_house42_map():
    xs={v for a in AREAS for v in (a[0],a[2])}
    ys={v for a in AREAS for v in (a[1],a[3])}
    for p1,p2 in LINE_TEX:
        xs.add(p1[0]); xs.add(p2[0]); ys.add(p1[1]); ys.add(p2[1])
    # Extra cuts split the right-side chimney and front facade into useful line spans.
    xs.update((144,288,512,672,128,400,560,1260,1516,-640,-384))
    ys.update((432,608,688,768,848,928,1024,1104))
    xs=sorted(xs); ys=sorted(ys)

    def covering(cx,cy):
        hit=None
        for a in AREAS:
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

    verts=[]; vmap={}
    def vid(x,y):
        k=(int(x),int(y))
        if k not in vmap:
            vmap[k]=len(verts); verts.append(k)
        return vmap[k]

    sidedefs=[]; linedefs=[]
    def side(sec,upper="-",lower="-",middle="-"):
        i=len(sidedefs)
        sidedefs.append((0,0,tex8(upper),tex8(lower),tex8(middle),sec))
        return i

    EXIT=norm_edge((-2200,-1024),(-2200,-896))

    def add_boundary(p1,p2,sec0,sec1=None,st0=None,st1=None):
        key=norm_edge(p1,p2)
        if sec1 is None:
            wall=_boundary_texture(p1,p2,st0)
            special=11 if key==EXIT else 0
            linedefs.append((vid(*p1),vid(*p2),1,special,0,side(sec0,middle=wall),0xFFFF))
        else:
            w0=STYLE[st0][5]; w1=STYLE[st1][5]
            if _solid_boundary(p1,p2,st0,st1):
                # Blocking two-sided midtexture = actual wall while retaining valid
                # sectors on both sides for the yard/porch/driveway.
                hst=st0 if st0 in HOUSE_STYLES else (st1 if st1 in HOUSE_STYLES else ("SHED" if "SHED" in (st0,st1) else st0))
                wall=_boundary_texture(p1,p2,hst)
                linedefs.append((vid(*p1),vid(*p2),5,0,0,
                                 side(sec0,middle=wall),
                                 side(sec1,middle=wall)))
            else:
                # Normal open two-sided transition. Height differences (neighbour
                # massing) get upper/lower walls and remain physically impassable.
                special=11 if key==EXIT else 0
                linedefs.append((vid(*p1),vid(*p2),4,special,0,
                                 side(sec0,upper=w0,lower=w0),
                                 side(sec1,upper=w1,lower=w1)))

    # Vertical boundaries.
    for bx in range(len(xs)):
        x=xs[bx]
        for iy in range(len(ys)-1):
            left=cells.get((bx-1,iy)); right=cells.get((bx,iy))
            y0,y1=ys[iy],ys[iy+1]
            if left is None and right is None: continue
            if left is not None and right is not None:
                add_boundary((x,y0),(x,y1),right,left,cell_style[(bx,iy)],cell_style[(bx-1,iy)])
            elif right is not None:
                add_boundary((x,y0),(x,y1),right,None,cell_style[(bx,iy)])
            else:
                add_boundary((x,y1),(x,y0),left,None,cell_style[(bx-1,iy)])

    # Horizontal boundaries.
    for by in range(len(ys)):
        y=ys[by]
        for ix in range(len(xs)-1):
            below=cells.get((ix,by-1)); above=cells.get((ix,by))
            x0,x1=xs[ix],xs[ix+1]
            if below is None and above is None: continue
            if below is not None and above is not None:
                add_boundary((x0,y),(x1,y),below,above,cell_style[(ix,by-1)],cell_style[(ix,by)])
            elif below is not None:
                add_boundary((x0,y),(x1,y),below,None,cell_style[(ix,by-1)])
            else:
                add_boundary((x1,y),(x0,y),above,None,cell_style[(ix,by)])

    # Classic Doom thing records: x,y,angle,type,flags.
    things=[
        (400,470,90,1,7),           # player: tiled entry
        (560,520,180,15105,7),      # Sam runner in/near front lounge
        (416,120,180,15103,7),      # cola clue at front path
        (416,-180,180,15101,7),     # footprints near Arnold Street
        (-1080,-420,180,15106,7),   # false trail on Collenso
        (-1500,-820,180,15410,7),   # Mopoke glimpse toward reserve
        (-1840,-940,180,15108,7),   # Sam message by playground approach
        (720,2060,180,15301,7),     # searchable shed/cache
        (820,1500,180,15403,7),     # small backyard threat
    ]
    bad=[t for t in things if covering(t[0],t[1]) is None]
    if bad:
        raise ValueError(f"MAP01 house42 things outside authored geometry: {bad}")

    out=[
      lump("MAP01"),
      lump("THINGS",b"".join(struct.pack("<hhhhh",*x) for x in things)),
      lump("LINEDEFS",b"".join(struct.pack("<HHHHHHH",*x) for x in linedefs)),
      lump("SIDEDEFS",b"".join(struct.pack("<hh8s8s8sH",*x) for x in sidedefs)),
      lump("VERTEXES",b"".join(struct.pack("<hh",*x) for x in verts)),
      lump("SEGS"),lump("SSECTORS"),lump("NODES"),
      lump("SECTORS",b"".join(struct.pack("<hh8s8shhh",*x) for x in sectors)),
      lump("REJECT"),lump("BLOCKMAP")
    ]
    return out,(len(sectors),len(linedefs),len(things))
