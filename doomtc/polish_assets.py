from pathlib import Path
import math, random
from sam_weapon_assets import _png, _canvas, _set, _disc, _rect, _line

# Final-look pass for Sam and the Mopoke.
# Everything here is original procedural pixel art generated into GZDoom-ready PNGs.
# The goal is a consistent late-90s Doom TC silhouette/palette rather than placeholder primitives.

INK=(15,14,16); SHADOW=(28,24,24); BONE=(205,188,157); BONE_D=(122,101,80)
FLESH=(120,62,52); BLOOD=(124,24,29); DRY=(72,24,22); DEAD=(101,118,86); DEAD_D=(53,66,48)
HAIR=(76,43,31); CLOTH=(64,69,67); DENIM=(51,61,73); LEATHER=(87,54,32)
PURPLE=(111,54,145); VIOLET=(176,74,220); RED=(192,40,48); GREEN=(58,183,76)
BLUE=(60,137,218); GOLD=(198,143,37); ORANGE=(224,109,31); METAL=(104,110,116)

def odisc(p,w,h,x,y,rx,ry,c,outline=INK):
    _disc(p,w,h,x,y,rx+2,ry+2,outline); _disc(p,w,h,x,y,rx,ry,c)

def oline(p,w,h,x0,y0,x1,y1,t,c,outline=INK):
    _line(p,w,h,x0,y0,x1,y1,t+2,outline); _line(p,w,h,x0,y0,x1,y1,t,c)

def ore(p,w,h,x0,y0,x1,y1,c,outline=INK):
    _rect(p,w,h,x0-2,y0-2,x1+2,y1+2,outline); _rect(p,w,h,x0,y0,x1,y1,c)

def fleck(p,w,h,x,y,c,n=8,seed=1):
    rng=random.Random(seed)
    for _ in range(n):
        xx=x+rng.randint(-9,9); yy=y+rng.randint(-9,9)
        _disc(p,w,h,xx,yy,rng.randint(1,2),rng.randint(1,2),c)

def _dead_hand(p,w,h,cx,cy,flip=1,curl=0,attack=0,sleeve=True):
    # sleeve + wrist, broad palm and five distinct fingers with nail highlights.
    if sleeve:
        ore(p,w,h,cx-18,cy+10,cx+18,cy+31,(42,48,59))
        _rect(p,w,h,cx-18,cy+10,cx+18,cy+16,(26,29,36))
    odisc(p,w,h,cx,cy,18,15,DEAD)
    _disc(p,w,h,cx-5*flip,cy-2,7,6,(128,139,100))
    lengths=(17,21,23,20)
    for i,L in enumerate(lengths):
        fx=cx+flip*(-15+i*10)
        top=cy-13-L+curl*(i%2)*3-attack*(3-i)
        oline(p,w,h,fx,cy-10,fx+flip*(i-1)*2,top,4,DEAD)
        _rect(p,w,h,fx-2,top-2,fx+3,top+2,(186,177,137))
    # thumb
    oline(p,w,h,cx+flip*14,cy+1,cx+flip*(27+attack*3),cy-8-curl*3,5,DEAD)
    _disc(p,w,h,cx+flip*27,cy-9-curl*3,3,2,(188,176,135))
    # wounds / knuckle dirt
    _line(p,w,h,cx-7,cy-3,cx+2,cy+1,2,BLOOD)
    _disc(p,w,h,cx+8*flip,cy+5,3,2,DRY)
    fleck(p,w,h,cx,cy,DEAD_D,5,abs(cx*13+cy))

