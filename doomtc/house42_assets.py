from pathlib import Path
import math, random

from world_assets import _png, _canvas, _rect, _line, _disc, _wav

# Source-matched domestic material pass for MAP01.
# This does not pretend to be a survey/photo-scan. Colours, pattern scale and
# fixture vocabulary are tuned to the supplied 42 Arnold walkthrough/aerials:
# warm cream plaster, brown carpet, polished boards, timber kitchen, pink bath,
# cream weatherboards, dark tiled roof, brick chimney, concrete drive and shed.

def _clamp(v):
    return max(0, min(255, int(v)))

def _shade(base, n):
    return tuple(_clamp(v+n) for v in base)

def _set(p,w,h,x,y,c,a=255):
    if 0 <= x < w and 0 <= y < h:
        i=(y*w+x)*4
        p[i:i+4]=[*c,a]

def _noise(base,x,y,amp=8,seed=0):
    n=((x*37+y*53+seed*97) % (amp*2+1))-amp
    return _shade(base,n)

def _plaster(root,name,base=(210,204,190),grey=False):
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            c=_noise(base,x,y,5,11 if grey else 7)
            # Subtle roller texture and age patches.
            if ((x*7+y*11)%97)<2: c=_shade(c,-5)
            if y > 112: c=_shade(c,-8)
            _set(p,w,h,x,y,c)
    # Skirting board baked into the bottom of one wall-height repeat.
    _rect(p,w,h,0,114,w,128,(224,222,213))
    _line(p,w,h,0,113,w-1,113,1,(166,161,150))
    # Fine old-house hairline marks: restrained, not horror grime.
    for x,y in [(17,33),(91,49),(55,82)]:
        _line(p,w,h,x,y,x+5,y+8,1,(170,165,155),90)
    _png(root/"textures"/f"{name}.png",w,h,p)

def _panel(root):
    w=h=128; p=_canvas(w,h)
    base=(126,82,49)
    for y in range(h):
        for x in range(w):
            grain=((x*5+y*19)%17)-8
            c=_shade(base,grain)
            if x%22 in (0,1): c=_shade(c,-28)
            if x%22 in (20,21): c=_shade(c,12)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,0,112,w,128,(157,132,99))
    _line(p,w,h,0,111,w-1,111,1,(75,51,34))
    _png(root/"textures"/"H42PANL.png",w,h,p)

def _kitchen(root):
    # One 128-high wall repeat: cream upper wall/backsplash, brown marbled bench,
    # honey timber base cabinets with dark handles.
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            if y < 42:
                c=_noise((218,214,199),x,y,4,2)
                if x%24 in (0,1) or y%24 in (0,1): c=(190,186,176)
            elif y < 55:
                c=_noise((102,72,55),x,y,8,8)
                if ((x*3+y*7)%31)<3: c=_shade(c,20)
            else:
                c=_noise((142,92,52),x,y,8,12)
                if x%32 in (0,1): c=_shade(c,-24)
                if y in (91,92): c=_shade(c,-18)
            _set(p,w,h,x,y,c)
    for x in range(14,128,32):
        _rect(p,w,h,x,76,x+4,82,(47,42,35))
    _png(root/"textures"/"H42KTCH.png",w,h,p)

def _bath(root):
    w=h=128; p=_canvas(w,h)
    base=(190,154,159)
    for y in range(h):
        for x in range(w):
            c=_noise(base,x,y,4,5)
            if x%24 in (0,1) or y%24 in (0,1): c=(146,137,134)
            _set(p,w,h,x,y,c)
    # Period cream accent band visible in the bathroom.
    _rect(p,w,h,0,47,w,54,(221,210,190))
    _line(p,w,h,0,46,w-1,46,1,(133,121,116))
    _line(p,w,h,0,54,w-1,54,1,(133,121,116))
    _png(root/"textures"/"H42BATH.png",w,h,p)

def _siding(root):
    w=h=128; p=_canvas(w,h)
    cream=(214,211,194)
    for y in range(h):
        band=y%18
        for x in range(w):
            c=_noise(cream,x,y,4,9)
            if band in (0,1): c=_shade(c,-28)
            elif band in (2,3): c=_shade(c,8)
            _set(p,w,h,x,y,c)
    _png(root/"textures"/"H42SIDN.png",w,h,p)

