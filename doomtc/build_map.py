from pathlib import Path
import struct

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"sam-and-the-mopoke-map.wad"

def lump(name,data=b""):
    return name.encode("ascii")[:8].ljust(8,b"\0"),data

def tex8(s):
    return s.encode("ascii")[:8].ljust(8,b"\0")

# Continuous Doom-II-style route:
# House -> playground -> forest -> cemetery -> tomb -> station -> mall -> library.
# Floors, ceilings, lighting and wall materials are genuinely different sectors.
zones=[
 (-512, 480,   0,128,"HCARPET","HCEIL",   176,"HOUSE"),
 ( 480, 800,   0,128,"KTILE",  "HCEIL",   184,"KITCHEN"),
 ( 800,1344,   0,128,"PBATH",  "HCEIL",   168,"PINKBATH"),
 (1344,2432,  -8,256,"GRASS",  "F_SKY1",  176,"PLAYGRND"),
 (2432,3520, -16,320,"DIRT",   "F_SKY1",  136,"FOREST"),
 (3520,4256,  -8,256,"GRAVEFL","F_SKY1",  144,"GRAVE"),
 (4256,4544, -24,112,"TOMBFL", "TOMBCE",    96,"TOMB"),
 (4544,5952,   0,176,"STNFLR", "STNCEIL",  148,"STATION"),
 (5952,7488,   8,208,"MALLFLR","MALLCEIL", 180,"MALL"),
 (7488,8320,  -8,152,"LIBFLR", "LIBCEIL",  112,"LIBRARY"),
]

verts=[]
vmap={}
def vid(x,y):
    key=(int(x),int(y))
    if key not in vmap:
        vmap[key]=len(verts)
        verts.append(key)
    return vmap[key]

sidedefs=[]
linedefs=[]
sectors=[(fz,cz,tex8(ff),tex8(cf),light,0,0) for _,_,fz,cz,ff,cf,light,_ in zones]

def side(sector,upper="-",lower="-",middle="-"):
    i=len(sidedefs)
    sidedefs.append((0,0,tex8(upper),tex8(lower),tex8(middle),sector))
    return i

def line(x1,y1,x2,y2,flags,s0,s1=0xFFFF,special=0,tag=0):
    linedefs.append((vid(x1,y1),vid(x2,y2),flags,special,tag,s0,s1))

Y0,Y1=-768,768

# North/south exterior walls for every material zone.
for s,(x0,x1,fz,cz,ff,cf,light,walltex) in enumerate(zones):
    line(x0,Y1,x1,Y1,1,side(s,middle=walltex))
    line(x1,Y0,x0,Y0,1,side(s,middle=walltex))

line(zones[0][0],Y0,zones[0][0],Y1,1,side(0,middle=zones[0][7]))
last=len(zones)-1
line(zones[-1][1],Y1,zones[-1][1],Y0,1,side(last,middle=zones[-1][7]))

# Zone transitions have a readable doorway rather than turning the route into one corridor.
for s in range(len(zones)-1):
    x=zones[s][1]
    lefttex=zones[s][7]
    righttex=zones[s+1][7]
    for ya,yb,blocked in ((Y0,-112,True),(-112,112,False),(112,Y1,True)):
        rs=side(s+1,upper=righttex,lower=righttex,middle=righttex if blocked else "-")
        ls=side(s,upper=lefttex,lower=lefttex,middle=lefttex if blocked else "-")
        line(x,ya,x,yb,4 | (1 if blocked else 0),rs,ls)

def barrier(x1,y1,x2,y2,sector,tex):
    # Two-sided blocking midtexture: visible from both directions, no phantom hidden wall.
    a=side(sector,middle=tex)
    b=side(sector,middle=tex)
    line(x1,y1,x2,y2,5,a,b)

# House: bedrooms/hall, timber kitchen, pink bathroom, enclosed porch/carport/shed.
for w in [
 (-120,-360,-120,-80),(160,80,160,360),(350,-360,350,-80),
 (520,90,520,360),(700,-360,700,-100),(930,100,930,360),
 (1080,-300,1280,-300),(1110,180,1280,180)
]:
    sec=0 if w[0] < 480 else (1 if w[0] < 800 else 2)
    barrier(*w,sec,"HOUSE")
barrier(560,-120,760,-120,1,"KITCHEN")
barrier(860,-100,1030,-100,2,"PINKBATH")
barrier(1130,300,1290,300,2,"CORRUG")

# Playground: exposed pursuit, equipment and fence sightline breaks.
for w in [(1500,-430,1500,-80),(1760,120,1990,120),(2140,-380,2310,-380),(1880,-520,2050,-520)]:
    barrier(*w,3,"PLAYGRND")

# Forest: deadfall, forked lanes, false trails and return sightlines.
for w in [
 (2520,-560,2730,-310),(2860,270,3060,520),(3160,-570,3400,-310),
 (3280,230,3460,460),(2580,50,2810,50),(2980,-150,3230,-150),
 (2700,430,2890,590),(3090,360,3220,590)
]:
    barrier(*w,4,"FOREST")
barrier(3400,Y0,3400,-54,4,"FOREST")
barrier(3400,54,3400,Y1,4,"FOREST")

# Cemetery: grave-row lanes and mausoleum pockets.
for w in [
 (3580,-460,3820,-460),(3580,-130,3770,-130),(3860,150,4110,150),
 (3970,440,4190,440),(3650,310,3830,310),(4020,-310,4200,-310),
 (3720,-620,3720,-500),(3920,-620,3920,-500)
]:
    barrier(*w,5,"GRAVE")

