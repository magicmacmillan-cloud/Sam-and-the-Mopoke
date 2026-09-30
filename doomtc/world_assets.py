from pathlib import Path
import math, random, struct, wave, zlib

def _png(path,w,h,pix,offx=None,offy=None):
    raw=b"".join(b"\0"+bytes(pix[y*w*4:(y+1)*w*4]) for y in range(h))
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))
    if offx is not None and offy is not None:
        data+=ch(b"grAb",struct.pack(">ii",int(offx),int(offy)))
    data+=ch(b"IDAT",zlib.compress(raw,9))+ch(b"IEND",b"")
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)

def _canvas(w,h): return [0]*(w*h*4)
def _disc(p,w,h,cx,cy,rx,ry,c,a=255):
    for y in range(max(0,int(cy-ry)),min(h,int(cy+ry+1))):
        for x in range(max(0,int(cx-rx)),min(w,int(cx+rx+1))):
            if ((x-cx)/max(1,rx))**2+((y-cy)/max(1,ry))**2<=1:
                i=(y*w+x)*4; p[i:i+4]=[*c,a]
def _rect(p,w,h,x0,y0,x1,y1,c,a=255):
    for y in range(max(0,int(y0)),min(h,int(y1))):
        for x in range(max(0,int(x0)),min(w,int(x1))):
            i=(y*w+x)*4;p[i:i+4]=[*c,a]
def _line(p,w,h,x0,y0,x1,y1,t,c,a=255):
    n=max(abs(int(x1-x0)),abs(int(y1-y0)),1)
    for i in range(n+1):
        q=i/n; _disc(p,w,h,int(x0+(x1-x0)*q),int(y0+(y1-y0)*q),t,t,c,a)