def _brick(root):
    w=h=128; p=_canvas(w,h)
    mortar=(166,153,137)
    base=(142,73,48)
    for y in range(h):
        row=y//16
        shift=16 if row%2 else 0
        for x in range(w):
            if y%16 in (0,1) or (x+shift)%32 in (0,1):
                c=mortar
            else:
                c=_noise(base,x,y,12,row)
            _set(p,w,h,x,y,c)
    _png(root/"textures"/"H42BRIK.png",w,h,p)

def _corrug(root):
    w=h=128; p=_canvas(w,h)
    base=(127,130,128)
    for y in range(h):
        for x in range(w):
            phase=x%14
            add=15 if phase<3 else (-17 if phase>10 else 0)
            c=_shade(_noise(base,x,y,5,4),add)
            _set(p,w,h,x,y,c)
    _png(root/"textures"/"H42SHED.png",w,h,p)

def _fence(root):
    w=h=128; p=_canvas(w,h)
    base=(70,61,50)
    for y in range(h):
        for x in range(w):
            c=_noise(base,x,y,7,13)
            if x%24 in (0,1,2): c=_shade(c,-25)
            if y in (36,37,96,97): c=_shade(c,-22)
            _set(p,w,h,x,y,c)
    _png(root/"textures"/"H42FENC.png",w,h,p)

def _gate(root):
    w=h=128; p=_canvas(w,h)
    # Transparent black metal railing/gate for GZDoom midtextures.
    for x in range(8,128,20):
        _rect(p,w,h,x,4,x+4,124,(37,38,36),235)
        _disc(p,w,h,x+2,4,4,5,(37,38,36),235)
    _rect(p,w,h,0,32,w,37,(37,38,36),235)
    _rect(p,w,h,0,92,w,97,(37,38,36),235)
    _png(root/"textures"/"H42GATE.png",w,h,p)

def _window(root):
    w=h=128; p=_canvas(w,h)
    _rect(p,w,h,0,0,w,h,(218,216,203))
    _rect(p,w,h,7,7,121,121,(24,29,31))
    # Dark night reflection / curtains.
    for y in range(10,118):
        for x in range(10,118):
            c=_noise((31,37,39),x,y,5,17)
            if (x+y)%41==0: c=_shade(c,12)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,61,7,67,121,(205,203,192))
    _rect(p,w,h,7,61,121,67,(205,203,192))
    _png(root/"textures"/"H42WIND.png",w,h,p)

def _blinds(root):
    w=h=128; p=_canvas(w,h)
    for x in range(0,w,13):
        _rect(p,w,h,x,0,min(w,x+8),h,(218,215,204),230)
        _line(p,w,h,min(w-1,x+9),0,min(w-1,x+9),h-1,1,(145,143,137),220)
    _png(root/"textures"/"H42BLND.png",w,h,p)

def _door(root,name,wood=True):
    w=64; h=128; p=_canvas(w,h)
    base=(126,79,47) if wood else (211,208,198)
    for y in range(h):
        for x in range(w):
            c=_noise(base,x,y,6,21 if wood else 22)
            _set(p,w,h,x,y,c)
    edge=(69,47,33) if wood else (160,157,151)
    for y0,y1 in [(8,55),(70,118)]:
        _line(p,w,h,7,y0,57,y0,2,edge); _line(p,w,h,7,y1,57,y1,2,edge)
        _line(p,w,h,7,y0,7,y1,2,edge); _line(p,w,h,57,y0,57,y1,2,edge)
    _disc(p,w,h,52,63,3,3,(75,68,57))
    _png(root/"textures"/f"{name}.png",w,h,p)

def _curb(root):
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            c=_noise((154,151,143),x,y,7,25)
            if y in (28,29,95,96): c=_shade(c,-20)
            _set(p,w,h,x,y,c)
    _png(root/"textures"/"H42CURB.png",w,h,p)

def _neighbor(root,name,brick=False):
    if brick:
        _brick(root)
        # copy brick appearance under a neighbour-specific name
        src=(root/"textures"/"H42BRIK.png").read_bytes()
        (root/"textures"/f"{name}.png").write_bytes(src)
    else:
        _siding(root)
        src=(root/"textures"/"H42SIDN.png").read_bytes()
        (root/"textures"/f"{name}.png").write_bytes(src)

