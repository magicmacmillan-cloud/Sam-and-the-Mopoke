from pathlib import Path
import struct, zlib, math

# Sam and the Mopoke: original Doom-style sprite pass.
# No commercial Doom art is used. All graphics are generated from primitives.

def _png(path, w, h, rgba, offx=None, offy=None):
    raw = b"".join(b"\x00" + bytes(rgba[y*w*4:(y+1)*w*4]) for y in range(h))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
    if offx is not None and offy is not None:
        data += chunk(b"grAb", struct.pack(">ii", int(offx), int(offy)))
    data += chunk(b"IDAT", zlib.compress(raw, 9))
    data += chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

def _canvas(w, h):
    return [0] * (w*h*4)

def _set(p,w,h,x,y,c,a=255):
    if 0 <= x < w and 0 <= y < h:
        i=(y*w+x)*4
        p[i:i+4]=[c[0],c[1],c[2],a]

def _disc(p,w,h,cx,cy,rx,ry,c,a=255):
    for y in range(max(0,int(cy-ry)), min(h,int(cy+ry+1))):
        for x in range(max(0,int(cx-rx)), min(w,int(cx+rx+1))):
            if ((x-cx)/max(1,rx))**2 + ((y-cy)/max(1,ry))**2 <= 1:
                _set(p,w,h,x,y,c,a)

def _rect(p,w,h,x0,y0,x1,y1,c,a=255):
    for y in range(max(0,int(y0)), min(h,int(y1))):
        for x in range(max(0,int(x0)), min(w,int(x1))):
            _set(p,w,h,x,y,c,a)

def _line(p,w,h,x0,y0,x1,y1,thick,c):
    steps=max(abs(int(x1-x0)),abs(int(y1-y0)),1)
    for i in range(steps+1):
        t=i/steps
        x=int(x0+(x1-x0)*t); y=int(y0+(y1-y0)*t)
        _disc(p,w,h,x,y,thick,thick,c)

SKIN=(94,111,78)
SKIN_DARK=(55,73,50)
BLOOD=(105,24,23)
BONE=(174,160,132)
BLACK=(24,24,26)
METAL=(110,113,117)
WOOD=(78,50,34)
PURPLE=(103,61,126)
GLOW=(221,160,70)
GOLD=(177,127,36)
GLASS=(121,170,166)
RED=(164,37,42)
GREEN=(62,155,82)

