import struct

# Detailed classic-Doom MAP01 reconstruction of the 42 Arnold house/street block.
# V32: gameplay/visual rebuild from the supplied walkthrough + satellite references.
# Coordinate convention: north/backyard = +Y, east/right driveway = +X.
# FRONT = Arnold Street / low-Y. REAR = backyard / high-Y.
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
    "SUNROOM": (0,120,"H42CONC","H42CEIL",142,"H42WALL"),
    "PORCH":   (0,112,"H42CONC","H42CEIL",176,"H42SIDN"),
    "DRIVE":   (0,192,"H42DRV","F_SKY1",112,"H42FENC"),
    "YARD":    (0,192,"H42LWN","F_SKY1",104,"H42FENC"),
    "PATIO":   (0,192,"H42PAVE","F_SKY1",112,"H42FENC"),
    "SHED":    (0,128,"H42CONC","H42CEIL",132,"H42SHED"),
    "FOOT":    (0,192,"H42PATH","F_SKY1",108,"H42CURB"),
    "VERGE":   (0,192,"H42VERG","F_SKY1",94,"H42CURB"),
    "ROAD":    (0,192,"H42ROAD","F_SKY1",86,"H42CURB"),
    "RESERVE": (0,224,"H42GRAS","F_SKY1",72,"H42FENC"),
    "PLAY":    (0,224,"H42SAFE","F_SKY1",94,"H42PLAY"),
    "LOT":     (0,192,"H42LWN","F_SKY1",82,"H42FENC"),
    "DOOR":    (0,0,"H42TILF","H42CEIL",160,"H42FRNT"),
    "BACKDOOR":(0,0,"H42CONC","H42CEIL",150,"H42RDR"),
    "GATEDOOR":(0,0,"H42SAFE","F_SKY1",118,"H42GATE"),
    "IDOOR":   (0,0,"H42TILF","H42CEIL",150,"H42DOOR"),
    "AWNING":  (0,112,"H42PAVE","H42ROOF",126,"H42SIDN"),
    "CARPORT": (0,112,"H42DRV","H42CEIL",138,"H42SHED"),
    "GARDEN":  (0,192,"H42BED","F_SKY1",72,"H42FENC"),
    "DIG":     (-2,192,"H42DIRT","F_SKY1",78,"H42FENC"),
    "STLIT":   (0,192,"H42ROAD","F_SKY1",176,"H42CURB"),
    "PLAYLIT": (0,224,"H42SAFE","F_SKY1",160,"H42PLAY"),
    "YARDLIT": (0,192,"H42LWN","F_SKY1",146,"H42FENC"),
    "LOWBRIK": (34,34,"H42CONC","H42CONC",112,"H42BRIK"),
    "FURNWOOD":(40,128,"H42WOOD","H42CEIL",136,"H42PANL"),
    "FURNFAB": (36,128,"H42CARP","H42CEIL",132,"H42SOFA"),
    "FIXWHITE":(44,128,"H42TILF","H42CEIL",156,"H42WDR"),
    "FIXPINK": (38,128,"H42TILF","H42CEIL",164,"H42BATH"),
    "APPLI":   (44,128,"H42TILF","H42CEIL",150,"H42APPL"),
    "POST":    (128,128,"H42CONC","H42CONC",128,"H42SIDN"),
    "PLAYEQ":  (36,224,"H42PAVE","F_SKY1",150,"H42PLAY"),
    # Zero-height sectors form solid neighbour-house massing while keeping
    # the site legible in automap/node builders.
    "NBR1":    (104,104,"H42ROOF","H42ROOF",104,"H42NBR1"),
    "NBR2":    (104,104,"H42ROOF","H42ROOF",104,"H42NBR2"),
    "NBRR1":   (148,148,"H42ROOF","H42ROOF",92,"H42ROFW"),
    "NBRR2":   (140,140,"H42ROOF","H42ROOF",88,"H42ROFW"),
}

def A(x0,y0,x1,y1,style):
    assert x0 < x1 and y0 < y1
    return (x0,y0,x1,y1,style)