def _play(root):
    w=h=128; p=_canvas(w,h)
    base=(116,103,83)
    for y in range(h):
        for x in range(w):
            c=_noise(base,x,y,7,31)
            _set(p,w,h,x,y,c)
    # Simple safety-fence / play-equipment silhouettes.
    _rect(p,w,h,0,92,w,97,(62,61,58))
    for x in range(10,128,24): _rect(p,w,h,x,58,x+3,104,(62,61,58))
    _line(p,w,h,24,80,44,36,3,(118,53,40))
    _line(p,w,h,44,36,63,80,3,(118,53,40))
    _line(p,w,h,34,56,55,56,3,(118,53,40))
    _png(root/"textures"/"H42PLAY.png",w,h,p)

def _flat(root,name,base,kind):
    w=h=64; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            c=_noise(base,x,y,7,41)
            if kind=="carpet":
                if ((x*5+y*7)%19)<4: c=_shade(c,-11)
                if ((x*11+y*3)%29)<3: c=_shade(c,8)
            elif kind=="wood":
                if y%12 in (0,1): c=_shade(c,-24)
                if x%32 in (0,1): c=_shade(c,-8)
                if ((x*13+y*5)%43)<2: c=_shade(c,10)
            elif kind=="vinyl":
                # tan 70s/80s patterned lino
                if x%16 in (0,1) or y%16 in (0,1): c=_shade(c,-9)
                if (x//8+y//8)%2==0: c=_shade(c,4)
            elif kind=="tile":
                if x%16 in (0,1) or y%16 in (0,1): c=(139,136,128)
            elif kind=="concrete":
                if ((x*17+y*23)%67)<2: c=_shade(c,-22)
                if x in (31,32) or y in (31,32): c=_shade(c,-12)
            elif kind=="asphalt":
                if ((x*11+y*17)%23)<4: c=_shade(c,12)
            elif kind=="grass":
                if ((x*3+y*5)%17)<5: c=_shade(c,-9)
                if ((x*7+y*13)%41)<3: c=_shade(c,11)
            elif kind=="pave":
                if x%16 in (0,1) or y%12 in (0,1): c=_shade(c,-20)
            elif kind=="roof":
                if y%10 in (0,1): c=_shade(c,-20)
                if x%24 in (0,1): c=_shade(c,-8)
            _set(p,w,h,x,y,c)
    _png(root/"flats"/f"{name}.png",w,h,p)

def _prop_bin(root):
    w=64;h=96;p=_canvas(w,h)
    _rect(p,w,h,15,28,50,84,(62,78,59))
    _rect(p,w,h,11,22,54,32,(78,89,62))
    _disc(p,w,h,20,84,6,6,(28,29,27));_disc(p,w,h,45,84,6,6,(28,29,27))
    _png(root/"sprites"/"H4BNA0.png",w,h,p,32,88)

def _prop_bathroom(root):
    # Tiny reference sprites for the builder; not placed by default.
    for name,kind in [("H4TBA0","tub"),("H4WCA0","wc"),("H4BSA0","basin"),("H4WMA0","washer")]:
        w=h=64;p=_canvas(w,h)
        if kind=="tub":
            _rect(p,w,h,7,30,57,50,(218,204,195));_rect(p,w,h,10,33,54,45,(181,151,157))
        elif kind=="wc":
            _disc(p,w,h,32,38,13,10,(223,218,205));_rect(p,w,h,22,13,42,34,(220,215,203))
        elif kind=="basin":
            _disc(p,w,h,32,31,18,9,(224,218,205));_rect(p,w,h,28,38,36,59,(188,181,169))
        else:
            _rect(p,w,h,11,9,53,58,(218,216,209));_disc(p,w,h,32,35,14,14,(89,97,99));_disc(p,w,h,32,35,9,9,(44,52,55))
        _png(root/"sprites"/f"{name}.png",w,h,p,32,58)

def _atlas(root):
    names=[
      "H42WALL","H42GREY","H42PANL","H42KTCH","H42BATH","H42SIDN",
      "H42BRIK","H42SHED","H42FENC","H42GATE","H42WIND","H42BLND",
      "H42DOOR","H42WDR","H42CURB","H42NBR1","H42NBR2","H42PLAY"
    ]
    w,h=768,384; p=_canvas(w,h)
    # Dark neutral atlas background.
    _rect(p,w,h,0,0,w,h,(28,28,28))
    # We cannot decode the just-written PNGs without an image dependency, so render
    # simple labelled material swatches directly from the same palette grammar.
    swatches=[
      ((210,204,190),"WALL"),((188,188,184),"GREY"),((126,82,49),"PANEL"),
      ((142,92,52),"KITCH"),((190,154,159),"BATH"),((214,211,194),"SIDING"),
      ((142,73,48),"BRICK"),((127,130,128),"SHED"),((70,61,50),"FENCE"),
      ((37,38,36),"GATE"),((31,37,39),"WINDOW"),((218,215,204),"BLINDS"),
      ((126,79,47),"DOOR"),((211,208,198),"W-DOOR"),((154,151,143),"CURB"),
      ((214,211,194),"NBR-S"),((142,73,48),"NBR-B"),((116,103,83),"PLAY")
    ]
    for i,(col,lab) in enumerate(swatches):
        cx=(i%6)*128; cy=(i//6)*128
        _rect(p,w,h,cx+4,cy+4,cx+124,cy+108,col)
        # label ticks: enough to visually separate in a no-font generator.
        for j,ch in enumerate(lab[:10]):
            v=20+(ord(ch)%50)*3
            _rect(p,w,h,cx+7+j*10,cy+112,cx+13+j*10,cy+120,(v,v,v))
    _png(root/"graphics"/"H42ATLAS.png",w,h,p)


def _front_door(root):
    # Front reference: dark domestic front door beneath the cream porch.
    w=64; h=128; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            _set(p,w,h,x,y,_noise((62,55,49),x,y,4,52))
    for x0,y0,x1,y1 in ((8,8,56,48),(8,57,56,116)):
        _line(p,w,h,x0,y0,x1,y0,2,(34,31,29))
        _line(p,w,h,x0,y1,x1,y1,2,(34,31,29))
        _line(p,w,h,x0,y0,x0,y1,2,(34,31,29))
        _line(p,w,h,x1,y0,x1,y1,2,(34,31,29))
    _disc(p,w,h,52,64,3,3,(173,168,157))
    _png(root/"textures"/"H42FRNT.png",w,h,p)

def _sofa(root):
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            c=_noise((92,78,67),x,y,7,59)
            if x%32 in (0,1) or y%32 in (0,1): c=_shade(c,-10)
            _set(p,w,h,x,y,c)
    _png(root/"textures"/"H42SOFA.png",w,h,p)

def _appliance(root):
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            _set(p,w,h,x,y,_noise((204,201,191),x,y,3,61))
    _rect(p,w,h,10,12,118,116,(217,214,205))
    _rect(p,w,h,16,20,112,58,(85,90,91))
    _rect(p,w,h,101,68,107,108,(92,90,85))
    _png(root/"textures"/"H42APPL.png",w,h,p)


def _cola_sprite(root):
    # Small crushed red cola can, replacing the old paper-placeholder SMCL art.
    w=24; h=34; p=_canvas(w,h)
    _rect(p,w,h,7,5,18,29,(139,37,34))
    _rect(p,w,h,8,3,17,7,(172,166,153))
    _rect(p,w,h,8,27,17,31,(104,102,96))
    _line(p,w,h,8,9,17,24,2,(198,193,179))
    _line(p,w,h,17,9,8,24,1,(84,27,25))
    _disc(p,w,h,12,4,3,1,(76,76,73))
    _png(root/"sprites"/"SMCLA0.png",w,h,p,12,30)

def _doorbell_sprite(root):
    # Deliberately small: a believable wall button, not a pickup-sized prop.
    w=20; h=28; p=_canvas(w,h)
    _rect(p,w,h,5,3,15,25,(205,201,188))
    _rect(p,w,h,6,4,14,24,(154,151,141))
    _disc(p,w,h,10,11,3,3,(52,50,47))
    _disc(p,w,h,10,11,1,1,(191,185,169))
    _rect(p,w,h,8,18,12,21,(74,72,68))
    _png(root/"sprites"/"DBELA0.png",w,h,p,10,24)

def _environment_sprites(root):
    # Suburban street/park props matched to the satellite/front-reference context.
    # Kept deliberately chunky and Doom-readable rather than modern 3-D models.

    # Street lamp / utility-style pole.
    w,h=48,128; p=_canvas(w,h)
    _rect(p,w,h,22,24,27,124,(72,73,70))
    _rect(p,w,h,18,18,31,26,(91,92,87))
    _rect(p,w,h,14,12,35,20,(176,171,149))
    _disc(p,w,h,24,15,8,4,(226,215,169))
    _rect(p,w,h,19,123,30,127,(58,59,57))
    _png(root/"sprites"/"STLPA0.png",w,h,p,24,124)

    # Broad suburban tree with dark trunk and irregular canopy.
    w,h=96,128; p=_canvas(w,h)
    _rect(p,w,h,43,58,52,124,(78,57,40))
    _rect(p,w,h,35,76,45,84,(78,57,40))
    _rect(p,w,h,51,70,62,78,(78,57,40))
    for cx,cy,rx,ry,col in [
        (48,44,31,30,(48,74,43)),(27,50,22,24,(54,84,47)),
        (67,48,24,25,(42,69,40)),(46,25,22,20,(59,91,50)),
        (72,29,16,18,(51,80,45)),(21,30,15,17,(62,93,52))
    ]:
        _disc(p,w,h,cx,cy,rx,ry,col)
    _png(root/"sprites"/"TREEA0.png",w,h,p,48,124)

    def car(name,body,glass):
        w,h=112,56; p=_canvas(w,h)
        # wheels
        _disc(p,w,h,27,44,10,10,(27,28,28))
        _disc(p,w,h,85,44,10,10,(27,28,28))
        _disc(p,w,h,27,44,5,5,(112,112,108))
        _disc(p,w,h,85,44,5,5,(112,112,108))
        # body and roof
        _rect(p,w,h,8,25,104,44,body)
        _rect(p,w,h,28,13,82,30,body)
        _line(p,w,h,8,25,19,18,2,_shade(body,-15))
        _line(p,w,h,104,25,94,18,2,_shade(body,-15))
        # windows
        _rect(p,w,h,34,16,53,27,glass)
        _rect(p,w,h,58,16,77,27,glass)
        _rect(p,w,h,10,31,17,36,(225,218,181))
        _rect(p,w,h,95,31,103,36,(170,45,40))
        _line(p,w,h,9,44,103,44,2,_shade(body,-28))
        _png(root/"sprites"/f"{name}A0.png",w,h,p,56,48)
    car("CARW",(186,189,184),(58,67,72))
    car("CARD",(66,73,76),(33,40,44))

    # Park bench.
    w,h=80,64; p=_canvas(w,h)
    _rect(p,w,h,8,24,72,30,(104,71,44))
    _rect(p,w,h,8,35,72,41,(104,71,44))
    _rect(p,w,h,15,12,65,18,(112,75,45))
    _rect(p,w,h,15,18,19,55,(61,61,58))
    _rect(p,w,h,61,18,65,55,(61,61,58))
    _png(root/"sprites"/"BNCHA0.png",w,h,p,40,56)

    # Swing frame.
    w,h=96,96; p=_canvas(w,h)
    metal=(75,81,82)
    _line(p,w,h,12,88,28,15,4,metal)
    _line(p,w,h,84,88,68,15,4,metal)
    _line(p,w,h,26,15,70,15,4,metal)
    for x in (39,57):
        _line(p,w,h,x,18,x,60,1,(46,47,46))
        _line(p,w,h,x+8,18,x+8,60,1,(46,47,46))
        _rect(p,w,h,x,60,x+8,64,(121,71,44))
    _png(root/"sprites"/"SWNGA0.png",w,h,p,48,90)

    # Slide.
    w,h=96,80; p=_canvas(w,h)
    _rect(p,w,h,24,18,48,25,(149,62,46))
    _line(p,w,h,26,25,16,70,4,(72,78,79))
    _line(p,w,h,46,25,78,67,6,(169,80,52))
    _line(p,w,h,80,67,90,70,3,(169,80,52))
    _line(p,w,h,22,18,22,68,3,(72,78,79))
    _line(p,w,h,50,18,50,56,3,(72,78,79))
    _png(root/"sprites"/"SLIDA0.png",w,h,p,48,72)

    # Small climbing frame / platform.
    w,h=96,80; p=_canvas(w,h)
    metal=(74,82,83)
    for x in (18,38,58,78):
        _line(p,w,h,x,22,x,72,3,metal)
    _line(p,w,h,18,22,78,22,3,metal)
    _line(p,w,h,18,46,78,46,2,metal)
    _line(p,w,h,18,70,78,70,3,metal)
    _rect(p,w,h,30,28,66,36,(139,65,45))
    _png(root/"sprites"/"CLMBA0.png",w,h,p,48,72)

    # Green wheelie bin seen around the property/street.
    w,h=48,64; p=_canvas(w,h)
    _rect(p,w,h,11,16,37,54,(53,79,56))
    _rect(p,w,h,8,12,40,19,(69,92,64))
    _line(p,w,h,14,22,34,22,1,(39,60,43))
    _line(p,w,h,14,30,34,30,1,(39,60,43))
    _disc(p,w,h,15,56,5,5,(28,29,28))
    _disc(p,w,h,33,56,5,5,(28,29,28))
    _png(root/"sprites"/"WBINA0.png",w,h,p,24,58)

def _extra_street_details(root):
    # White Toyota Hilux Workmate-style single-cab tray ute.
    # Eight Doom rotations keep the ute oriented along the real driveway.
    body=(218,218,211); shadow=(151,153,150); dark=(42,48,50); tray=(157,160,157)
    tyre=(28,29,28); rim=(126,128,125)

    def wheel(p,w,h,cx,cy):
        _disc(p,w,h,cx,cy,8,8,tyre)
        _disc(p,w,h,cx,cy,3,3,rim)

    def hilux_view(rot):
        if rot in (1,5):  # front / rear
            w,h=78,62; p=_canvas(w,h)
            wheel(p,w,h,16,50); wheel(p,w,h,62,50)
            _rect(p,w,h,12,27,66,49,body if rot==1 else tray)
            if rot==1:
                _rect(p,w,h,20,16,58,31,body)
                _rect(p,w,h,24,18,54,29,dark)
                _rect(p,w,h,20,34,58,42,(71,74,72))
                _rect(p,w,h,14,31,20,36,(231,220,174))
                _rect(p,w,h,58,31,64,36,(231,220,174))
            else:
                _rect(p,w,h,18,23,60,34,tray)
                _line(p,w,h,18,24,60,24,2,(102,104,102))
                _rect(p,w,h,22,30,56,42,(139,141,138))
                _rect(p,w,h,14,36,21,41,(153,40,36))
                _rect(p,w,h,57,36,64,41,(153,40,36))
            return w,h,p

        if rot in (3,7):  # full side
            w,h=126,58; p=_canvas(w,h)
            wheel(p,w,h,31,47); wheel(p,w,h,96,47)
            left_to_right = rot==3
            if left_to_right:
                _rect(p,w,h,10,28,72,45,tray)
                _rect(p,w,h,72,21,111,45,body)
                _rect(p,w,h,81,12,108,30,body)
                _rect(p,w,h,84,15,105,28,dark)
                _line(p,w,h,11,27,70,27,2,(118,121,118))
                _rect(p,w,h,106,32,116,37,(231,220,174))
            else:
                _rect(p,w,h,54,28,116,45,tray)
                _rect(p,w,h,15,21,54,45,body)
                _rect(p,w,h,18,12,45,30,body)
                _rect(p,w,h,21,15,42,28,dark)
                _line(p,w,h,56,27,115,27,2,(118,121,118))
                _rect(p,w,h,10,32,20,37,(231,220,174))
            _line(p,w,h,12,45,114,45,2,shadow)
            return w,h,p

        # three-quarter views
        w,h=104,60; p=_canvas(w,h)
        mirror = rot in (6,8)
        rearward = rot in (4,6)
        if not mirror:
            _rect(p,w,h,12,29,62,45,tray)
            _rect(p,w,h,58,22,92,45,body)
            _rect(p,w,h,65,13,89,30,body)
            _rect(p,w,h,68,16,86,28,dark)
            wheel(p,w,h,28,48); wheel(p,w,h,80,48)
            _line(p,w,h,13,28,58,28,2,(113,116,113))
            if rearward: _rect(p,w,h,13,34,20,40,(153,40,36))
            else: _rect(p,w,h,89,32,98,38,(231,220,174))
        else:
            _rect(p,w,h,42,29,92,45,tray)
            _rect(p,w,h,12,22,46,45,body)
            _rect(p,w,h,15,13,39,30,body)
            _rect(p,w,h,18,16,36,28,dark)
            wheel(p,w,h,24,48); wheel(p,w,h,76,48)
            _line(p,w,h,46,28,91,28,2,(113,116,113))
            if rearward: _rect(p,w,h,84,34,91,40,(153,40,36))
            else: _rect(p,w,h,6,32,15,38,(231,220,174))
        return w,h,p

    for rot in range(1,9):
        w,h,p=hilux_view(rot)
        _png(root/"sprites"/f"HILXA{rot}.png",w,h,p,w//2,h-4)

    def bin_sprite(name,lid):
        w,h=44,62; p=_canvas(w,h)
        shell=(48,71,51)
        _rect(p,w,h,10,16,34,52,shell)
        _line(p,w,h,13,23,31,23,1,(35,54,39))
        _line(p,w,h,13,31,31,31,1,(35,54,39))
        _rect(p,w,h,7,10,37,18,lid)
        _line(p,w,h,8,10,36,10,2,_shade(lid,18))
        _disc(p,w,h,14,54,5,5,(27,28,27))
        _disc(p,w,h,31,54,5,5,(27,28,27))
        _png(root/"sprites"/f"{name}A0.png",w,h,p,22,57)
    bin_sprite("BINR",(153,49,43))
    bin_sprite("BINY",(196,166,45))

    # Low garden shrub, used around 42 and the immediate neighbours.
    w,h=64,48; p=_canvas(w,h)
    for cx,cy,rx,ry,col in [
        (19,27,15,15,(56,91,50)),(35,22,18,18,(48,81,44)),
        (50,29,13,13,(64,96,52)),(30,34,17,12,(53,86,47))
    ]:
        _disc(p,w,h,cx,cy,rx,ry,col)
    _rect(p,w,h,29,35,34,47,(75,54,38))
    _png(root/"sprites"/"SHRBA0.png",w,h,p,32,46)

    # Finer outdoor flats so road, footpath, driveway, lawn and garden do not
    # all read as the same generic surface.
    _flat(root,"H42LWN",(72,105,59),"grass")
    _flat(root,"H42VERG",(77,102,62),"grass")
    _flat(root,"H42DRV",(156,154,148),"concrete")
    _flat(root,"H42PATH",(167,165,158),"concrete")
    _flat(root,"H42ROAD",(61,63,62),"asphalt")
    _flat(root,"H42BED",(91,69,47),"concrete")

def generate_house42_assets(root: Path):
    root=Path(root)
    _plaster(root,"H42WALL",(211,205,192))
    _plaster(root,"H42GREY",(188,188,184),grey=True)
    _panel(root)
    _kitchen(root)
    _bath(root)
    _siding(root)
    _brick(root)
    _corrug(root)
    _fence(root)
    _gate(root)
    _window(root)
    _blinds(root)
    _door(root,"H42DOOR",True)
    _door(root,"H42WDR",False)
    _front_door(root)
    _sofa(root)
    _appliance(root)
    _doorbell_sprite(root)
    _cola_sprite(root)
    _environment_sprites(root)
    _extra_street_details(root)
    _wav(root,"doorbell.wav",780,.18,.03)
    _curb(root)
    _neighbor(root,"H42NBR1",False)
    _neighbor(root,"H42NBR2",True)
    _play(root)

    for spec in [
      ("H42CARP",(95,76,63),"carpet"),
      ("H42WOOD",(132,83,48),"wood"),
      ("H42VNYL",(164,142,106),"vinyl"),
      ("H42TILF",(184,174,153),"tile"),
      ("H42CONC",(151,149,143),"concrete"),
      ("H42ASPH",(64,66,65),"asphalt"),
      ("H42GRAS",(66,94,56),"grass"),
      ("H42PAVE",(135,109,86),"pave"),
      ("H42CEIL",(217,213,202),"tile"),
      ("H42DIRT",(95,78,59),"concrete"),
      ("H42ROOF",(71,69,66),"roof"),
      ("H42SAFE",(174,112,65),"pave"),
      ("H44ROOF",(103,72,58),"roof"),
      ("H40ROOF",(83,77,69),"roof"),
      ("H39ROOF",(112,74,57),"roof"),
      ("H37ROOF",(119,77,58),"roof"),
      ("H35ROOF",(101,69,56),"roof"),
    ]:
        _flat(root,*spec)

    _prop_bin(root)
    _prop_bathroom(root)
    _atlas(root)
    print("Generated source-matched 42 Arnold MAP01 texture/detail pack")