def _texture(root,name,base,w=128,h=128,pattern="noise"):
    p=[]
    for y in range(h):
        for x in range(w):
            n=((x*17+y*31)%23)-11
            c=[max(0,min(255,v+n)) for v in base]
            if pattern=="brick" and (y%32<2 or ((x+(16 if (y//32)%2 else 0))%64)<2): c=[max(0,v-26) for v in c]
            elif pattern=="boards" and (x%24<2): c=[max(0,v-22) for v in c]
            elif pattern=="tiles" and (x%32<2 or y%32<2): c=[max(0,v-20) for v in c]
            p += [*c,255]
    _png(root/"textures"/f"{name}.png",w,h,p)

def _finger(root,name,animal):
    w=h=96;p=_canvas(w,h); bone=(151,137,112); dead=(91,75,62); nail=(54,45,39); blood=(102,27,25)
    _disc(p,w,h,48,55,12,30,dead);_disc(p,w,h,48,28,11,16,bone);_disc(p,w,h,48,14,8,7,nail)
    _disc(p,w,h,48,82,8,7,blood)
    if animal=="goat":
        _disc(p,w,h,37,30,5,15,bone);_disc(p,w,h,59,30,5,15,bone)
    elif animal=="crow":
        _disc(p,w,h,39,66,4,18,nail);_disc(p,w,h,57,66,4,18,nail)
    else:
        _disc(p,w,h,48,73,14,8,(124,103,91))
    _png(root/"sprites"/f"{name}A0.png",w,h,p,48,84)

def _prop(root,name,kind):
    w=h=64;p=_canvas(w,h)
    if kind=="note":
        _rect(p,w,h,13,9,52,56,(202,190,154));_line(p,w,h,20,20,45,20,1,(70,61,54));_line(p,w,h,20,29,42,29,1,(70,61,54));_line(p,w,h,20,38,46,38,1,(70,61,54))
    elif kind=="print":
        _disc(p,w,h,32,42,8,16,(72,57,44)); 
        for x in (22,28,34,40): _disc(p,w,h,x,22,4,7,(72,57,44))
    elif kind=="loot":
        _rect(p,w,h,10,25,54,55,(77,65,52));_rect(p,w,h,15,19,49,30,(103,83,59));_disc(p,w,h,32,38,5,5,(190,150,53))
    elif kind=="survivor":
        _disc(p,w,h,32,15,8,9,(154,129,104));_rect(p,w,h,22,25,43,50,(72,74,70));_line(p,w,h,25,48,18,61,4,(74,67,61));_line(p,w,h,40,48,48,61,4,(74,67,61))
    elif kind=="echo":
        _disc(p,w,h,32,28,10,14,(120,141,161),120);_rect(p,w,h,24,40,40,58,(84,104,126),100)
    else:
        _rect(p,w,h,15,15,49,49,(91,76,60));_disc(p,w,h,32,32,7,7,(180,140,48))
    _png(root/"sprites"/f"{name}A0.png",w,h,p,32,58)

def _creature(root,prefix,kind):
    w=h=96
    for i,fr in enumerate("ABCDEFGH"):
        p=_canvas(w,h); bob=(0,-2,0,2,1,-1,0,1)[i]; stride=(-8,-4,1,8,7,2,-5,-8)[i]
        if kind=="zombie":
            skin=(75,96,72); cloth=(61,55,52); _disc(p,w,h,48,21+bob,11,12,skin);_disc(p,w,h,48,49+bob,15,22,cloth)
            _line(p,w,h,42,64+bob,40+stride,91,5,cloth);_line(p,w,h,54,64+bob,56-stride,91,5,cloth)
            _disc(p,w,h,43,19+bob,2,2,(204,197,150));_disc(p,w,h,53,19+bob,2,2,(204,197,150))
        else:
            fur=(78,73,65);bone=(157,146,126);_disc(p,w,h,48,51+bob,24,14,fur);_disc(p,w,h,68,39+bob,11,10,fur)
            _line(p,w,h,37,58+bob,36+stride//2,90,4,fur);_line(p,w,h,57,58+bob,58-stride//2,90,4,fur)
            _line(p,w,h,63,32+bob,59,13+bob,3,bone);_line(p,w,h,73,32+bob,78,13+bob,3,bone)
        _png(root/"sprites"/f"{prefix}{fr}0.png",w,h,p,48,91)

def _wav(root,name,freq,dur=.3,noise=.15):
    rate=22050; random.seed(name); vals=[]
    for i in range(int(rate*dur)):
        env=max(0,1-i/(rate*dur));v=math.sin(2*math.pi*freq*i/rate)*.5+random.uniform(-noise,noise)
        vals.append(int(max(-1,min(1,v*env))*14000))
    path=root/"sounds"/name;path.parent.mkdir(parents=True,exist_ok=True)
    with wave.open(str(path),"wb") as w:
        w.setparams((1,2,rate,len(vals),"NONE",""));w.writeframes(struct.pack("<"+"h"*len(vals),*vals))

def _midi(root):
    trk=bytearray(b"\x00\xc0\x30")
    for note in [45,48,52,43,47,50,41,45,48]:
        trk+=b"\x00\x90"+bytes([note,38])+b"\x83\x60\x80"+bytes([note,0])
    trk+=b"\x00\xff\x2f\x00"
    data=b"MThd"+struct.pack(">IHHH",6,0,1,480)+b"MTrk"+struct.pack(">I",len(trk))+trk
    (root/"music").mkdir(parents=True,exist_ok=True);(root/"music"/"sam-mopoke.mid").write_bytes(data)

def generate_world_assets(root: Path):
    root=Path(root)
    # Distinct material zones so each chapter reads immediately in Doom's 2.5D space.
    for name,base,pat in [
        ("HOUSE",(129,98,78),"boards"),("PLAYGRND",(105,86,69),"noise"),("FOREST",(57,78,60),"noise"),
        ("GRAVE",(91,94,90),"brick"),("TOMB",(101,91,78),"brick"),("STATION",(83,88,94),"tiles"),
        ("MALL",(104,94,90),"tiles"),("LIBRARY",(79,61,48),"boards"),("SHED",(86,73,61),"boards")]:
        _texture(root,name,base,pattern=pat)
    # Extra domestic texture identities: timber kitchen, pink bath, corrugated shed.
    _texture(root,"KITCHEN",(133,91,58),pattern="boards");_texture(root,"PINKBATH",(157,111,118),pattern="tiles");_texture(root,"CORRUG",(88,91,94),pattern="boards")
    for name,base in [("MOPFLR",(61,60,57)),("MOPCEI",(43,46,50))]:
        w=h=64;p=[]
        for y in range(h):
            for x in range(w):
                n=((x*11+y*7)%15)-7;p += [base[0]+n,base[1]+n,base[2]+n,255]
        _png(root/"flats"/f"{name}.png",w,h,p)
    # Finger keys and physical gate silhouettes.
    _finger(root,"GTFG","goat");_finger(root,"CRFG","crow");_finger(root,"PSFG","possum")
    for n,k in [("SMCL","note"),("SMFP","print"),("SMNT","note"),("SMSG","note"),("FMSG","note"),("LNTE","note"),("LOOT","loot"),("SURV","survivor"),("LNEC","echo")]:
        _prop(root,n,k)
    # Required extra print animation frames.
    for fr in "BCD": 
        src=(root/"sprites"/"SMFPA0.png").read_bytes();(root/"sprites"/f"SMFP{fr}0.png").write_bytes(src)
    _creature(root,"MZOM","zombie");_creature(root,"GOAT","goat")
    # Original title/intermission and night sky.
    w,h=320,200;p=[]
    for y in range(h):
        for x in range(w):
            fog=int(9+25*(1-y/h));moon=62 if (x-245)**2+(y-45)**2<25**2 else 0;p += [fog+moon,fog+moon,fog+moon+8,255]
    _png(root/"graphics"/"TITLEPIC.png",w,h,p);_png(root/"graphics"/"INTERPIC.png",w,h,p)
    w,h=256,128;p=[];random.seed(42);stars={(random.randrange(w),random.randrange(h//2)) for _ in range(90)}
    for y in range(h):
        for x in range(w):
            c=(150,160,170) if (x,y) in stars else (max(5,18-y//12),max(7,20-y//12),max(12,25-y//12));p += [*c,255]
    _png(root/"textures"/"MOPSKY.png",w,h,p)
    # Lightweight original soundscape; no commercial Doom audio.
    for n,f,d,no in [
        ("punch.wav",75,.12,.16),("scratch.wav",180,.18,.20),("door.wav",55,.35,.18),("pickup.wav",620,.12,.08),("secret.wav",880,.35,.10),
        ("goat1.wav",115,.55,.24),("goat2.wav",92,.62,.25),("zombie1.wav",72,.5,.25),("zombie2.wav",64,.6,.28),
        ("survivor.wav",145,.8,.12),("loot.wav",500,.15,.10),("step1.wav",92,.10,.10),("step2.wav",78,.11,.12),
        ("rain.wav",44,1.8,.65),("wind.wav",38,2.2,.38),("forest.wav",52,2.0,.28),("station.wav",46,1.8,.24),
        ("mallhum.wav",55,1.8,.12),("whisper1.wav",190,.75,.28),("whisper2.wav",145,.9,.30),("mopokecry.wav",68,1.15,.34),
        ("stafffire.wav",330,.22,.20),("cursefire.wav",245,.28,.25),("gauntlet.wav",62,.55,.40),("jandal.wav",105,.16,.18),
        ("hitflesh.wav",84,.14,.28),("key.wav",720,.20,.08),("samfar.wav",210,.65,.12),("heartbeat.wav",48,.48,.06)
    ]: _wav(root,n,f,d,no)
    _midi(root)
    print("Generated Sam and the Mopoke world textures, keys, clues, monsters, ambience and music")


# --- Full environment + monster-art polish pass ---
def _flat_material(root,name,base,kind):
    w=h=64;p=[]
    for y in range(h):
        for x in range(w):
            n=((x*13+y*17)%13)-6
            c=[max(0,min(255,v+n)) for v in base]
            if kind=="carpet" and ((x+y)%9==0): c=[max(0,v-10) for v in c]
            elif kind=="tile" and (x%16<1 or y%16<1): c=[max(0,v-30) for v in c]
            elif kind=="wood" and (x%16<2): c=[max(0,v-24) for v in c]
            elif kind=="dirt" and ((x*7+y*11)%29<3): c=[max(0,v-18) for v in c]
            elif kind=="stone" and (x%32<2 or y%24<2): c=[max(0,v-22) for v in c]
            elif kind=="concrete" and ((x*5+y*3)%37==0): c=[max(0,v-20) for v in c]
            p += [*c,255]
    _png(root/"flats"/f"{name}.png",w,h,p)

def _wall_polish(root,name,base,style):
    w=h=128;p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            n=((x*19+y*23)%17)-8
            c=[max(0,min(255,v+n)) for v in base]
            # Material grammar.
            if style=="plaster":
                if y in (94,95): c=[max(0,v-35) for v in c]
                if x%64==0: c=[max(0,v-8) for v in c]
            elif style=="panel":
                if x%24<2: c=[max(0,v-28) for v in c]
                if y in (96,97): c=[min(255,v+18) for v in c]
            elif style=="tile":
                if x%24<2 or y%24<2: c=[max(0,v-32) for v in c]
            elif style=="corrug":
                if x%12<3: c=[min(255,v+14) for v in c]
                elif x%12>9: c=[max(0,v-18) for v in c]
            elif style=="fence":
                if x%32<4 or y in (28,29,92,93): c=[max(0,v-38) for v in c]
            elif style=="bark":
                if x%21<4: c=[max(0,v-24) for v in c]
                if (x*3+y*5)%79<2: c=[max(0,v-30) for v in c]
            elif style=="masonry":
                if y%24<2 or ((x+(16 if (y//24)%2 else 0))%48)<2: c=[max(0,v-34) for v in c]
            elif style=="concrete":
                if y in (31,63,95): c=[max(0,v-15) for v in c]
            elif style=="shop":
                if y in (18,19,92,93): c=[min(255,v+18) for v in c]
                if x%64<3: c=[max(0,v-26) for v in c]
            elif style=="shelves":
                if y%28<4 or x%40<3: c=[max(0,v-34) for v in c]
            i=(y*w+x)*4;p[i:i+4]=[*c,255]
    # Baked grime/cracks/trims so walls do not read as flat colour swaps.
    grime=(42,38,35)
    for k in range(8):
        x=9+k*17; y=18+(k*29)%90
        _line(p,w,h,x,y,x+8,y+10,1,grime)
        if k%2==0:_line(p,w,h,x+8,y+10,x+4,y+19,1,grime)
    if name in ("STATION","MALL","LIBRARY"):
        _rect(p,w,h,8,8,58,20,(45,43,42))
        _rect(p,w,h,12,11,54,17,(156,145,118))
    _png(root/"textures"/f"{name}.png",w,h,p)

def _gate_sprite(root,name,metal):
    w=h=96;p=_canvas(w,h)
    stone=(87,82,74); dark=(39,37,35)
    _rect(p,w,h,8,5,88,94,stone)
    _rect(p,w,h,16,13,80,94,dark)
    for x in range(20,80,12): _rect(p,w,h,x,15,x+5,92,metal)
    _disc(p,w,h,48,48,10,15,(116,83,59))
    _disc(p,w,h,48,48,5,10,(28,23,20))
    _png(root/"sprites"/f"{name}A0.png",w,h,p,48,92)

def _extra_creature(root,prefix,kind):
    w=h=96
    for i,fr in enumerate("ABCDEFGH"):
        p=_canvas(w,h); bob=(0,-2,0,2,1,-1,0,1)[i]; step=(-7,-3,2,8,6,2,-4,-8)[i]
        if kind=="possum":
            fur=(101,94,89); pale=(178,153,145); tail=(154,119,113)
            _disc(p,w,h,45,55+bob,23,12,fur);_disc(p,w,h,65,47+bob,9,8,pale)
            _line(p,w,h,24,58+bob,8,47+bob+step//2,4,tail)
            _line(p,w,h,38,64+bob,36+step,87,3,fur);_line(p,w,h,55,64+bob,57-step,87,3,fur)
            _disc(p,w,h,69,45+bob,2,2,(219,156,61))
        elif kind=="crow":
            feather=(25,27,31); eye=(221,151,54); spread=(2,6,11,16,12,8,4,1)[i]
            _disc(p,w,h,48,45+bob,13,20,feather);_disc(p,w,h,48,25+bob,9,9,feather)
            _line(p,w,h,40,42+bob,20-spread,60+bob,5,feather);_line(p,w,h,56,42+bob,76+spread,60+bob,5,feather)
            _line(p,w,h,48,30+bob,61,33+bob,3,(90,74,52));_disc(p,w,h,44,23+bob,2,2,eye)
        elif kind=="husk":
            skin=(95,105,93); coat=(62,67,71); glow=(206,132,65)
            _disc(p,w,h,48,20+bob,11,12,skin);_rect(p,w,h,34,33+bob,62,67+bob,coat)
            _line(p,w,h,39,64+bob,37+step,92,5,coat);_line(p,w,h,57,64+bob,59-step,92,5,coat)
            _disc(p,w,h,43,18+bob,2,2,glow);_disc(p,w,h,53,18+bob,2,2,glow)
            _disc(p,w,h,66,48+bob,5,5,glow)
        elif kind=="brute":
            skin=(91,101,78); cloth=(67,52,49); wound=(105,29,27)
            _disc(p,w,h,48,19+bob,13,13,skin);_disc(p,w,h,48,53+bob,24,27,cloth)
            _line(p,w,h,32,46+bob,17+step//2,76,7,skin);_line(p,w,h,64,46+bob,79-step//2,76,7,skin)
            _line(p,w,h,40,72+bob,37+step,94,7,cloth);_line(p,w,h,57,72+bob,60-step,94,7,cloth)
            _disc(p,w,h,62,42+bob,5,5,wound)
        else:
            body=(34,35,42); edge=(96,94,111); eye=(200,190,165)
            _disc(p,w,h,48,25+bob,10,11,edge,175);_disc(p,w,h,48,54+bob,16,29,body,185)
            _line(p,w,h,36,48+bob,24-step//2,79,5,body);_line(p,w,h,60,48+bob,72+step//2,79,5,body)
            _disc(p,w,h,43,23+bob,2,2,eye,220);_disc(p,w,h,53,23+bob,2,2,eye,220)
        _png(root/"sprites"/f"{prefix}{fr}0.png",w,h,p,48,92)

_base_world_assets = generate_world_assets
def generate_world_assets(root: Path):
    root=Path(root)
    _base_world_assets(root)

    # Wall identities, with baked trim/grime/signage details.
    for spec in [
      ("HOUSE",(129,105,92),"plaster"),("KITCHEN",(132,88,55),"panel"),
      ("PINKBATH",(155,111,119),"tile"),("CORRUG",(88,92,96),"corrug"),
      ("PLAYGRND",(91,81,67),"fence"),("FOREST",(57,74,55),"bark"),
      ("GRAVE",(91,93,88),"masonry"),("TOMB",(103,91,76),"masonry"),
      ("STATION",(83,87,91),"concrete"),("MALL",(108,98,92),"shop"),
      ("LIBRARY",(78,59,47),"shelves")
    ]:_wall_polish(root,*spec)

    # Separate floor and roof/ceiling materials.
    for spec in [
      ("HCARPET",(82,70,62),"carpet"),("KTILE",(124,111,91),"tile"),
      ("PBATH",(156,126,130),"tile"),("GRASS",(56,75,50),"dirt"),
      ("DIRT",(73,61,48),"dirt"),("GRAVEFL",(76,72,65),"stone"),
      ("TOMBFL",(85,74,61),"stone"),("STNFLR",(78,81,84),"concrete"),
      ("MALLFLR",(113,105,99),"tile"),("LIBFLR",(65,52,44),"wood"),
      ("HCEIL",(111,106,98),"concrete"),("TOMBCE",(70,62,54),"stone"),
      ("STNCEIL",(63,67,71),"concrete"),("MALLCEIL",(93,89,84),"tile"),
      ("LIBCEIL",(58,48,42),"wood")
    ]:_flat_material(root,*spec)

    _gate_sprite(root,"GTGT",(104,93,73))
    _gate_sprite(root,"CRGT",(62,64,68))
    _gate_sprite(root,"PSGT",(112,79,62))

    for prefix,kind in [
      ("ROTP","possum"),("CROW","crow"),("HUSK","husk"),
      ("BRUT","brute"),("SHAD","shade")
    ]:_extra_creature(root,prefix,kind)

    print("Generated distinct walls, floors, ceilings, gates and expanded monster sprites")