# Area order matters: later rectangles override earlier ones.
AREAS = [
    # --- reserve and playground west of Collenso / up Arnold Street ---
    A(-2500,-1500,-1248,1900,"RESERVE"),
    A(-2240,-1180,-1540,-700,"PLAY"),
    A(-1700,-930,-1652,-830,"PLAYLIT"),
    A(-1620,-980,-1248,-700,"FOOT"),
    A(-1880,-820,-1620,-750,"FOOT"),
    A(-1700,-700,-1600,-300,"FOOT"),
    A(-1600,-300,-1480,200,"FOOT"),
    A(-1480,200,-1360,700,"FOOT"),
    A(-1360,700,-1260,1150,"FOOT"),

    # Padlocked playground entrance. The door sector itself is the iron gate.
    A(-1652,-930,-1620,-830,"GATEDOOR"),

    # Playground equipment as sector silhouettes, supplemented by sprites.
    A(-2130,-1020,-2020,-965,"PLAYEQ"),
    A(-1990,-960,-1890,-865,"PLAYEQ"),
    A(-1905,-870,-1815,-815,"PLAYEQ"),
    A(-1775,-1015,-1640,-960,"PLAYEQ"),

    # --- Collenso Street ---
    A(-1312,-1500,-1248,1900,"FOOT"),
    A(-1248,-1500,-960,1900,"ROAD"),
    A(-960,-1500,-912,1900,"VERGE"),
    A(-912,-1500,-864,1900,"FOOT"),

    # --- Arnold Street public realm: footpath / verge / road / verge / footpath ---
    A(-2500,-704,2100,-608,"FOOT"),
    A(-2500,-608,2100,-256,"ROAD"),
    A(-2500,-256,2100,-96,"VERGE"),
    A(-2500,-96,2100,0,"FOOT"),
    # small pools of brighter light under street lamps
    A(-760,-580,-500,-300,"STLIT"),
    A(40,-580,300,-300,"STLIT"),
    A(940,-580,1200,-300,"STLIT"),
    A(-1248,-760,-960,-500,"STLIT"),
    A(-1780,-980,-1580,-760,"PLAYLIT"),

    # --- opposite lots/houses 39,37,35 ---
    A(-944,-1500,-48,-720,"LOT"),
    A(16,-1500,960,-720,"LOT"),
    A(1008,-1500,1980,-720,"LOT"),
    A(-816,-1330,-160,-900,"NBR2"),
    A(-640,-1180,-384,-960,"NBRR2"),
    A(96,-1330,800,-900,"NBR1"),
    A(128,-1180,672,-960,"NBRR1"),
    A(1104,-1330,1776,-900,"NBR2"),
    A(1260,-1180,1516,-960,"NBRR2"),

    # Fill the thin frontage/lot gaps: these must be real outdoor space, never void walls.
    A(-944,-720,1980,-704,"FOOT"),
    A(-944,0,1980,16,"FOOT"),

    # --- immediate neighbours 44 and 40 ---
    A(-944,16,-48,2944,"LOT"),
    A(1008,16,1980,2944,"LOT"),
    A(-816,320,-160,1110,"NBR1"),
    A(-640,384,-384,1024,"NBRR1"),
    A(1104,320,1776,1088,"NBR2"),
    A(1260,384,1516,1024,"NBRR2"),
    A(-720,1450,-256,2080,"NBR1"),
    A(-880,2140,-520,2580,"NBR1"),
    A(1260,1350,1740,2150,"NBR1"),
    A(1120,2240,1600,2700,"NBR1"),
    # neighbour driveways/paths
    A(-400,16,-160,320,"DRIVE"),
    A(-600,160,-520,320,"FOOT"),
    A(1600,16,1820,320,"DRIVE"),
    A(1320,180,1380,320,"FOOT"),

    # Fill the two side-boundary gaps and behind the rear fence so fences are
    # two-sided midtextures with sky above, not 192-unit enclosing walls.
    A(-48,16,16,3100,"LOT"),
    A(960,16,1008,3100,"LOT"),
    A(16,2944,960,3100,"LOT"),

    # --- 42 Arnold yard / front / driveway / rear ---
    A(16,16,960,320,"YARD"),
    A(16,320,96,1312,"YARD"),
    A(704,320,960,1312,"YARD"),
    A(16,1312,960,1600,"YARD"),
    A(16,1600,960,2944,"YARD"),
    A(384,16,448,320,"FOOT"),
    A(736,16,928,1312,"DRIVE"),
    A(736,384,928,1312,"CARPORT"),
    A(704,1312,928,1750,"AWNING"),
    A(560,1750,896,2350,"SHED"),

    # planted beds and dog-dig evidence
    A(64,176,304,304,"GARDEN"),
    A(472,224,672,304,"GARDEN"),

    A(32,1360,96,2200,"GARDEN"),
    A(896,1750,944,2500,"GARDEN"),
    A(160,2820,330,2944,"DIG"),

    # Front porch/covered entry.
    A(320,256,704,368,"PORCH"),

    # --- house plan ---
    # front entry and central hall
    A(352,384,448,528,"ENTRY"),
    A(352,528,448,960,"HALL"),

    # pair 1: lounge opposite bathroom
    A(464,544,704,704,"LOUNGE"),
    A(96,544,336,704,"BATH"),

    # pair 2: Sam room opposite master bedroom
    A(464,736,704,928,"BED"),
    A(96,736,336,928,"BEDWOOD"),

    # rear: Lincoln room off kitchen, kitchen, small laundry
    A(96,976,336,1152,"BED"),
    A(352,976,544,1152,"KITCH"),
    A(560,976,704,1152,"LAUNDRY"),

    # long enclosed rear sunroom/veranda
    A(96,1168,704,1312,"SUNROOM"),

    # --- proper doors/connectors ---
    A(384,352,416,384,"DOOR"),       # real front door
    A(384,512,416,544,"ENTRY"),      # entry -> hall
    A(320,576,368,640,"IDOOR"),      # bathroom door
    A(432,576,480,640,"IDOOR"),      # lounge door
    A(320,792,368,856,"IDOOR"),      # master bedroom door
    A(432,792,480,856,"IDOOR"),      # Sam bedroom door
    A(384,944,416,992,"IDOOR"),      # kitchen/hall door
    A(320,1024,368,1088,"IDOOR"),    # Lincoln bedroom door off kitchen
    A(528,1040,576,1104,"KITCH"),    # kitchen <-> laundry
    A(608,1136,656,1184,"LAUNDRY"),  # laundry <-> sunroom
    A(624,1296,688,1312,"BACKDOOR"), # actual locked rear/sunroom door
    A(624,1312,688,1344,"PATIO"),    # backyard threshold outside rear door

    # Front pedestrian/driveway gates.
    A(384,-16,448,32,"FOOT"),
    A(736,-16,928,32,"DRIVE"),

    # --- room furniture/fixtures from video ---
    # lounge
    A(500,570,688,614,"FURNFAB"),
    A(532,632,628,676,"FURNWOOD"),
    A(660,616,700,688,"FURNWOOD"),
    # bathroom
    A(104,552,216,586,"FIXPINK"),
    A(108,620,164,690,"FIXPINK"),
    A(246,620,310,692,"FIXWHITE"),
    # master
    A(112,760,236,880,"FURNFAB"),
    A(272,744,328,912,"FURNWOOD"),
    # Sam room
    A(488,760,608,872,"FURNFAB"),
    A(648,752,696,912,"FURNWOOD"),
    # Lincoln room off kitchen
    A(112,992,224,1104,"FURNFAB"),
    A(272,992,328,1136,"FURNWOOD"),
    # kitchen cabinetry/appliances
    A(360,992,384,1136,"FURNWOOD"),
    A(384,1104,528,1144,"FURNWOOD"),
    A(500,988,540,1044,"APPLI"),
    # laundry
    A(572,992,696,1032,"FURNWOOD"),
    A(648,1048,696,1128,"APPLI"),
    # sunroom storage
    A(112,1184,288,1218,"FURNWOOD"),
    # garage/shed workbench where the spare key is hidden nearby
    A(584,2190,872,2240,"FURNWOOD"),
    A(828,1800,884,1976,"FURNWOOD"),
    # porch posts
    A(336,320,352,368,"POST"),
    A(688,320,704,368,"POST"),
]