def _weapon_object(p,w,h,kind,bob=0,kick=0,flash=False):
    y=bob-kick
    if kind=="DMST":
        oline(p,w,h,64,112+y,64,42+y,6,(79,49,31))
        odisc(p,w,h,64,34+y,14,13,(72,22,28))
        oline(p,w,h,54,38+y,43,20+y,3,BONE_D); oline(p,w,h,74,38+y,85,20+y,3,BONE_D)
        odisc(p,w,h,64,31+y,5,5,RED)
    elif kind=="AMUL":
        oline(p,w,h,64,103+y,64,56+y,2,GOLD)
        odisc(p,w,h,64,47+y,18,22,GOLD); odisc(p,w,h,64,47+y,12,16,(61,33,70))
        _line(p,w,h,54,47+y,74,47+y,2,VIOLET); _disc(p,w,h,64,47+y,4,4,(240,195,69))
    elif kind=="VIRS":
        ore(p,w,h,52,50+y,76,95+y,(76,84,87)); ore(p,w,h,56,55+y,72,86+y,(56,87,71))
        _rect(p,w,h,57,67+y,71,84+y,(57,181,75)); oline(p,w,h,64,51+y,64,28+y,2,METAL)
        odisc(p,w,h,64,26+y,3,3,GREEN)
    elif kind=="DOLL":
        odisc(p,w,h,64,49+y,15,17,(174,147,126)); ore(p,w,h,49,64+y,79,96+y,(93,60,75))
        oline(p,w,h,52,69+y,38,85+y,4,(174,147,126)); oline(p,w,h,76,69+y,90,85+y,4,(174,147,126))
        _disc(p,w,h,58,46+y,2,2,INK); _disc(p,w,h,70,46+y,2,2,RED); _line(p,w,h,58,57+y,70,57+y,1,BLOOD)
    elif kind=="BLOD":
        ore(p,w,h,51,50+y,77,96+y,(87,62,48)); ore(p,w,h,55,55+y,73,90+y,(113,45,47))
        _rect(p,w,h,56,70+y,72,89+y,(155,25,31)); _rect(p,w,h,55,45+y,73,54+y,METAL)
    elif kind=="FEEB":
        ore(p,w,h,47,82+y,81,98+y,(63,61,61)); odisc(p,w,h,64,64+y,18,23,(116,108,91))
        _disc(p,w,h,57,58+y,3,3,(231,173,66)); _disc(p,w,h,71,58+y,3,3,(231,173,66)); _line(p,w,h,56,74+y,72,74+y,2,INK)
    elif kind=="DACR":
        odisc(p,w,h,64,52+y,18,20,(193,151,129)); ore(p,w,h,49,69+y,79,98+y,(134,96,126))
        _disc(p,w,h,58,49+y,2,2,INK); _disc(p,w,h,70,49+y,2,2,INK); _line(p,w,h,57,62+y,71,62+y,1,BLOOD)
    elif kind=="SCOT":
        oline(p,w,h,64,112+y,64,57+y,6,METAL); oline(p,w,h,37,55+y,91,55+y,5,METAL)
        odisc(p,w,h,37,55+y,7,7,INK); odisc(p,w,h,91,55+y,7,7,INK); ore(p,w,h,47,81+y,81,91+y,(73,78,84))
    elif kind=="GAUN":
        odisc(p,w,h,64,91+y,30,30,GOLD)
        gems=((45,RED),(55,BLUE),(65,GREEN),(75,VIOLET),(85,ORANGE))
        for i,(x,c) in enumerate(gems):
            oline(p,w,h,x,81+y,x,53+y-(i%2)*3,7,GOLD); odisc(p,w,h,x,76+y,5,5,c); _disc(p,w,h,x-1,74+y,1,1,(250,240,210))
    elif kind=="FEAT":
        oline(p,w,h,64,112+y,64,43+y,4,(69,43,29))
        for k in range(7):
            yy=40+y+k*6; c=(147+8*k,100-4*k,164+4*k)
            oline(p,w,h,64,yy,46+(k%2)*3,yy-8,2,c); oline(p,w,h,64,yy,82-(k%2)*3,yy-8,2,c)
        odisc(p,w,h,64,34+y,4,4,VIOLET)
    elif kind=="SAUS":
        oline(p,w,h,46,98+y,84,58+y,10,(149,64,48)); _line(p,w,h,56,87+y,67,75+y,1,(225,133,94))
        _disc(p,w,h,47,98+y,6,6,(104,45,39)); _disc(p,w,h,84,58+y,6,6,(104,45,39))
    elif kind=="TOES":
        ore(p,w,h,48,54+y,80,98+y,(88,108,102)); _rect(p,w,h,51,58+y,77,94+y,(65,81,74))
        ore(p,w,h,46,48+y,82,58+y,METAL)
        for x0,y0 in ((55,80),(63,72),(70,85),(72,65),(58,62)): odisc(p,w,h,x0,y0+y,3,6,(210,195,156))
    elif kind=="JAND":
        oline(p,w,h,43,101+y,84,56+y,12,(45,50,58)); oline(p,w,h,55,83+y,70,63+y,3,(125,63,87)); oline(p,w,h,70,63+y,80,77+y,3,(125,63,87))
    if flash:
        for rr,c in ((18,(90,35,110)),(11,(205,70,220)),(5,(255,222,124))): _disc(p,w,h,64,25+y,rr,rr,c,150 if rr>5 else 255)

