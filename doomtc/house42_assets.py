from pathlib import Path
import math, random
from PIL import Image, ImageOps

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
    cream=(211,208,191)
    for y in range(h):
        band=y%18
        for x in range(w):
            c=_noise(cream,x,y,5,9)
            # weatherboard lap: dark underside, thin highlight on upper edge
            if band in (0,1): c=_shade(c,-34)
            elif band in (2,3): c=_shade(c,10)
            # subtle age/grime toward the lower wall
            if y>104 and ((x*7+y*11)%37)<8: c=_shade(c,-8)
            _set(p,w,h,x,y,c)
    # sparse nail heads so large walls do not read as sterile stripes
    for yy in range(9,128,18):
        for xx in range(15,128,32):
            _disc(p,w,h,xx,yy,1,1,(114,112,105))
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
    # Uneven suburban timber paling fence with rails, knots and plank variation.
    widths=(20,23,19,25,21,20)
    edges=[0]; x=0; i=0
    while x<128:
        x += widths[i%len(widths)]
        edges.append(min(127,x)); i+=1
    for y in range(h):
        for x in range(w):
            plank=0
            for j,e in enumerate(edges[1:]):
                if x<e: plank=j; break
            base=(72+((plank*7)%12)-6,61+((plank*5)%10)-5,49+((plank*3)%8)-4)
            c=_noise(base,x,y,8,13+plank)
            if any(abs(x-e)<=1 for e in edges): c=_shade(c,-28)
            if y in (36,37,96,97): c=_shade(c,-24)
            if y>112: c=_shade(c,-9)
            _set(p,w,h,x,y,c)
    # knots and nail points
    for cx,cy in ((15,27),(44,73),(70,19),(98,58),(119,88)):
        _disc(p,w,h,cx,cy,3,2,(48,42,35))
        _disc(p,w,h,cx,cy,1,1,(31,29,26))
    _png(root/"textures"/"H42FENC.png",w,h,p)