# Explicit windows/detail panels. These coordinates are also injected as grid cuts.
LINE_TEX = {
    norm_edge((512,384),(672,384)):"H42LWIN",    # warm front lounge window
    norm_edge((144,384),(288,384)):"H42WIND",    # darker front/left window
    norm_edge((96,576),(96,672)):"H42WIND",      # bathroom side/frosted treatment
    norm_edge((96,776),(96,896)):"H42WIND",      # master side window
    norm_edge((704,776),(704,896)):"H42WIND",    # Sam room side window
    norm_edge((96,1024),(96,1104)):"H42WIND",    # Lincoln room side
    norm_edge((704,1024),(704,1104)):"H42WIND",  # laundry side
    norm_edge((112,1312),(304,1312)):"H42RWIN",  # broad rear sunroom glazing
    norm_edge((368,1312),(608,1312)):"H42RWIN",
    norm_edge((704,432),(704,608)):"H42BRIK",    # chimney mass
    norm_edge((-640,320),(-384,320)):"H42LWIN",
    norm_edge((1260,320),(1516,320)):"H42LWIN",
}

HOUSE_STYLES={"ENTRY","HALL","LOUNGE","BED","BEDWOOD","BATH","KITCH","LAUNDRY","SUNROOM"}
DETAIL_STYLES={"DOOR","BACKDOOR","IDOOR","GATEDOOR","FURNWOOD","FURNFAB","FIXWHITE","FIXPINK","APPLI","POST","PLAYEQ"}

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
    if x1==x2==-1652:
        lo,hi=sorted((y1,y2))
        if -930 <= lo and hi <= -830:
            return "H42GATE"
    if y1==y2:
        y=y1; lo,hi=sorted((x1,x2))
        if y==2944 and 16 <= lo and hi <= 960:
            return "H42FENC"
        # front boundary is intentionally open at the pedestrian path/driveway;
        # do not create another artificial street wall here.
        # rear driveway gate: see-through iron, blocks shortcut to Hilux/front
        if y==1312 and 704 <= lo and hi <= 960:
            return "H42GATE"
        # narrow west side rear blocker
        if y==1312 and 16 <= lo and hi <= 96:
            return "H42FENC"
        # front and rear elevations deliberately differ
        if y in (320,384) and 96 <= lo and hi <= 704:
            return "H42FACA"
        if y==1312 and 96 <= lo and hi <= 704:
            return "H42REAR"
    if st=="BACKDOOR":
        return "H42RDR"
    if st=="DOOR":
        return "H42FRNT"
    if _is_house_exterior(p1,p2,st):
        return "H42SIDN"
    return STYLE[st][5]