def _hands(p,w,h,bob=0,sway=0):
    # recognisably undead Dad hands: green-grey skin, torn knuckles, blood and nails
    for cx in (37+sway, 91-sway):
        _disc(p,w,h,cx,111+bob,28,19,SKIN)
        _disc(p,w,h,cx,99+bob,18,15,SKIN)
    for x in (26,36,46,79,89,99):
        _disc(p,w,h,x+sway//2,91+bob,6,14,SKIN)
    _disc(p,w,h,30+sway,101+bob,5,3,BLOOD)
    _disc(p,w,h,88-sway,95+bob,4,4,BLOOD)
    _line(p,w,h,44,109+bob,51,113+bob,1,SKIN_DARK)
    _line(p,w,h,79,106+bob,85,110+bob,1,SKIN_DARK)

def _staff(p,w,h,bob,recoil):
    _line(p,w,h,66,112+bob,66,39+bob+recoil,7,WOOD)
    _disc(p,w,h,66,32+bob+recoil,15,13,PURPLE)
    _disc(p,w,h,66,29+bob+recoil,6,6,GLOW)
    _line(p,w,h,54,36+bob+recoil,44,22+bob+recoil,3,BONE)
    _line(p,w,h,78,36+bob+recoil,88,22+bob+recoil,3,BONE)

def _amulet(p,w,h,bob,recoil):
    _line(p,w,h,64,75+bob,64,45+bob+recoil,2,GOLD)
    _disc(p,w,h,64,39+bob+recoil,18,22,GOLD)
    _disc(p,w,h,64,39+bob+recoil,11,15,PURPLE)
    _disc(p,w,h,64,39+bob+recoil,4,5,GLOW)

def _virus(p,w,h,bob,recoil):
    _rect(p,w,h,54,42+bob+recoil,75,92+bob+recoil,METAL)
    _rect(p,w,h,57,47+bob+recoil,72,78+bob+recoil,GLASS,220)
    _rect(p,w,h,59,60+bob+recoil,70,77+bob+recoil,GREEN,235)
    _line(p,w,h,64,42+bob+recoil,64,23+bob+recoil,2,METAL)
    _disc(p,w,h,64,21+bob+recoil,3,3,RED)

def _doll(p,w,h,bob,recoil):
    _disc(p,w,h,64,42+bob+recoil,15,17,(176,154,132))
    _rect(p,w,h,50,57+bob+recoil,78,91+bob+recoil,(106,72,91))
    _line(p,w,h,51,63+bob+recoil,37,79+bob+recoil,4,(176,154,132))
    _line(p,w,h,77,63+bob+recoil,91,79+bob+recoil,4,(176,154,132))
    _disc(p,w,h,58,39+bob+recoil,2,2,BLACK); _disc(p,w,h,70,39+bob+recoil,2,2,BLACK)
    _line(p,w,h,58,50+bob+recoil,70,50+bob+recoil,1,BLOOD)

def _blood(p,w,h,bob,recoil):
    _rect(p,w,h,52,44+bob+recoil,76,91+bob+recoil,(76,58,47))
    _rect(p,w,h,55,49+bob+recoil,73,87+bob+recoil,GLASS,210)
    _rect(p,w,h,56,66+bob+recoil,72,86+bob+recoil,RED,240)
    _rect(p,w,h,57,36+bob+recoil,71,46+bob+recoil,METAL)
    _line(p,w,h,58,58+bob+recoil,70,73+bob+recoil,2,(220,206,180))

def _feeb(p,w,h,bob,recoil):
    _rect(p,w,h,48,78+bob+recoil,80,92+bob+recoil,(73,69,65))
    _disc(p,w,h,64,61+bob+recoil,17,23,(102,98,90))
    _disc(p,w,h,57,54+bob+recoil,3,4,GLOW); _disc(p,w,h,71,54+bob+recoil,3,4,GLOW)
    _line(p,w,h,56,70+bob+recoil,72,70+bob+recoil,2,BLACK)

def _baby(p,w,h,bob,recoil):
    _disc(p,w,h,64,47+bob+recoil,18,20,(192,154,132))
    _rect(p,w,h,49,65+bob+recoil,79,95+bob+recoil,(143,117,139))
    _disc(p,w,h,58,44+bob+recoil,2,2,BLACK); _disc(p,w,h,70,44+bob+recoil,2,2,BLACK)
    _line(p,w,h,57,58+bob+recoil,71,58+bob+recoil,1,BLOOD)

def _scooter(p,w,h,bob,recoil):
    _line(p,w,h,64,108+bob,64,49+bob+recoil,6,METAL)
    _line(p,w,h,37,47+bob+recoil,91,47+bob+recoil,5,METAL)
    _disc(p,w,h,37,47+bob+recoil,7,7,BLACK); _disc(p,w,h,91,47+bob+recoil,7,7,BLACK)
    _rect(p,w,h,48,75+bob+recoil,80,85+bob+recoil,(80,83,88))

def _gauntlet(p,w,h,bob,recoil):
    _disc(p,w,h,65,89+bob+recoil,30,31,GOLD)
    for i,x in enumerate((43,54,65,76,87)):
        _disc(p,w,h,x,54+bob+recoil-(i%2)*2,8,24,GOLD)
    gems=[(45,(180,35,42)),(55,(45,105,200)),(65,(55,170,90)),(75,(145,65,190)),(85,(225,150,35))]
    for x,c in gems:
        _disc(p,w,h,x,77+bob+recoil,5,5,c)
        _disc(p,w,h,x-1,76+bob+recoil,2,2,(238,238,220))

def _feather(p,w,h,bob,recoil):
    _line(p,w,h,64,110+bob,64,40+bob+recoil,4,WOOD)
    for k in range(7):
        yy=35+bob+recoil+k*6
        _line(p,w,h,64,yy,45+(k%2)*4,yy-8,2,(176,176,164))
        _line(p,w,h,64,yy,83-(k%2)*4,yy-8,2,(176,176,164))
    _disc(p,w,h,64,29+bob+recoil,5,5,PURPLE)

def _sausage(p,w,h,bob,recoil):
    _line(p,w,h,47,93+bob,82,54+bob+recoil,10,(151,66,54))
    _disc(p,w,h,46,94+bob,7,7,(118,52,44)); _disc(p,w,h,83,53+bob+recoil,7,7,(118,52,44))
    _line(p,w,h,58,82+bob,66,72+bob+recoil,1,(214,132,102))

def _toenails(p,w,h,bob,recoil):
    _rect(p,w,h,49,49+bob+recoil,79,91+bob+recoil,GLASS,205)
    _rect(p,w,h,46,43+bob+recoil,82,53+bob+recoil,METAL)
    for x,y in ((55,76),(62,69),(69,80),(72,62),(58,58)):
        _disc(p,w,h,x,y+bob+recoil,3,6,(210,196,160))

def _jandal(p,w,h,bob,recoil):
    _line(p,w,h,44,97+bob,81,51+bob+recoil,12,(46,46,49))
    _line(p,w,h,55,78+bob,70,57+bob+recoil,3,(105,58,82))
    _line(p,w,h,69,57+bob+recoil,79,72+bob+recoil,3,(105,58,82))

DRAW={
    "ZHND":None, "DMST":_staff, "AMUL":_amulet, "VIRS":_virus, "DOLL":_doll,
    "BLOD":_blood, "FEEB":_feeb, "DACR":_baby, "SCOT":_scooter, "GAUN":_gauntlet,
    "FEAT":_feather, "SAUS":_sausage, "TOES":_toenails, "JAND":_jandal
}

PICKUPS={
    "DMST":"WSTA","AMUL":"WAMU","VIRS":"WVIR","DOLL":"WDOL","BLOD":"WBLO","FEEB":"WFEE",
    "DACR":"WDAC","SCOT":"WSCO","GAUN":"WGAU","FEAT":"WFEA","SAUS":"WSAU","TOES":"WTOE","JAND":"WJAN"
}

def _view_sprite(root,prefix,frame):
    w=h=128; p=_canvas(w,h)
    bob=(0,1,3,7,10,6,3,1)[frame]
    recoil=(0,0,2,8,12,7,3,0)[frame]
    sway=(-2,-1,0,2,3,2,0,-1)[frame]
    _hands(p,w,h,bob//2,sway)
    fn=DRAW[prefix]
    if fn is not None:
        fn(p,w,h,bob,recoil)
    if frame in (3,4) and prefix in ("DMST","AMUL","VIRS","DOLL","BLOD","FEEB","DACR","SCOT","FEAT","TOES"):
        _disc(p,w,h,64,18+recoil,8+frame*2,6+frame,GLOW,205)
    _png(root/"sprites"/f"{prefix}{'ABCDEFGH'[frame]}0.png",w,h,p,64,112)

def _pickup(root,viewprefix,pickprefix):
    w=h=80; p=_canvas(w,h)
    # draw centred miniature using same language but without hands
    # temporary scale by rendering into 128 then nearest-neighbour downsample
    big=_canvas(128,128)
    fn=DRAW[viewprefix]
    if fn is not None:
        fn(big,128,128,-12,-8)
    small=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            sx=int(x*128/w); sy=int(y*128/h)
            si=(sy*128+sx)*4; di=(y*w+x)*4
            small[di:di+4]=big[si:si+4]
    _png(root/"sprites"/f"{pickprefix}A0.png",w,h,small,40,72)

def _sam(root,frame):
    w=h=96;p=_canvas(w,h)
    bob=(0,-2,0,2,1,-1,0,1)[frame]; stride=(-8,-4,1,8,7,2,-5,-8)[frame]
    skin=(181,145,112); hair=(79,58,43); hoodie=(67,86,103); jeans=(65,72,82); bag=(82,55,37)
    _disc(p,w,h,48,20+bob,10,11,skin); _disc(p,w,h,47,15+bob,11,7,hair)
    _rect(p,w,h,36,32+bob,60,65+bob,hoodie); _rect(p,w,h,58,37+bob,69,64+bob,bag)
    _line(p,w,h,42,62+bob,40+stride,90,5,jeans); _line(p,w,h,55,62+bob,57-stride,90,5,jeans)
    _png(root/"sprites"/f"SAMR{'ABCDEFGH'[frame]}0.png",w,h,p,48,91)

def _mopoke(root,frame):
    w=h=96;p=_canvas(w,h)
    bob=(0,-1,-2,0,2,1,0,-1)[frame]; spread=(2,5,9,13,15,10,6,3)[frame]
    feather=(27,29,32); pale=(188,183,167); eye=(225,148,47)
    _disc(p,w,h,48,24+bob,12,13,pale)
    _disc(p,w,h,48,53+bob,14,29,feather)
    _line(p,w,h,37,43+bob,22-spread//2,75+bob,6,feather)
    _line(p,w,h,59,43+bob,74+spread//2,75+bob,6,feather)
    _disc(p,w,h,43,22+bob,2,2,eye); _disc(p,w,h,53,22+bob,2,2,eye)
    _png(root/"sprites"/f"MPKE{'ABCDEFGH'[frame]}0.png",w,h,p,48,90)

def _dad_face(root,name,damage=0,look=0):
    w=h=32;p=_canvas(w,h)
    skin=(90-damage*8,108-damage*8,78-damage*6)
    _disc(p,w,h,16,16,13,15,skin)
    _disc(p,w,h,11+look,13,2,2,(210,205,158)); _disc(p,w,h,21+look,13,2,2,(210,205,158))
    _disc(p,w,h,7,18,3,4,BLOOD)
    if damage>0:_disc(p,w,h,23,8,3,3,BLOOD)
    if damage>1:_disc(p,w,h,16,6,4,2,SKIN_DARK)
    if damage>2:_disc(p,w,h,22,22,4,4,BLOOD)
    _line(p,w,h,11,24,21,24,1,(38,38,34))
    _png(root/"graphics"/f"{name}.png",w,h,p,16,28)

def generate_sam_assets(root: Path):
    root=Path(root)
    for prefix in DRAW:
        for i in range(8):
            _view_sprite(root,prefix,i)
    for view,pick in PICKUPS.items():
        _pickup(root,view,pick)
    for i in range(8):
        _sam(root,i); _mopoke(root,i)
    for pain in range(5):
        d=min(3,pain)
        for look in range(3):
            _dad_face(root,f"DADST{pain}{look}",d,(-1,0,1)[look])
        _dad_face(root,f"DADTR{pain}0",d,-2)
        _dad_face(root,f"DADTL{pain}0",d,2)
        _dad_face(root,f"DADOUCH{pain}",min(3,d+1))
        _dad_face(root,f"DADEVL{pain}",d)
        _dad_face(root,f"DADKILL{pain}",d)
    _dad_face(root,"DADGOD0",0); _dad_face(root,"DADDEAD0",3)
    print("Generated Sam and the Mopoke distinct Doom weapon/character sprite pass")


# Extra Doom projectile/ammo sprites for the clean Sam and the Mopoke project.
def _orb(root):
    root=Path(root)
    for i,fr in enumerate("ABCDE"):
        w=h=48;p=_canvas(w,h)
        r=(9,12,15,11,7)[i]
        _disc(p,w,h,24,24,r+5,r+5,(104,52,132),180)
        _disc(p,w,h,24,24,r,r,(230,158,72),235)
        _disc(p,w,h,21,21,max(2,r//3),max(2,r//3),(255,235,175),255)
        _png(root/"sprites"/f"MORB{fr}0.png",w,h,p,24,24)
    w=h=40;p=_canvas(w,h)
    _disc(p,w,h,20,22,13,12,(79,56,92),255)
    _disc(p,w,h,20,19,8,8,(220,154,67),255)
    _png(root/"sprites"/"CHGRA0.png",w,h,p,20,34)

# Extend the public generator after its original definition.
_base_generate_sam_assets = generate_sam_assets
def generate_sam_assets(root: Path):
    _base_generate_sam_assets(root)
    _orb(root)


def _dad_world(root):
    root=Path(root)
    w=h=96
    for i,fr in enumerate("ABCDEFGHIJK"):
        p=_canvas(w,h); bob=(0,-1,1,0,2,0,-1,0,1,2,0)[i]
        _disc(p,w,h,48,20+bob,11,12,(91,108,78))
        _rect(p,w,h,34,32+bob,62,67+bob,(63,70,63))
        _line(p,w,h,39,62+bob,35+(i%3)*4,91,6,(54,58,55))
        _line(p,w,h,57,62+bob,61-(i%3)*4,91,6,(54,58,55))
        _disc(p,w,h,40,18+bob,2,2,(212,205,158))
        _disc(p,w,h,56,18+bob,2,2,(212,205,158))
        _disc(p,w,h,60,28+bob,3,4,BLOOD)
        if i>=5: _disc(p,w,h,35,41+bob,4,5,BLOOD)
        _png(root/"sprites"/f"ZDAD{fr}0.png",w,h,p,48,91)

def _statusbar(root):
    root=Path(root)
    w,h=320,32;p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            edge=34 if y<2 or y>29 else 18
            _set(p,w,h,x,y,(edge+11,edge+9,edge+7),235)
    _png(root/"graphics"/"STBAR.png",w,h,p,0,32)

_prev_generate_sam_assets = generate_sam_assets
def generate_sam_assets(root: Path):
    _prev_generate_sam_assets(root)
    _dad_world(root)
    _statusbar(root)