def _dog_hole_fence(root):
    """Rear-fence section visibly damaged where the dog dug underneath.

    This is still a blocking Doom midtexture: the gap is visual/environmental
    evidence, not a player shortcut.
    """
    w=h=128; p=_canvas(w,h)
    wood=(78,65,51)
    gap_l,gap_r=39,89
    gap_top=94

    # Paling fence, deliberately leave the dog-sized bottom opening transparent.
    for x in range(w):
        plank=(x//20)
        base=(wood[0]+((plank*5)%9)-4, wood[1]+((plank*3)%7)-3, wood[2]+((plank*7)%9)-4)
        for y in range(h):
            if gap_l <= x <= gap_r and y >= gap_top:
                continue
            c=_noise(base,x,y,7,319+plank)
            if x%20 in (0,1): c=_shade(c,-25)
            if y in (35,36,94,95): c=_shade(c,-18)
            _set(p,w,h,x,y,c)

    # Broken/raised board edges and scratch marks around the opening.
    _line(p,w,h,gap_l-4,60,gap_l+3,111,5,(93,69,47))
    _line(p,w,h,gap_r+4,61,gap_r-2,112,5,(90,66,45))
    _line(p,w,h,gap_l-1,88,gap_l+9,101,2,(47,39,32))
    _line(p,w,h,gap_r+1,87,gap_r-10,102,2,(47,39,32))
    for x0 in (50,60,72,81):
        _line(p,w,h,x0,83,x0-5,95,1,(42,35,29))

    # Dark soil lip visible at the base, with the centre left transparent so
    # the actual yard beyond is visible through the dog-sized gap.
    _line(p,w,h,28,116,100,116,4,(71,50,35))
    _line(p,w,h,33,121,95,121,3,(54,41,31))
    _png(root/"textures"/"H42DHOL.png",w,h,p)


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
    w=h=128; p=_canvas(w,h)
    if brick:
        mortar=(168,142,124); brickc=(142,73,48)
        for y in range(h):
            for x in range(w):
                row=y//10
                xx=(x + (5 if row%2 else 0))%24
                c=_noise(brickc,x,y,5,201)
                if y%10 in (0,1) or xx in (0,1): c=mortar
                _set(p,w,h,x,y,c)
    else:
        base=(205,202,186)
        for y in range(h):
            band=y%15
            for x in range(w):
                c=_noise(base,x,y,4,203)
                if band in (0,1): c=_shade(c,-23)
                elif band in (2,3): c=_shade(c,8)
                _set(p,w,h,x,y,c)

    # Eave shadow makes the facade read as a house rather than a featureless wall.
    _rect(p,w,h,0,0,w,10,(73,69,62))
    # Two domestic windows with warm interior glow.
    for x0,x1 in ((10,48),(76,116)):
        _rect(p,w,h,x0,24,x1,69,(200,198,184))
        _rect(p,w,h,x0+4,28,x1-4,65,(82,68,47))
        for y in range(30,64):
            for x in range(x0+6,x1-5):
                c=_noise((119,89,48),x,y,4,211)
                if ((x+y)%31)==0: c=_shade(c,14)
                _set(p,w,h,x,y,c)
        _rect(p,w,h,(x0+x1)//2-2,28,(x0+x1)//2+2,65,(184,181,168))
    # Front door / porch recess.
    _rect(p,w,h,52,50,72,116,(66,58,50))
    _rect(p,w,h,55,54,69,113,(101,77,55))
    _disc(p,w,h,66,84,2,2,(181,174,151))
    # Concrete/brick base.
    _rect(p,w,h,0,116,w,128,(120,112,102))
    _png(root/"textures"/f"{name}.png",w,h,p)

def _roofwall(root):
    w=h=128; p=_canvas(w,h)
    base=(77,70,65)
    for y in range(h):
        row=y//10
        for x in range(w):
            c=_noise(base,x,y,5,217)
            if y%10 in (0,1): c=_shade(c,-24)
            if (x + (12 if row%2 else 0))%24 in (0,1): c=_shade(c,-9)
            _set(p,w,h,x,y,c)
    # shadow under eave
    _rect(p,w,h,0,112,w,128,(49,47,44))
    _png(root/"textures"/"H42ROFW.png",w,h,p)

def _litwindow(root):
    w=h=128; p=_canvas(w,h)
    frame=(205,202,188); glow=(151,104,53)
    _rect(p,w,h,0,0,w,h,frame)
    _rect(p,w,h,7,7,121,121,(69,55,42))
    for y in range(10,118):
        for x in range(10,118):
            c=_noise(glow,x,y,5,223)
            # warm curtains / irregular room light
            if x<28 or x>100: c=_shade(c,-20)
            if y>92: c=_shade(c,-14)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,61,7,67,121,(190,187,173))
    _rect(p,w,h,7,61,121,67,(190,187,173))
    _png(root/"textures"/"H42LWIN.png",w,h,p)
def _play(root):
    w=h=128; p=_canvas(w,h)
    # Timber reserve boundary with vegetation at the base. Equipment is rendered
    # as proper sprites/sectors, never painted onto a billboard wall.
    wood=(91,72,55)
    for y in range(h):
        for x in range(w):
            c=_noise(wood,x,y,6,231)
            if x%18 in (0,1,2): c=_shade(c,-23)
            if y in (40,41,92,93): c=_shade(c,-16)
            _set(p,w,h,x,y,c)
    # darker support posts
    for x in range(8,128,36):
        _rect(p,w,h,x,0,x+4,128,(60,52,44))
    # irregular shrubs/grass along the bottom
    for cx,cy,rx,ry,col in [
        (14,111,14,17,(47,72,42)),(34,114,18,15,(55,82,46)),
        (66,111,20,18,(44,69,40)),(96,115,20,15,(56,83,46)),
        (121,110,14,18,(48,75,42))
    ]:
        _disc(p,w,h,cx,cy,rx,ry,col)
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
                if x%16 in (0,1) or y%16 in (0,1): c=_shade(c,-9)
                if (x//8+y//8)%2==0: c=_shade(c,4)
            elif kind=="tile":
                if x%16 in (0,1) or y%16 in (0,1): c=(139,136,128)
            elif kind=="concrete":
                # slab joins, aggregate and faint worn/cracked patches
                if x in (31,32) or y in (31,32): c=_shade(c,-16)
                if ((x*17+y*23)%67)<3: c=_shade(c,-19)
                if ((x-12)*(x-12)+(y-48)*(y-48))<8: c=_shade(c,-12)
                if (x+y in (42,43,44) and 10<x<31): c=_shade(c,-18)
            elif kind=="asphalt":
                # coarse road aggregate plus two tiny irregular crack traces
                if ((x*11+y*17)%23)<5: c=_shade(c,10)
                if ((x*19+y*7)%41)<2: c=_shade(c,-10)
                if (x==22+(y//9)%3 and 9<y<45): c=_shade(c,-24)
                if (y==49 and 35<x<54): c=_shade(c,-18)
            elif kind=="grass":
                # patchy mown suburban lawn, not a uniform green carpet
                if ((x*3+y*5)%17)<5: c=_shade(c,-10)
                if ((x*7+y*13)%41)<3: c=_shade(c,12)
                if ((x//12)+(y//10))%5==0: c=_shade(c,5)
                if y%16 in (0,1) and (x//8)%3==0: c=_shade(c,-5)
            elif kind=="pave":
                # staggered small pavers / safety-surface breakup
                row=y//12
                if y%12 in (0,1): c=_shade(c,-22)
                if (x+(8 if row%2 else 0))%16 in (0,1): c=_shade(c,-18)
            elif kind=="roof":
                # staggered tiled roof rows
                row=y//10
                if y%10 in (0,1): c=_shade(c,-24)
                if (x+(12 if row%2 else 0))%24 in (0,1): c=_shade(c,-10)
                if y%10==2: c=_shade(c,6)
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

def _front_rear_facades(root):
    # FRONT: Arnold Street only. Cream horizontal weatherboards with brick base.
    # REAR: enclosed sunroom/veranda from the walkthrough. It must never resemble
    # the front porch or the earlier full-height barred facade.
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        band=y%16
        for x in range(w):
            c=_noise((205,202,187),x,y,5,101)
            if band in (0,1): c=_shade(c,-24)
            elif band in (2,3): c=_shade(c,8)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,0,106,w,128,(124,69,48))
    for yy in range(106,128,11):
        _line(p,w,h,0,yy,w-1,yy,1,(164,130,105))
    _png(root/"textures"/"H42FACA.png",w,h,p)

    # Rear opaque pieces: horizontal older cream boards, darker than the front,
    # with a concrete/painted base. No vertical prison-bar rhythm.
    w=h=128; p=_canvas(w,h)
    for y in range(h):
        band=y%15
        for x in range(w):
            c=_noise((187,187,174),x,y,5,109)
            if band in (0,1): c=_shade(c,-22)
            elif band in (2,3): c=_shade(c,7)
            if y>98: c=_shade(c,-9)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,0,108,w,128,(126,124,116))
    _line(p,w,h,0,107,w-1,107,2,(86,86,81))
    _png(root/"textures"/"H42REAR.png",w,h,p)

    # Rear sunroom glazing from the video: wide domestic panes above a low
    # cream sill/panel wall. 256px wide prevents repetitive jail-bar windows.
    w=256; h=128; p=_canvas(w,h)
    frame=(171,173,168); frame_dark=(112,114,111)
    sill=(188,186,174); glass=(35,43,47)
    _rect(p,w,h,0,0,w,h,sill)
    _rect(p,w,h,5,7,251,82,glass)
    for y in range(9,81):
        for x in range(7,249):
            c=_noise((38,46,50),x,y,5,117)
            if ((x*3+y*5)%101)==0: c=_shade(c,12)
            _set(p,w,h,x,y,c)
    # Three broad window bays and one horizontal rail.
    for x in (5,86,168,251):
        _rect(p,w,h,max(0,x-2),5,min(w,x+2),86,frame)
    _rect(p,w,h,5,45,251,50,frame)
    _line(p,w,h,5,84,251,84,2,frame_dark)
    # Lower solid veranda panels.
    _rect(p,w,h,5,86,251,121,sill)
    for x in (86,168):
        _rect(p,w,h,x-2,86,x+2,121,frame_dark)
    _rect(p,w,h,0,121,w,128,(124,122,115))
    _png(root/"textures"/"H42RWIN.png",w,h,p)

    # Actual rear/sunroom screen door: dark mesh/glass upper half, solid lower
    # panel and narrow off-white frame. This is deliberately not the front door.
    w=64; h=128; p=_canvas(w,h)
    frame=(194,193,183); dark=(37,42,43)
    _rect(p,w,h,0,0,w,h,(154,153,145))
    _rect(p,w,h,5,4,59,124,frame)
    _rect(p,w,h,10,10,54,75,dark)
    # screen mesh
    for y in range(12,74,6):
        _line(p,w,h,11,y,53,y,1,(62,67,67),130)
    for x in range(12,54,6):
        _line(p,w,h,x,11,x,74,1,(62,67,67),130)
    _rect(p,w,h,10,81,54,117,(181,179,167))
    _line(p,w,h,10,80,54,80,2,(116,115,109))
    _disc(p,w,h,51,79,3,3,(89,83,72))
    _png(root/"textures"/"H42RDR.png",w,h,p)
def _environment_sprites(root):
    # Street lamp with a compact warm lantern; map sectors provide the light pool.
    w,h=48,128; p=_canvas(w,h)
    _rect(p,w,h,22,24,27,124,(67,68,66))
    _rect(p,w,h,18,18,31,26,(88,88,83))
    _rect(p,w,h,14,11,35,20,(129,124,107))
    _rect(p,w,h,17,13,32,18,(225,207,148))
    _disc(p,w,h,24,15,7,4,(240,219,157),210)
    _png(root/"sprites"/"STLPA0.png",w,h,p,24,124)

    # Mature suburban street tree: visible branching and irregular leaf masses,
    # not a single green oval.
    w,h=112,144; p=_canvas(w,h)
    trunk=(75,55,40); branch=(82,59,42)
    _rect(p,w,h,50,70,61,139,trunk)
    _line(p,w,h,55,86,30,55,5,branch)
    _line(p,w,h,57,80,80,49,5,branch)
    _line(p,w,h,53,74,45,42,4,branch)
    blobs=[
        (29,52,23,22,(46,73,42)),(49,47,28,26,(50,79,45)),
        (76,51,25,24,(42,69,39)),(61,29,25,22,(56,86,48)),
        (32,30,20,19,(61,91,50)),(87,31,17,18,(48,77,43)),
        (19,70,17,18,(54,82,45)),(90,69,17,19,(44,72,40)),
        (51,67,27,20,(49,78,43))
    ]
    for cx,cy,rx,ry,col in blobs:
        _disc(p,w,h,cx,cy,rx,ry,col)
    # leaf speckle breaks up the blob edges in classic Doom fashion
    for y in range(15,88,7):
        for x in range(10,103,9):
            if ((x*13+y*7)%5)==0:
                _disc(p,w,h,x,y,2,2,(68,99,53),180)
    _png(root/"sprites"/"TREEA0.png",w,h,p,56,139)

    # Second suburban/gum-tree silhouette: taller, lighter canopy and a bent trunk.
    w,h=104,152; p=_canvas(w,h)
    trunk=(83,67,50); branch=(91,73,54)
    _line(p,w,h,50,146,53,82,8,trunk)
    _line(p,w,h,52,102,34,63,5,branch)
    _line(p,w,h,54,96,74,58,5,branch)
    _line(p,w,h,51,86,49,45,4,branch)
    for cx,cy,rx,ry,col in [
        (48,41,24,20,(62,91,56)),(29,55,21,19,(67,97,59)),
        (72,55,22,20,(55,85,51)),(80,32,15,14,(70,100,61)),
        (19,35,14,13,(73,102,63)),(52,65,25,17,(57,87,52))
    ]:
        _disc(p,w,h,cx,cy,rx,ry,col)
    for y in range(20,76,9):
        for x in range(12,94,10):
            if ((x*7+y*11)%4)==0:
                _disc(p,w,h,x,y,2,2,(84,112,67),170)
    _png(root/"sprites"/"TRE2A0.png",w,h,p,52,146)

    # Park bench.
    w,h=80,64; p=_canvas(w,h)
    _rect(p,w,h,8,24,72,30,(104,71,44)); _rect(p,w,h,8,35,72,41,(104,71,44))
    _rect(p,w,h,15,12,65,18,(112,75,45)); _rect(p,w,h,15,18,19,55,(61,61,58)); _rect(p,w,h,61,18,65,55,(61,61,58))
    _png(root/"sprites"/"BNCHA0.png",w,h,p,40,56)

    # Swing frame.
    w,h=96,96; p=_canvas(w,h); metal=(75,81,82)
    _line(p,w,h,12,88,28,15,4,metal); _line(p,w,h,84,88,68,15,4,metal); _line(p,w,h,26,15,70,15,4,metal)
    for x in (39,57):
        _line(p,w,h,x,18,x,60,1,(46,47,46)); _line(p,w,h,x+8,18,x+8,60,1,(46,47,46)); _rect(p,w,h,x,60,x+8,64,(121,71,44))
    _png(root/"sprites"/"SWNGA0.png",w,h,p,48,90)

    # Slide and climber.
    w,h=96,80; p=_canvas(w,h)
    _rect(p,w,h,24,18,48,25,(149,62,46)); _line(p,w,h,26,25,16,70,4,(72,78,79)); _line(p,w,h,46,25,78,67,6,(169,80,52))
    _line(p,w,h,22,18,22,68,3,(72,78,79)); _line(p,w,h,50,18,50,56,3,(72,78,79))
    _png(root/"sprites"/"SLIDA0.png",w,h,p,48,72)

    w,h=96,80; p=_canvas(w,h)
    for x in (18,38,58,78): _line(p,w,h,x,22,x,72,3,metal)
    _line(p,w,h,18,22,78,22,3,metal); _line(p,w,h,18,46,78,46,2,metal); _line(p,w,h,18,70,78,70,3,metal)
    _rect(p,w,h,30,28,66,36,(139,65,45))
    _png(root/"sprites"/"CLMBA0.png",w,h,p,48,72)

    # General wheelie bin.
    w,h=48,64; p=_canvas(w,h)
    _rect(p,w,h,11,16,37,54,(53,79,56)); _rect(p,w,h,8,12,40,19,(69,92,64))
    _line(p,w,h,14,25,34,25,1,(36,60,41)); _line(p,w,h,14,34,34,34,1,(36,60,41))
    _disc(p,w,h,15,56,5,5,(28,29,28)); _disc(p,w,h,33,56,5,5,(28,29,28))
    _png(root/"sprites"/"WBINA0.png",w,h,p,24,58)
def _scene_polish_props(root):
    # Large playground tower: one Doom sprite combining roof, platform, ladder and slide.
    w,h=132,118; p=_canvas(w,h)
    metal=(66,75,77); timber=(107,77,50); red=(151,61,45); roof=(77,68,52)
    # supports/platform
    for x in (28,54,80,104):
        _rect(p,w,h,x,40,x+5,108,metal)
    _rect(p,w,h,24,50,108,57,timber)
    _rect(p,w,h,30,36,102,43,timber)
    # pitched roof
    _line(p,w,h,25,35,65,10,6,roof); _line(p,w,h,65,10,106,35,6,roof)
    _line(p,w,h,31,35,99,35,5,roof)
    # ladder and rails
    _line(p,w,h,31,58,19,106,4,metal); _line(p,w,h,47,58,35,106,4,metal)
    for yy in range(64,104,9): _line(p,w,h,23,yy,41,yy,2,metal)
    # long red slide
    _line(p,w,h,94,57,123,106,9,red)
    _line(p,w,h,89,57,118,106,2,(92,54,43))
    # guard rails
    _line(p,w,h,54,43,54,26,3,metal); _line(p,w,h,80,43,80,26,3,metal)
    _line(p,w,h,54,27,80,27,3,metal)
    _png(root/"sprites"/"PTOWA0.png",w,h,p,66,110)

    # Dense clipped hedge with irregular upper edge.
    w,h=104,58; p=_canvas(w,h)
    base=(47,76,43)
    _rect(p,w,h,7,18,97,55,base)
    for cx,cy,rx,ry,col in [
        (15,24,13,15,(57,87,48)),(34,18,16,16,(51,81,45)),
        (55,22,18,17,(62,92,51)),(77,17,15,17,(48,78,43)),
        (92,25,12,14,(58,88,48))
    ]: _disc(p,w,h,cx,cy,rx,ry,col)
    for y in range(16,50,7):
        for x in range(8,98,8):
            if ((x*5+y*3)%4)==0: _disc(p,w,h,x,y,2,2,(72,101,57),170)
    _png(root/"sprites"/"HEDGA0.png",w,h,p,52,55)

    # Brick porch / fence pier.
    w,h=34,70; p=_canvas(w,h)
    mortar=(159,132,114); brick=(133,68,46)
    for y in range(h):
        row=y//8
        for x in range(w):
            xx=(x+(4 if row%2 else 0))%18
            c=_noise(brick,x,y,4,251)
            if y%8 in (0,1) or xx in (0,1): c=mortar
            _set(p,w,h,x,y,c)
    _rect(p,w,h,2,0,32,5,(116,105,95))
    _png(root/"sprites"/"BRPRA0.png",w,h,p,17,68)

    # Static suburban letterbox in a small masonry pillar.
    w,h=46,68; p=_canvas(w,h)
    stone=(135,128,116)
    for y in range(h):
        for x in range(w):
            c=_noise(stone,x,y,4,257)
            if y%13 in (0,1): c=_shade(c,-10)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,8,21,38,34,(58,58,56))
    _rect(p,w,h,11,24,35,29,(24,25,24))
    _disc(p,w,h,34,42,2,2,(96,93,85))
    _png(root/"sprites"/"MBXSA0.png",w,h,p,23,66)

    # Small warm porch light for domestic facades.
    w,h=28,34; p=_canvas(w,h)
    _rect(p,w,h,9,12,19,30,(80,78,70))
    _rect(p,w,h,6,5,22,15,(139,125,93))
    _rect(p,w,h,8,7,20,13,(236,206,132))
    _disc(p,w,h,14,10,7,5,(245,215,143),175)
    _png(root/"sprites"/"PLITA0.png",w,h,p,14,30)

def _extra_street_details(root):
    # White Toyota Hilux Workmate-style single-cab tray ute. Eight directional
    # sprites give stable world orientation while the player walks around it.
    body=(215,216,210); body_hi=(231,231,224); shadow=(142,145,142)
    dark=(38,45,48); tray=(155,158,155); tyre=(25,26,25); rim=(132,134,131)
    red=(142,42,38); amber=(207,159,71)

    def wheel(p,w,h,cx,cy):
        _disc(p,w,h,cx,cy,9,9,tyre)
        _disc(p,w,h,cx,cy,4,4,rim)
        _disc(p,w,h,cx,cy,2,2,(64,66,65))

    def tailgate_letters(p,w,h,x0,y0):
        # Tiny block lettering reads as TOYOTA without turning into UI text.
        patt={
          "T":["111","010","010","010"],"O":["111","101","101","111"],
          "Y":["101","111","010","010"],"A":["010","101","111","101"]
        }
        x=x0
        for ch in "TOYOTA":
            rows=patt[ch]
            for yy,row in enumerate(rows):
                for xx,v in enumerate(row):
                    if v=="1": _rect(p,w,h,x+xx*2,y0+yy*2,x+xx*2+1,y0+yy*2+1,(84,86,83))
            x+=8

    def frontrear(front=True):
        w,h=92,72; p=_canvas(w,h)
        wheel(p,w,h,19,58); wheel(p,w,h,73,58)
        if front:
            _rect(p,w,h,13,31,79,55,body)
            _rect(p,w,h,22,17,70,38,body_hi)
            _rect(p,w,h,27,20,65,34,dark)
            _rect(p,w,h,17,39,75,47,(104,108,106))
            _rect(p,w,h,14,47,78,53,(176,178,173))
            _rect(p,w,h,18,37,27,43,(229,214,164))
            _rect(p,w,h,65,37,74,43,(229,214,164))
            _rect(p,w,h,9,30,14,43,(70,72,71)); _rect(p,w,h,78,30,83,43,(70,72,71))
        else:
            _rect(p,w,h,10,29,82,54,tray)
            _rect(p,w,h,16,22,76,34,(171,173,168))
            _line(p,w,h,16,23,76,23,2,(108,111,108))
            _rect(p,w,h,15,34,77,50,(166,169,165))
            tailgate_letters(p,w,h,27,37)
            _rect(p,w,h,12,42,20,49,red); _rect(p,w,h,72,42,80,49,red)
            _rect(p,w,h,38,51,54,55,(72,73,71))
        return w,h,p

    def side(left_to_right=True):
        w,h=142,68; p=_canvas(w,h)
        wheel(p,w,h,34,55); wheel(p,w,h,108,55)
        if left_to_right:
            _rect(p,w,h,8,31,79,51,tray)
            _line(p,w,h,11,30,76,30,2,(108,111,108))
            _rect(p,w,h,77,25,126,51,body)
            _rect(p,w,h,89,12,124,31,body_hi)
            _rect(p,w,h,93,15,121,29,dark)
            _line(p,w,h,107,15,107,29,2,(119,123,123))
            _rect(p,w,h,124,34,134,41,(229,214,164))
            _rect(p,w,h,82,34,86,43,shadow)
        else:
            _rect(p,w,h,63,31,134,51,tray)
            _line(p,w,h,66,30,131,30,2,(108,111,108))
            _rect(p,w,h,16,25,65,51,body)
            _rect(p,w,h,18,12,53,31,body_hi)
            _rect(p,w,h,21,15,49,29,dark)
            _line(p,w,h,35,15,35,29,2,(119,123,123))
            _rect(p,w,h,8,34,18,41,(229,214,164))
            _rect(p,w,h,56,34,60,43,shadow)
        return w,h,p

    def threeq(mirror=False,rear=False):
        w,h=118,70; p=_canvas(w,h)
        if not mirror:
            wheel(p,w,h,30,56); wheel(p,w,h,90,56)
            _rect(p,w,h,10,32,65,51,tray)
            _rect(p,w,h,62,26,103,51,body)
            _rect(p,w,h,72,14,100,31,body_hi)
            _rect(p,w,h,76,17,97,29,dark)
            _line(p,w,h,84,17,84,29,2,(116,120,120))
            _line(p,w,h,12,31,62,31,2,(106,109,106))
            _rect(p,w,h,99,35,109,42,(red if rear else (229,214,164)))
        else:
            wheel(p,w,h,28,56); wheel(p,w,h,88,56)
            _rect(p,w,h,53,32,108,51,tray)
            _rect(p,w,h,15,26,56,51,body)
            _rect(p,w,h,18,14,46,31,body_hi)
            _rect(p,w,h,21,17,42,29,dark)
            _line(p,w,h,34,17,34,29,2,(116,120,120))
            _line(p,w,h,56,31,106,31,2,(106,109,106))
            _rect(p,w,h,9,35,19,42,(red if rear else (229,214,164)))
        return w,h,p

    views={
      1:frontrear(True), 5:frontrear(False),
      3:side(True), 7:side(False),
      2:threeq(False,False), 4:threeq(False,True),
      8:threeq(True,False), 6:threeq(True,True)
    }
    for rot,(w,h,p) in views.items():
        _png(root/"sprites"/f"HILXA{rot}.png",w,h,p,w//2,h-5)

    # Simple parked sedan with 8 rotational lumps, so it does not turn to face the player.
    def sedan(prefix,base):
        for rot in range(1,9):
            w,h=96,50; p=_canvas(w,h)
            if rot in (1,5):
                _disc(p,w,h,20,42,7,7,(25,26,26)); _disc(p,w,h,76,42,7,7,(25,26,26))
                _rect(p,w,h,12,23,84,41,base); _rect(p,w,h,25,12,71,28,base); _rect(p,w,h,30,15,66,26,(42,50,55))
            else:
                _disc(p,w,h,27,42,7,7,(25,26,26)); _disc(p,w,h,69,42,7,7,(25,26,26))
                _rect(p,w,h,8,24,88,41,base); _rect(p,w,h,26,12,70,29,base); _rect(p,w,h,31,15,65,27,(42,50,55))
            _png(root/"sprites"/f"{prefix}A{rot}.png",w,h,p,48,46)
    sedan("CARW",(181,184,180)); sedan("CARD",(66,72,75))

    def bin_sprite(name,lid):
        w,h=44,62; p=_canvas(w,h); shell=(48,71,51)
        _rect(p,w,h,10,16,34,52,shell); _rect(p,w,h,7,10,37,18,lid)
        _disc(p,w,h,14,54,5,5,(27,28,27)); _disc(p,w,h,31,54,5,5,(27,28,27))
        _png(root/"sprites"/f"{name}A0.png",w,h,p,22,57)
    bin_sprite("BINR",(153,49,43)); bin_sprite("BINY",(196,166,45))

    w,h=64,48; p=_canvas(w,h)
    for cx,cy,rx,ry,col in [(19,27,15,15,(56,91,50)),(35,22,18,18,(48,81,44)),(50,29,13,13,(64,96,52)),(30,34,17,12,(53,86,47))]:
        _disc(p,w,h,cx,cy,rx,ry,col)
    _rect(p,w,h,29,35,34,47,(75,54,38))
    _png(root/"sprites"/"SHRBA0.png",w,h,p,32,46)

    # Dug-under-fence evidence: dark hole, disturbed soil and loose board.
    w,h=72,48; p=_canvas(w,h)
    _disc(p,w,h,34,38,24,8,(55,39,29))
    _disc(p,w,h,34,37,15,5,(20,18,16))
    _line(p,w,h,12,27,58,31,4,(89,65,44)); _line(p,w,h,49,19,58,37,5,(71,54,39))
    _png(root/"sprites"/"DOGDA0.png",w,h,p,36,45)

    # Small spare-key sprite.
    w,h=32,24; p=_canvas(w,h)
    _disc(p,w,h,8,10,6,6,(184,155,72)); _disc(p,w,h,8,10,3,3,(30,30,28))
    _rect(p,w,h,13,8,29,12,(184,155,72)); _rect(p,w,h,23,12,27,17,(184,155,72))
    _png(root/"sprites"/"BDKYA0.png",w,h,p,16,19)

    # Finer outdoor flats.
    _flat(root,"H42LWN",(72,105,59),"grass")
    _flat(root,"H42VERG",(77,102,62),"grass")
    _flat(root,"H42DRV",(156,154,148),"concrete")
    _flat(root,"H42PATH",(167,165,158),"concrete")
    _flat(root,"H42ROAD",(61,63,62),"asphalt")
    _flat(root,"H42BED",(91,69,47),"concrete")
    _flat(root,"H42SAFE",(174,112,65),"pave")

def _puzzle_story_assets(root):
    # Small black/steel padlock for the side iron gate Sam locks behind him.
    w,h=28,30; p=_canvas(w,h)
    metal=(116,118,113); dark=(46,47,45)
    _line(p,w,h,8,13,8,7,4,metal); _line(p,w,h,20,13,20,7,4,metal)
    _line(p,w,h,8,7,20,7,4,metal)
    _rect(p,w,h,5,12,23,27,dark)
    _rect(p,w,h,8,15,20,24,(74,75,72))
    _disc(p,w,h,14,19,2,2,(24,25,24))
    _line(p,w,h,14,20,14,23,1,(24,25,24))
    _png(root/"sprites"/"GPDLA0.png",w,h,p,14,27)

    # Small coloured keys for the two house/gate locks.
    for name,col in [("FDKY",(204,177,57)),("PGKY",(158,49,45))]:
        w,h=32,24; p=_canvas(w,h)
        _disc(p,w,h,8,10,6,6,col); _disc(p,w,h,8,10,3,3,(28,28,27))
        _rect(p,w,h,13,8,29,12,col); _rect(p,w,h,23,12,27,18,col)
        _png(root/"sprites"/f"{name}A0.png",w,h,p,16,19)

    # Lincoln's phone.
    w,h=30,46; p=_canvas(w,h)
    _rect(p,w,h,4,2,26,44,(34,36,38)); _rect(p,w,h,6,6,24,38,(49,63,71))
    for yy in (12,17,22,27,32): _rect(p,w,h,8,yy,22,yy+1,(184,196,194))
    _disc(p,w,h,15,41,2,2,(97,99,98))
    _png(root/"sprites"/"PHONA0.png",w,h,p,15,42)

    # Notes taped to front door / playground gate.
    for name,base,ink in [("FDNT",(215,203,166),(76,58,49)),("SGNT",(196,184,146),(111,33,31))]:
        w,h=34,42; p=_canvas(w,h)
        _rect(p,w,h,4,4,30,38,base)
        for yy in (11,16,21,26,31): _line(p,w,h,8,yy,26,yy,1,ink)
        _rect(p,w,h,13,1,21,6,(176,166,139),210)
        _png(root/"sprites"/f"{name}A0.png",w,h,p,17,38)

    # Sam's puzzle box.
    w,h=72,42; p=_canvas(w,h)
    _rect(p,w,h,6,12,66,38,(104,70,47)); _rect(p,w,h,9,7,63,16,(139,93,57))
    _line(p,w,h,8,17,64,17,2,(64,45,34)); _rect(p,w,h,28,19,44,29,(46,44,42))
    for x in (31,36,41): _disc(p,w,h,x,24,1,1,(195,173,82))
    _png(root/"sprites"/"PBOXA0.png",w,h,p,36,38)

    # Number buttons 0-9: compact high-contrast keypad tiles.
    segs={
      0:"abcedf",1:"bc",2:"abdeg",3:"abcdg",4:"bcfg",
      5:"acdfg",6:"acdefg",7:"abc",8:"abcdefg",9:"abcdfg"
    }
    coords={
      "a":(8,5,22,8),"b":(21,7,24,18),"c":(21,19,24,30),
      "d":(8,29,22,32),"e":(5,19,8,30),"f":(5,7,8,18),"g":(8,17,22,20)
    }
    # Correct the zero map explicitly; typo-safe and visually complete.
    segs[0]="abcdef"
    for d in range(10):
        w=h=36; p=_canvas(w,h)
        _rect(p,w,h,2,2,34,34,(54,51,47)); _rect(p,w,h,4,4,32,32,(25,25,24))
        for key in segs[d]:
            x0,y0,x1,y1=coords[key]; _rect(p,w,h,x0,y0,x1,y1,(210,171,61))
        _png(root/"sprites"/f"D{d}BTA0.png",w,h,p,18,32)

    # Two e-scooters in the garage.
    w,h=42,70; p=_canvas(w,h)
    _disc(p,w,h,10,60,7,7,(27,28,28)); _disc(p,w,h,32,60,7,7,(27,28,28))
    _line(p,w,h,10,57,28,57,4,(78,82,83)); _line(p,w,h,28,57,25,15,4,(78,82,83))
    _line(p,w,h,18,16,34,16,3,(78,82,83)); _disc(p,w,h,34,16,4,4,(35,36,36))
    _png(root/"sprites"/"ESCOA0.png",w,h,p,21,64)

    # TV with Xbox console underneath.
    w,h=70,54; p=_canvas(w,h)
    _rect(p,w,h,8,5,62,37,(40,42,43)); _rect(p,w,h,12,9,58,33,(31,45,55))
    _rect(p,w,h,15,40,55,49,(46,47,46)); _rect(p,w,h,25,42,45,47,(65,69,67))
    _disc(p,w,h,49,44,2,2,(77,161,89))
    _png(root/"sprites"/"XBOXA0.png",w,h,p,35,49)

    # Fridge; interaction tells player there are exactly three eggs.
    w,h=46,82; p=_canvas(w,h)
    _rect(p,w,h,7,4,39,78,(210,208,199)); _line(p,w,h,7,31,39,31,2,(158,157,150))
    _rect(p,w,h,11,12,14,27,(119,118,113)); _rect(p,w,h,11,39,14,63,(119,118,113))
    _png(root/"sprites"/"FRDGA0.png",w,h,p,23,78)

    # Projector body.
    w,h=48,30; p=_canvas(w,h)
    _rect(p,w,h,5,9,43,25,(112,115,113)); _disc(p,w,h,37,16,7,7,(49,59,64))
    _disc(p,w,h,37,16,4,4,(174,201,205)); _rect(p,w,h,10,5,24,10,(83,86,84))
    _png(root/"sprites"/"PROJA0.png",w,h,p,24,25)

    # Projected countdown: 3 -> 2 -> 1 -> 0, then remain on 0.
    def projected_digit(name,d):
        w=h=64; p=_canvas(w,h); glow=(193,222,213)
        seg={
          0:"abcdef",1:"bc",2:"abdeg",3:"abcdg"
        }[d]
        cc={"a":(18,10,46,14),"b":(44,13,49,31),"c":(44,33,49,51),
            "d":(18,50,46,54),"e":(15,33,20,51),"f":(15,13,20,31),"g":(18,30,46,35)}
        for k in seg:
            x0,y0,x1,y1=cc[k]; _rect(p,w,h,x0,y0,x1,y1,glow,150)
        _png(root/"sprites"/f"{name}.png",w,h,p,32,54)
    projected_digit("PJCTA0",3); projected_digit("PJCTB0",2); projected_digit("PJCTC0",1); projected_digit("PJCTD0",0)

    # Neighbour letterbox: masonry pillar, normal suburban scale.
    w,h=48,70; p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            c=_noise((132,124,112),x,y,4,271)
            if y%14 in (0,1): c=_shade(c,-11)
            _set(p,w,h,x,y,c)
    _rect(p,w,h,8,20,40,35,(61,61,58))
    _rect(p,w,h,11,23,37,28,(25,26,25))
    _disc(p,w,h,36,45,2,2,(102,98,88))
    _png(root/"sprites"/"LBOXA0.png",w,h,p,24,68)


_PIXEL3 = {
"A":("010","101","111","101","101"),"B":("110","101","110","101","110"),
"C":("011","100","100","100","011"),"D":("110","101","101","101","110"),
"E":("111","100","110","100","111"),"F":("111","100","110","100","100"),
"G":("011","100","101","101","011"),"H":("101","101","111","101","101"),
"I":("111","010","010","010","111"),"J":("001","001","001","101","010"),
"K":("101","101","110","101","101"),"L":("100","100","100","100","111"),
"M":("101","111","111","101","101"),"N":("101","111","111","111","101"),
"O":("010","101","101","101","010"),"P":("110","101","110","100","100"),
"Q":("010","101","101","111","011"),"R":("110","101","110","101","101"),
"S":("011","100","010","001","110"),"T":("111","010","010","010","010"),
"U":("101","101","101","101","111"),"V":("101","101","101","101","010"),
"W":("101","101","111","111","101"),"X":("101","101","010","101","101"),
"Y":("101","101","010","010","010"),"Z":("111","001","010","100","111"),
"0":("111","101","101","101","111"),"1":("010","110","010","010","111"),
"2":("110","001","010","100","111"),"3":("110","001","010","001","110"),
"4":("101","101","111","001","001"),"5":("111","100","110","001","110"),
"6":("011","100","111","101","111"),"7":("111","001","010","010","010"),
"8":("111","101","111","101","111"),"9":("111","101","111","001","110"),
"$":("010","111","110","011","010"),"-":("000","000","111","000","000"),
}

def _tiny_text(p,w,h,x,y,text,col=(35,24,18),scale=1):
    cx=x
    for ch in text.upper():
        if ch==" ":
            cx += 2*scale
            continue
        rows=_PIXEL3.get(ch)
        if rows is None:
            cx += 4*scale
            continue
        for yy,row in enumerate(rows):
            for xx,v in enumerate(row):
                if v=="1":
                    _rect(p,w,h,cx+xx*scale,y+yy*scale,
                          cx+(xx+1)*scale,y+(yy+1)*scale,col)
        cx += 4*scale

def _wanted_door_base(seed=0):
    w=64; h=128; p=_canvas(w,h)
    # dark, ordinary neighbour-house timber door
    for y in range(h):
        for x in range(w):
            c=_noise((74,55,43),x,y,5,310+seed)
            if x in (5,6,57,58) or y in (5,6,121,122): c=_shade(c,-22)
            _set(p,w,h,x,y,c)
    # paper poster fixed to door
    paper=(205,174,126)
    _rect(p,w,h,7,10,57,116,paper)
    _rect(p,w,h,8,11,56,115,(220,190,142))
    # damaged corners / age
    for cx,cy in ((9,13),(54,14),(10,111),(53,109)):
        _disc(p,w,h,cx,cy,3,3,(116,76,48),130)
    # top/bottom rule
    _line(p,w,h,10,33,54,33,1,(70,42,28))
    _line(p,w,h,10,98,54,98,1,(70,42,28))
    return w,h,p

def _poster_doors(root):
    """Install the user's eight uploaded wanted posters as natural door posters.

    The originals live under doomtc/source_posters and are treated as source of
    truth. They are not redrawn. Each image is aspect-preserved and reduced into
    a small paper poster mounted on the generated domestic door texture.
    """
    srcdir=root/"source_posters"
    source_names=[
        "poster01.png","poster02.png","poster03.png","poster04.png",
        "poster05.png","poster06.png","poster07.png","poster08.jpg",
    ]
    missing=[name for name in source_names if not (srcdir/name).is_file()]
    if missing:
        raise RuntimeError(f"missing exact uploaded wanted-poster sources: {missing}")

    door_path=root/"textures"/"H42DOOR.png"
    if not door_path.is_file():
        raise RuntimeError("H42DOOR.png must exist before wanted-poster installation")

    # Door-facing linedefs in No.44 are 32 map units wide. 32x128 prevents
    # horizontal cropping while leaving the poster at believable paper scale.
    door=Image.open(door_path).convert("RGBA").resize((32,128),Image.Resampling.LANCZOS)

    for idx,name in enumerate(source_names,1):
        poster=Image.open(srcdir/name).convert("RGBA")
        # Preserve the complete uploaded image. No crop, reinterpretation, or redraw.
        thumb=ImageOps.contain(poster,(28,58),Image.Resampling.LANCZOS)

        out=door.copy()
        x=(32-thumb.width)//2
        y=34+(58-thumb.height)//2

        # Thin dark backing/shadow makes the physical paper readable on the door.
        shadow=Image.new("RGBA",(thumb.width+2,thumb.height+2),(25,20,17,210))
        out.alpha_composite(shadow,(max(0,x-1),max(0,y-1)))
        out.alpha_composite(thumb,(x,y))

        # Save as ordinary PNG texture inside TX_START/TX_END.
        out.save(root/"textures"/f"WANT{idx:02d}.png","PNG")

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
    _dog_hole_fence(root)
    _gate(root)
    _window(root)
    _litwindow(root)
    _blinds(root)
    _door(root,"H42DOOR",True)
    _door(root,"H42WDR",False)
    _front_door(root)
    _front_rear_facades(root)
    _sofa(root)
    _appliance(root)
    _doorbell_sprite(root)
    _cola_sprite(root)
    _environment_sprites(root)
    _scene_polish_props(root)
    _extra_street_details(root)
    _puzzle_story_assets(root)
    _poster_doors(root)
    _wav(root,"doorbell.wav",780,.18,.03)
    _curb(root)
    _neighbor(root,"H42NBR1",False)
    _neighbor(root,"H42NBR2",True)
    _roofwall(root)
    _play(root)

    for spec in [
      ("H42CARP",(95,76,63),"carpet"),
      ("H42WOOD",(132,83,48),"wood"),
      ("H42VNYL",(164,142,106),"vinyl"),
      ("H42TILF",(184,174,153),"tile"),
      ("H42CONC",(145,143,137),"concrete"),
      ("H42ASPH",(67,69,68),"asphalt"),
      ("H42GRAS",(62,88,53),"grass"),
      ("H42PAVE",(135,109,86),"pave"),
      ("H42CEIL",(217,213,202),"tile"),
      ("H42DIRT",(95,78,59),"concrete"),
      ("H42ROOF",(71,69,66),"roof"),
    ]:
        _flat(root,*spec)

    _prop_bin(root)
    _prop_bathroom(root)
    _atlas(root)
    print("Generated source-matched 42 Arnold MAP01 texture/detail pack")