OUTDOOR_STYLES={"PORCH","DRIVE","CARPORT","AWNING","YARD","YARDLIT","PATIO","FOOT","VERGE","ROAD","STLIT","RESERVE","PLAY","PLAYLIT","LOT","GARDEN","DIG"}

def _solid_boundary(p1,p2,st0,st1):
    pair={st0,st1}
    (x1,y1),(x2,y2)=p1,p2
    # Real property fences are blocking two-sided midtextures, not full-height void walls.
    if x1==x2 and x1 in (16,960):
        lo,hi=sorted((y1,y2))
        if 16 <= lo and hi <= 2944:
            return True
    if y1==y2==2944:
        lo,hi=sorted((x1,x2))
        if 16 <= lo and hi <= 960:
            return True

    # no side escape from backyard: timber blocker west, see-through iron gate east
    if y1==y2==1312:
        lo,hi=sorted((x1,x2))
        if (16 <= lo and hi <= 96) or (704 <= lo and hi <= 960):
            return True
    if (st0 in HOUSE_STYLES and st1 in OUTDOOR_STYLES) or (st1 in HOUSE_STYLES and st0 in OUTDOOR_STYLES):
        return True
    # shed/garage is solid except its south-facing backyard doorway
    if "SHED" in pair and (st0 in OUTDOOR_STYLES or st1 in OUTDOOR_STYLES):
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
    xs.update((96,128,144,288,320,336,352,384,400,416,432,448,464,512,544,560,576,608,656,672,704,736,928,1260,1516,-640,-384,-2240,-1880,-1700,-1652,-1620,-1540))
    ys.update((320,352,368,384,512,528,544,576,640,704,736,792,856,928,944,960,976,992,1024,1040,1088,1104,1136,1152,1168,1184,1296,1312,1344,1750,2350,-1030,-960,-832,-820,-760,-704,-700,-608,-580,-300,-256,-96,0))
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

    # MAP01 ends only after Dad actually enters the playground shown in the
    # supplied satellite view, not at the house/front boundary.
    EXIT=norm_edge((-1700,-930),(-1700,-830))

    def add_boundary(p1,p2,sec0,sec1=None,st0=None,st1=None):
        key=norm_edge(p1,p2)
        if sec1 is None:
            wall=_boundary_texture(p1,p2,st0)
            if _segment_inside(key,EXIT):
                # Padlocked playground gate: red key opens it; crossing the far side
                # is handled by a separate small exit trigger sector.
                linedefs.append((vid(*p1),vid(*p2),1,28,0,side(sec0,middle="H42GATE"),0xFFFF))
            else:
                linedefs.append((vid(*p1),vid(*p2),1,0,0,side(sec0,middle=wall),0xFFFF))
        else:
            w0=STYLE[st0][5]; w1=STYLE[st1][5]
            if key==EXIT:
                # Crossing this line after the red-key gate opens ends MAP01.
                linedefs.append((vid(*p1),vid(*p2),4,11,0,
                                 side(sec0,upper=STYLE[st0][5],lower=STYLE[st0][5]),
                                 side(sec1,upper=STYLE[st1][5],lower=STYLE[st1][5])))
            elif st0 in ("DOOR","BACKDOOR","GATEDOOR","IDOOR") or st1 in ("DOOR","BACKDOOR","GATEDOOR","IDOOR"):
                door_style = st1 if st1 in ("DOOR","BACKDOOR","GATEDOOR","IDOOR") else st0
                dtex = "H42FRNT" if door_style=="DOOR" else ("H42RDR" if door_style=="BACKDOOR" else ("H42GATE" if door_style=="GATEDOOR" else "H42DOOR"))
                special = 27 if door_style=="DOOR" else (26 if door_style=="BACKDOOR" else (28 if door_style=="GATEDOOR" else 1))
                if st1 == door_style:
                    linedefs.append((vid(*p1),vid(*p2),4,special,0,
                                     side(sec0,upper=dtex,lower=dtex),
                                     side(sec1,upper=dtex,lower=dtex)))
                else:
                    linedefs.append((vid(*p2),vid(*p1),4,special,0,
                                     side(sec1,upper=dtex,lower=dtex),
                                     side(sec0,upper=dtex,lower=dtex)))
            elif _solid_boundary(p1,p2,st0,st1):
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
                special=11 if _segment_inside(key,EXIT) else 0
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
        (540,1500,270,1,7),          # Dad starts in backyard facing the real rear/sunroom
        (650,1260,270,15113,7),      # Sam is seen at rear door and escapes through house
        (444,356,270,15710,7),       # small front doorbell
        (842,2145,180,15740,7),      # spare back-door key tucked beside garage workbench/shelving
        (710,2060,180,15301,7),      # garage searchable cache nudges the player to search

        # house puzzle chain
        (220,1060,180,15741,7),      # Lincoln's phone in his bedroom
        (404,410,180,15742,7),       # note on inside of front door
        (602,880,180,15743,7),       # Sam's puzzle box in Sam's room
        # in-world keypad: 1 2 3 4 5 / 6 7 8 9 0
        (570,890,180,15751,7),(586,890,180,15752,7),(602,890,180,15753,7),
        (618,890,180,15754,7),(634,890,180,15755,7),
        (570,908,180,15756,7),(586,908,180,15757,7),(602,908,180,15758,7),
        (618,908,180,15759,7),(634,908,180,15750,7),
        (660,900,180,15104,7),       # small Sam room note/detail
        (420,120,270,15101,7),       # footprints/front path
        (-980,-430,180,15106,7),     # false trail near Arnold/Collenso
        (-1595,-880,180,15744,7),    # Sam's note on approach side of locked playground gate
        (-610,230,180,15745,7),       # neighbour letterbox containing gate key
        (-1450,-650,180,15410,7),    # Mopoke glimpse at reserve edge

        # physical puzzle evidence: 2 scooters, 3 Xbox/TV setups, 3 eggs, projector countdown
        (640,1880,90,15760,7),(760,1880,90,15760,7),
        (500,690,180,15761,7),(575,690,180,15761,7),(640,690,180,15761,7),
        (480,1012,180,15762,7),
        (250,900,180,15763,7),

        # dog dug under rear fence
        (245,2860,180,15733,7),

        # street lamps/poles
        (120,-150,0,15720,7),
        (-620,-150,0,15720,7),
        (-1160,-560,90,15720,7),
        (-880,760,90,15720,7),
        (-1850,-620,0,15720,7),

        # trees around frontages/reserve
        (-650,180,90,15721,7),
        (270,-165,90,15734,7),
        (1460,180,90,15721,7),
        (180,-760,90,15734,7),
        (-1200,360,90,15721,7),
        (-1450,120,90,15734,7),
        (-1750,360,90,15721,7),
        (-2050,620,90,15734,7),
        (-1850,-620,90,15721,7),
        (-2140,-1120,90,15734,7),
        (-1510,-1080,90,15721,7),

        # vehicles: fixed multi-angle sprites; Workmate in 42 driveway
        (832,620,90,15729,7),
        (1050,-430,90,15722,7),
        (-520,-430,90,15723,7),
        (1660,190,90,15723,7),

        # kerbside bins for 42 + neighbours
        (780,-220,0,15730,7),
        (820,-220,0,15731,7),
        (860,-220,0,15728,7),
        (-340,40,0,15728,7),
        (1500,30,0,15728,7),
        (-760,-190,0,15728,7),
        (1710,-190,0,15731,7),

        # low planting
        (180,210,0,15732,7),
        (560,275,0,15732,7),
        (100,1450,0,15732,7),
        (-560,205,0,15732,7),
        (1410,210,0,15732,7),

        # playground furniture/equipment
        (-1710,-940,0,15724,7),
        (-2050,-980,0,15725,7),
        (-1920,-900,0,15726,7),
        (-1820,-830,0,15727,7),
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