def _polish_weapon(root,prefix,frame):
    w=h=128; p=_canvas(w,h)
    bob=(7,4,2,0,2,5,8,12)[frame]
    attack=max(0,3-abs(frame-3)); kick=(0,0,4,12,18,10,4,0)[frame]
    if prefix=="ZHND":
        _dead_hand(p,w,h,36,103+bob,1,curl=frame//3,attack=attack)
        _dead_hand(p,w,h,92,103+bob,-1,curl=(frame+1)//3,attack=attack)
    else:
        # hands sit low and to the sides so held objects are readable and not floating.
        _dead_hand(p,w,h,34,108+bob,1,curl=2 if frame>1 else 1)
        _dead_hand(p,w,h,94,108+bob,-1,curl=2 if frame>1 else 1)
        _weapon_object(p,w,h,prefix,bob//2,kick//2,frame in (3,4) and prefix not in ("SCOT","SAUS","JAND"))
    _png(root/"sprites"/f"{prefix}{'ABCDEFGH'[frame]}0.png",w,h,p,64,112)

def _rot_factor(rot):
    a=(rot-1)*math.pi/4
    return math.sin(a), math.cos(a)

def _mopoke_frame(root,frame,rot):
    # Updated canonical Mopoke: pale beaked mask, huge black eyes, shaggy rust/olive body,
    # long asymmetrical forearms and oversized black claws.
    w=h=112;p=_canvas(w,h); sx,cz=_rot_factor(rot)
    idx="ABCDEFGHIJKLMNO".index(frame)
    bob=(0,-1,0,1,-1,1,0,-2,1,0,0,1,2,4,7)[idx]
    if frame in "LMNO":
        fall="LMNO".index(frame); bx=56+fall*7; by=54+fall*8
        odisc(p,w,h,bx,by,24,18,(61,56,42)); odisc(p,w,h,bx+8,by-9,12,14,(210,179,145))
        _disc(p,w,h,bx+4,by-11,5,6,INK); _disc(p,w,h,bx+13,by-10,5,6,INK)
        oline(p,w,h,bx-18,by+4,bx-40,by+16,6,(30,31,31)); oline(p,w,h,bx+18,by+2,bx+42,by+14,6,(30,31,31))
        _png(root/"sprites"/f"MPKE{frame}{rot}.png",w,h,p,56,99); return
    sway=(0,1,-2,2,-3,3,0,-1,1,0,0,0,0,0,0)[idx]
    bx=56+int(sx*4)+sway; by=49+bob
    # shaggy silhouette
    odisc(p,w,h,bx,by+18,18,27,(73,69,47))
    for k in range(10):
        x=bx-17+k*4; y=by+10+(k%3)*6
        _line(p,w,h,x,y,x+(k%2*2-1)*4,y+28,3,(77,62,43))
    fleck(p,w,h,bx,by+18,(66,93,52),18,idx*31+rot)
    # head and beak mask
    odisc(p,w,h,bx,by-9,15,16,(194,158,127))
    _disc(p,w,h,bx-6,by-12,6,7,INK); _disc(p,w,h,bx+6,by-12,6,7,INK)
    _disc(p,w,h,bx-7,by-13,2,2,(230,221,194)); _disc(p,w,h,bx+5,by-13,2,2,(230,221,194))
    oline(p,w,h,bx,by-5,bx+int(sx*4),by+9,5,(177,137,106))
    # ragged crown
    for k in range(9):
        ang=(k-4)*.35; _line(p,w,h,bx,by-22,bx+int(math.sin(ang)*18),by-29-int(math.cos(ang)*5),2,(83,42,35))
    # arms/claws, attack frames stretch one arm far forward
    attack=frame in "GHI"; reach=32+(18 if attack and frame=="H" else 0)
    leftx=bx-reach+int(sx*4); rightx=bx+reach+int(sx*4)
    oline(p,w,h,bx-10,by+6,leftx,by+28-(10 if attack else 0),6,(49,47,39))
    oline(p,w,h,bx+10,by+6,rightx,by+28-(15 if attack else 0),6,(49,47,39))
    for hx,sgn in ((leftx,-1),(rightx,1)):
        odisc(p,w,h,hx,by+29-(12 if attack else 0),7,6,(23,24,26))
        for f in range(4):
            oline(p,w,h,hx+sgn*(f-1)*2,by+29,hx+sgn*(10+f*2),by+39-f*3,2,(19,20,21))
    # legs
    oline(p,w,h,bx-7,by+39,bx-12,94,6,(58,52,42)); oline(p,w,h,bx+7,by+39,bx+12,94,6,(58,52,42))
    if frame in "JK": _line(p,w,h,bx-12,by+6,bx+13,by+32,3,BLOOD)
    _png(root/"sprites"/f"MPKE{frame}{rot}.png",w,h,p,56,99)

def _goat(root,frame,rot):
    w=h=96;p=_canvas(w,h); idx=ord(frame)-65; sx,_=_rot_factor(rot); bob=(0,-1,0,2,-2,1,0,-2,0,1,2,4,7,9,11)[idx%15]
    if frame in "LMNO":
        odisc(p,w,h,50+idx*2,73,28,12,(116,109,87)); oline(p,w,h,30,65,18,83,4,BONE_D); oline(p,w,h,70,65,83,83,4,BONE_D)
    else:
        odisc(p,w,h,50,55+bob,27,17,(139,132,106)); odisc(p,w,h,66+int(sx*5),42+bob,12,11,(152,141,111))
        # curled horns
        oline(p,w,h,61,37+bob,55,25+bob,3,BONE_D); oline(p,w,h,71,37+bob,80,24+bob,3,BONE_D)
        oline(p,w,h,55,25+bob,48,30+bob,2,BONE); oline(p,w,h,80,24+bob,87,31+bob,2,BONE)
        for x in (34,47,58,70): oline(p,w,h,x,64+bob,x-3+(idx%3)*3,91,4,(83,77,63))
        _disc(p,w,h,70+int(sx*5),40+bob,2,2,RED); fleck(p,w,h,50,55+bob,BLOOD,8,idx*17+rot)
        if frame in "GHI": oline(p,w,h,72,48+bob,89,56+bob,3,BONE)
    _png(root/"sprites"/f"GOAT{frame}{rot}.png",w,h,p,48,91)

def _possum(root,frame,rot):
    w=h=88;p=_canvas(w,h); idx=ord(frame)-65; sx,_=_rot_factor(rot); bob=(0,1,-1,1,-1,0,-2,0,1,0,1,3,5,7,9)[idx%15]
    if frame in "LMNO":
        odisc(p,w,h,48,71,28,10,(83,76,72)); _line(p,w,h,24,72,8,78,2,(141,105,100))
    else:
        odisc(p,w,h,45,63+bob,25,13,(81,78,76)); odisc(p,w,h,64+int(sx*4),57+bob,12,9,(120,110,105))
        _disc(p,w,h,68,54+bob,2,2,RED); _disc(p,w,h,76,59+bob,3,2,(206,163,153))
        for x in (30,42,54,64): oline(p,w,h,x,70+bob,x+(idx%3-1)*3,83,3,(104,91,88))
        oline(p,w,h,22,64+bob,6,70+bob,2,(147,111,108))
        if frame in "GHI": oline(p,w,h,75,60+bob,86,55+bob,2,BONE)
        fleck(p,w,h,45,63+bob,BLOOD,6,idx*19+rot)
    _png(root/"sprites"/f"POSS{frame}{rot}.png",w,h,p,44,84)

def _crow(root,frame,rot):
    w=h=96;p=_canvas(w,h); idx=ord(frame)-65; wing=10+abs((idx%4)-2)*7
    if frame in "LMNO":
        _line(p,w,h,48,60,50,84,4,(32,31,39)); _line(p,w,h,49,78,70,90,2,(32,31,39))
    else:
        odisc(p,w,h,48,48,11,18,(32,31,39)); odisc(p,w,h,51,31,8,8,(38,37,45))
        oline(p,w,h,42,45,18,46-wing,5,(28,27,35)); oline(p,w,h,54,45,78,46-wing,5,(28,27,35))
        for k in range(3): oline(p,w,h,18,46-wing+k*3,8-k*2,34-wing+k*6,2,(24,24,30))
        oline(p,w,h,78,46-wing,88,34-wing,2,(24,24,30)); _disc(p,w,h,55,30,2,2,RED)
        oline(p,w,h,58,32,70,35,2,BONE_D)
        if frame in "GHI": _line(p,w,h,70,35,85,42,3,BLOOD)
    _png(root/"sprites"/f"CROW{frame}{rot}.png",w,h,p,48,86)

def _humanoid(root,prefix,frame,rot,coat,skin=(104,108,89),brute=False,shade=False):
    w=h=104;p=_canvas(w,h); idx=ord(frame)-65; sx,_=_rot_factor(rot); bob=(0,-1,0,2,-2,1,0,-2,0,1,2,4,6,8,10)[idx%15]
    if frame in "LMNO":
        odisc(p,w,h,56+idx*2,82,28+(4 if brute else 0),12,coat); odisc(p,w,h,72,75,10,10,skin)
    elif shade:
        # robe dissolves into wisps
        odisc(p,w,h,52,32+bob,10,12,(30,23,42)); ore(p,w,h,37,42+bob,67,77+bob,(45,28,62))
        for k in range(7): oline(p,w,h,40+k*4,70+bob,34+k*6,94-(k%3)*5,3,(38,24,54))
        _disc(p,w,h,48,31+bob,2,2,VIOLET); _disc(p,w,h,56,31+bob,2,2,VIOLET)
        if frame in "GHI":
            for k in range(5): oline(p,w,h,64,48,89,35+k*7,2,(108,44,146))
    else:
        bw=18+(6 if brute else 0); odisc(p,w,h,52,25+bob,10+(2 if brute else 0),12,skin)
        ore(p,w,h,34-(4 if brute else 0),38+bob,70+(4 if brute else 0),72+bob,coat)
        leg=7+(2 if brute else 0); oline(p,w,h,43,69+bob,40+(idx%3)*4,96,leg,DENIM); oline(p,w,h,61,69+bob,64-(idx%3)*4,96,leg,DENIM)
        reach=14+(12 if frame in "GHI" else 0); oline(p,w,h,37,43+bob,26-reach//2,67+bob,6,skin); oline(p,w,h,67,43+bob,78+reach,62+bob,6,skin)
        _disc(p,w,h,48+int(sx*2),23+bob,2,2,(214,208,165)); _disc(p,w,h,56+int(sx*2),23+bob,2,2,RED)
        fleck(p,w,h,52,50+bob,BLOOD,6,idx*23+rot)
    _png(root/"sprites"/f"{prefix}{frame}{rot}.png",w,h,p,52,97)

def _face(root,name,damage=0,look=0,grin=False,dead=False):
    w=h=42;p=_canvas(w,h); skin=(94-damage*7,111-damage*7,80-damage*5)
    odisc(p,w,h,21,21,16,18,skin)
    # hair and wounds
    for k in range(8): _line(p,w,h,9+k*3,7,7+k*4,2+(k%3),2,HAIR)
    eye=(218,207,159) if not dead else (90,75,65)
    _disc(p,w,h,15+look,18,3,3,eye); _disc(p,w,h,27+look,18,3,3,eye)
    _disc(p,w,h,16+look,18,1,1,INK); _disc(p,w,h,28+look,18,1,1,INK)
    _line(p,w,h,9,23,14,24,2,BLOOD)
    if damage>0:_disc(p,w,h,30,10,4,3,BLOOD)
    if damage>1:_line(p,w,h,18,6,23,13,2,DRY)
    if damage>2:_disc(p,w,h,31,28,4,4,BLOOD)
    if dead: _line(p,w,h,12,18,18,20,2,INK); _line(p,w,h,24,20,30,18,2,INK)
    _line(p,w,h,14,31,28,31 if not grin else 27,2,(36,31,28))
    if grin:
        _rect(p,w,h,16,28,26,31,BONE)
        for x in (18,21,24): _line(p,w,h,x,28,x,31,1,INK)
    _png(root/"graphics"/f"{name}.png",w,h,p,21,37)

def _statusbar(root):
    w,h=320,32;p=_canvas(w,h)
    for y in range(h):
        for x in range(w):
            base=27+(4 if (x//16+y//8)%2 else 0)
            _set(p,w,h,x,y,(base,base-2,base-4),255)
    # metal/rusted frame and three recesses
    for x0,x1 in ((0,80),(80,150),(150,320)):
        _rect(p,w,h,x0,0,x1,2,(87,77,64)); _rect(p,w,h,x0,29,x1,32,(9,9,10))
    for x in range(0,320,20): _disc(p,w,h,x+4,4,1,1,(146,118,73))
    _rect(p,w,h,8,5,72,27,(12,12,13)); _rect(p,w,h,88,5,144,27,(12,12,13)); _rect(p,w,h,151,2,202,30,(13,13,14))
    _png(root/"graphics"/"STBAR.png",w,h,p,0,32)

def _texture(root,name,pal,kind="brick",flat=False,seed=1):
    w=h=64;p=_canvas(w,h); rng=random.Random(seed)
    for y in range(h):
        for x in range(w):
            n=rng.randint(-8,8); c=pal[(x//16+y//16)%len(pal)]
            _set(p,w,h,x,y,tuple(max(0,min(255,v+n)) for v in c))
    if kind=="brick":
        for y in range(0,h,16):
            _rect(p,w,h,0,y,64,y+2,(30,28,27))
            off=8 if (y//16)%2 else 0
            for x in range(-off,64,16): _rect(p,w,h,x,y,x+2,y+16,(35,31,29))
    elif kind=="tile":
        for y in range(0,h,16): _rect(p,w,h,0,y,64,y+2,(35,35,38))
        for x in range(0,w,16): _rect(p,w,h,x,0,x+2,64,(35,35,38))
    elif kind=="wood":
        for x in range(0,w,12): _rect(p,w,h,x,0,x+2,64,(35,25,19))
        for y in range(8,h,16): _line(p,w,h,0,y,64,y,1,(54,38,28))
    elif kind=="books":
        _rect(p,w,h,0,0,64,64,(44,27,22))
        colors=((105,46,39),(54,66,94),(82,71,38),(66,44,75),(101,79,46))
        for row in range(4):
            _rect(p,w,h,0,row*16+14,64,row*16+16,(26,19,17))
            x=1
            while x<63:
                ww=rng.randint(3,6); hh=rng.randint(10,14); c=colors[rng.randrange(len(colors))]
                _rect(p,w,h,x,row*16+14-hh,x+ww,row*16+14,c); x+=ww+1
    elif kind=="bark":
        for x in range(4,64,10): _line(p,w,h,x,0,x+rng.randint(-3,3),64,2,(55,36,24))
        for _ in range(18): _line(p,w,h,rng.randrange(64),rng.randrange(64),rng.randrange(64),rng.randrange(64),1,(29,45,26))
    # grime/cracks
    for _ in range(7):
        x=rng.randrange(64); y=rng.randrange(64)
        _line(p,w,h,x,y,min(63,x+rng.randint(-8,8)),min(63,y+rng.randint(4,14)),1,(31,26,26))
    dest=(root/"flats" if flat else root/"textures")/f"{name}.png"
    _png(dest,w,h,p)

def _prop(root,name,kind,seed=1):
    w=h=96;p=_canvas(w,h)
    if kind=="note":
        ore(p,w,h,24,20,72,78,(194,179,139))
        rng=random.Random(seed)
        for y in range(30,70,9): _line(p,w,h,31,y,65-rng.randint(0,8),y+rng.randint(-1,1),1,(57,68,85))
    elif kind=="bag":
        ore(p,w,h,26,25,70,80,(47,75,113)); odisc(p,w,h,48,48,11,13,(214,155,47)); _line(p,w,h,32,26,40,14,3,LEATHER); _line(p,w,h,64,26,56,14,3,LEATHER)
    elif kind=="crate":
        ore(p,w,h,20,27,76,82,(116,72,38)); _line(p,w,h,23,30,73,79,4,(72,41,25)); _line(p,w,h,73,30,23,79,4,(72,41,25))
    elif kind=="lantern":
        ore(p,w,h,36,38,60,80,(67,56,44)); odisc(p,w,h,48,55,10,17,(226,139,38)); oline(p,w,h,38,38,48,21,2,METAL); oline(p,w,h,58,38,48,21,2,METAL)
    elif kind=="tree":
        oline(p,w,h,48,88,49,34,9,(72,45,28)); oline(p,w,h,48,48,28,22,5,(61,40,26)); oline(p,w,h,50,51,73,26,5,(61,40,26))
        for x,y in ((24,24),(36,17),(55,18),(72,25),(30,37),(68,39)): odisc(p,w,h,x,y,13,10,(38,64,37))
    elif kind=="grave":
        ore(p,w,h,30,28,66,84,(89,88,82)); _rect(p,w,h,35,35,61,39,(55,54,52)); _line(p,w,h,48,47,48,70,3,(55,54,52)); _line(p,w,h,40,55,56,55,3,(55,54,52))
    _png(root/"sprites"/f"{name}A0.png",w,h,p,48,88)

def _finger_key(root,prefix,animal,color):
    w=h=72;p=_canvas(w,h)
    # ring/socket at base
    odisc(p,w,h,36,58,11,9,(86,69,47)); odisc(p,w,h,36,58,5,4,INK)
    # severed animal digit, deliberately stylised and readable rather than realistic gore.
    oline(p,w,h,36,57,35,21,8,color)
    _disc(p,w,h,35,18,7,8,color); _rect(p,w,h,30,12,40,17,BONE)
    if animal=="crow": oline(p,w,h,33,18,24,9,3,INK)
    if animal=="goat": _line(p,w,h,31,12,38,4,2,BONE_D)
    if animal=="possum": _disc(p,w,h,40,21,3,3,(196,135,129))
    _rect(p,w,h,29,43,41,48,BLOOD)
    _png(root/"sprites"/f"{prefix}A0.png",w,h,p,36,64)

def generate_polish_assets(root: Path):
    root=Path(root)
    # full first-person pass
    for prefix in ("ZHND","DMST","AMUL","VIRS","DOLL","BLOD","FEEB","DACR","SCOT","GAUN","FEAT","SAUS","TOES","JAND"):
        for i in range(8): _polish_weapon(root,prefix,i)

    # monster animation sets: A/B idle, C-F move, G-I attack, J/K pain, L-O death.
    frames="ABCDEFGHIJKLMNO"
    for fr in frames:
        for rot in range(1,9):
            _mopoke_frame(root,fr,rot)
            _goat(root,fr,rot); _possum(root,fr,rot); _crow(root,fr,rot)
            _humanoid(root,"CGHL",fr,rot,(84,63,45),(126,117,94))
            _humanoid(root,"HUSK",fr,rot,(195,92,31),(81,100,81))
            _humanoid(root,"BRUT",fr,rot,(125,36,33),(104,101,83),brute=True)
            _humanoid(root,"SHAD",fr,rot,(45,28,62),(58,48,67),shade=True)

    # HUD mugshot family
    for pain in range(5):
        for look in range(3): _face(root,f"DADST{pain}{look}",min(3,pain),(-1,0,1)[look])
        _face(root,f"DADTR{pain}0",min(3,pain),-2)
        _face(root,f"DADTL{pain}0",min(3,pain),2)
        _face(root,f"DADOUCH{pain}",min(3,pain+1))
        _face(root,f"DADEVL{pain}",min(3,pain),0,True)
        _face(root,f"DADKILL{pain}",min(3,pain),0,True)
    _face(root,"DADGOD0",0,0,True); _face(root,"DADDEAD0",3,0,False,True)
    _statusbar(root)

    # Keys
    _finger_key(root,"GKEY","goat",(149,127,98)); _finger_key(root,"CKEY","crow",(67,64,75)); _finger_key(root,"PKEY","possum",(154,116,106))

    # story/environment props
    for name,kind,seed in (
        ("SBAG","bag",1),("SNOT","note",2),("LNOT","note",3),("FNOT","note",4),
        ("LOOT","crate",5),("LANT","lantern",6),("TREE","tree",7),("GRAV","grave",8)
    ): _prop(root,name,kind,seed)

    # core location texture sets
    specs=[
      ("HSWALL1",((104,73,57),(84,57,45)),"wood",False,11),
      ("BATHWAL",((170,116,127),(132,86,99)),"tile",False,12),
      ("EXTWALL",((125,58,42),(92,43,33)),"brick",False,13),
      ("PLAYWAL",((55,70,94),(42,55,76)),"tile",False,14),
      ("FORWALL",((73,57,38),(42,62,37)),"bark",False,15),
      ("CEMWALL",((92,91,85),(64,67,64)),"brick",False,16),
      ("TOMBWALL",((79,72,64),(55,51,48)),"brick",False,17),
      ("STNWALL",((99,112,116),(58,70,78)),"tile",False,18),
      ("MALLWAL",((136,130,122),(86,92,104)),"tile",False,19),
      ("LIBWALL",((82,49,39),(50,34,31)),"books",False,20),
      ("VOIDWAL",((47,28,64),(27,22,46)),"tile",False,21),
      ("HSFLOOR",((89,62,43),(61,42,31)),"wood",True,31),
      ("BATHFLR",((124,93,98),(77,67,71)),"tile",True,32),
      ("DIRTFLR",((74,57,39),(54,46,33)),"tile",True,33),
      ("GRASSFL",((45,66,38),(34,53,33)),"tile",True,34),
      ("CEMFLR",((72,70,65),(53,52,49)),"tile",True,35),
      ("TOMBFLR",((67,58,52),(46,43,40)),"tile",True,36),
      ("STNFLR",((82,86,88),(56,62,67)),"tile",True,37),
      ("MALLFLR",((123,113,104),(82,85,92)),"tile",True,38),
      ("LIBFLR",((75,50,39),(48,38,34)),"wood",True,39),
      ("HSCEL",((96,91,81),(76,73,67)),"tile",True,40),
      ("STNCEL",((83,87,91),(60,66,72)),"tile",True,41),
      ("VOIDFLR",((52,34,66),(32,27,48)),"tile",True,42),
    ]
    for spec in specs:_texture(root,*spec)

    # The original first-pass generator created rotation-0 Mopoke frames. The polished
    # boss uses real 8-direction sprites, so remove those legacy lumps to avoid a mixed
    # rotation set being selected by GZDoom.
    for fr in "ABCDEFGH":
        old=root/"sprites"/f"MPKE{fr}0.png"
        if old.exists(): old.unlink()

    print("Generated final-look weapon, enemy, HUD, key, prop and environment pass")