# Tomb: compressed sandstone chambers and Crow Finger choke.
for w in [(4300,-460,4490,-460),(4300,-90,4440,-90),(4380,250,4520,250)]:
    barrier(*w,6,"TOMB")
barrier(4480,Y0,4480,-50,6,"TOMB")
barrier(4480,50,4480,Y1,6,"TOMB")

# Station: platform, service tunnel, maintenance cross-lanes.
for w in [
 (4620,-320,5010,-320),(5120,280,5500,280),(5580,-390,5880,-390),
 (5700,110,5920,110),(4760,90,4990,90),(5300,-140,5500,-140),
 (5650,380,5890,380),(4900,520,5350,520)
]:
    barrier(*w,7,"STATION")

# Mall: shopfront cover, kiosks/loading lane and largest sustained fight.
for w in [
 (6060,-510,6440,-510),(6200,130,6480,130),(6540,-590,6540,-190),
 (6700,280,7110,280),(7160,-450,7420,-450),(6120,390,6400,390),
 (6640,-330,6900,-330),(7040,520,7330,520),(6820,520,6820,720)
]:
    barrier(*w,8,"MALL")
barrier(7350,Y0,7350,-52,8,"MALL")
barrier(7350,52,7350,Y1,8,"MALL")

# Library: alternating stacks, deceptive returns and archive cage.
for w in [
 (7560,-680,7560,-190),(7770,130,7770,680),(7980,-680,7980,-130),
 (8180,180,8180,680),(7680,-50,7900,-50),(8050,50,8270,50),
 (7520,-510,7730,-510),(7840,440,8050,440),(8120,-440,8290,-440),
 (7860,-250,8060,-250)
]:
    barrier(*w,9,"LIBRARY")

things=[
 (-320,0,0,1,7),

 # Domestic opening / Sam pursuit.
 (620,0,0,15103,7),(850,80,0,15101,7),(1100,-80,0,15104,7),
 (1420,120,0,15105,7),(1580,-120,0,15106,7),(1750,220,0,15301,7),

 # Forest: new fast wildlife, clues, survivor and Goat Finger before gate.
 (1900,-180,0,15401,7),(2200,220,0,15401,7),(2380,120,0,15107,7),
 (2480,-180,0,15402,7),(2650,360,0,15403,7),(2780,-420,0,15404,7),
 (2920,120,0,15108,7),(3050,180,0,15302,7),(3050,-300,0,15501,7),
 (3200,420,0,15403,7),(3400,0,0,15601,7),

 # Cemetery/tomb.
 (3480,-180,0,15301,7),(3650,0,0,15402,7),(3720,120,0,15301,7),
 (3740,-220,0,15502,7),(3860,-430,0,15404,7),(4050,160,0,15109,7),
 (4100,200,0,15401,7),(4160,-360,0,15403,7),(4230,-180,0,15402,7),
 (4360,180,0,15401,7),(4480,0,0,15602,7),

 # Station action spike.
 (4550,0,0,15110,7),(4680,180,0,15402,7),(4780,-180,0,15301,7),
 (4900,320,0,15405,7),(4980,-280,0,15401,7),(5100,240,0,15402,7),
 (5220,-220,0,15401,7),(5250,180,0,15110,7),(5360,250,0,15405,7),
 (5480,-240,0,15401,7),(5600,220,0,15402,7),(5750,-180,0,15301,7),
 (5750,300,0,15503,7),

 # Mall sustained fight.
 (6100,-180,0,15109,7),(6250,200,0,15301,7),(6300,-40,0,15102,7),
 (6350,-220,0,15401,7),(6440,-520,0,15406,7),(6550,220,0,15402,7),
 (6750,-220,0,15401,7),(6830,40,0,15406,7),(6900,220,0,15403,7),
 (7060,-520,0,15404,7),(7150,300,0,15503,7),(7350,0,0,15603,7),

 # Library quiet-to-panic escalation.
 (7580,560,0,15407,7),(7760,-560,0,15407,7),(7960,520,0,15407,7),
 (8100,-300,0,15405,7),

 # Cursed weapon discoveries.
 (2050,0,0,15001,7),(3180,-350,0,15002,7),(3900,-250,0,15003,7),
 (4700,-120,0,15004,7),(5200,0,0,15005,7),(5800,0,0,15006,7),
 (6200,-300,0,15007,7),(6450,300,0,15008,7),(6700,420,0,15009,7),
 (6900,0,0,15010,7),(7150,300,0,15011,7),(7700,300,0,15012,7),
 (8000,300,0,15013,7),

 # Recovery caches after peaks.
 (2700,620,0,15301,7),(3300,-700,0,15301,7),(3800,560,0,15301,7),
 (4900,470,0,15301,7),(5650,-650,0,15301,7),(6400,650,0,15301,7),
 (7900,-700,0,15301,7),

 # Finale.
 (8180,0,180,15102,7)
]

L=[
 lump("SAMMPK",b"Sam and the Mopoke standalone Doom II game"),
 lump("MAP01"),
 lump("THINGS",b"".join(struct.pack("<hhhhh",*x) for x in things)),
 lump("LINEDEFS",b"".join(struct.pack("<HHHHHHH",*x) for x in linedefs)),
 lump("SIDEDEFS",b"".join(struct.pack("<hh8s8s8sH",*x) for x in sidedefs)),
 lump("VERTEXES",b"".join(struct.pack("<hh",*x) for x in verts)),
 lump("SEGS"),lump("SSECTORS"),lump("NODES"),
 lump("SECTORS",b"".join(struct.pack("<hh8s8shhh",*x) for x in sectors)),
 lump("REJECT"),lump("BLOCKMAP")
]

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
print(f"{OUT} sectors={len(sectors)} linedefs={len(linedefs)} things={len(things)}")
