class SamRunner : Actor
{
  Default
  {
    Radius 14;
    Height 54;
    Speed 13;
    +NOBLOCKMAP;
    +FRIENDLY;
  }
  States
  {
  Spawn:
    SAMS A 8 A_Wander;
    SAMW ABCDEF 3 A_Wander;
    Loop;
  See:
    SAMR ABCDEF 2 A_Wander;
    SAML ABC 2 A_Wander;
    SAMR ABCDEF 2 A_Wander;
    SAML DEF 2 A_Wander;
    Loop;
  LookBack:
    SAML ABCDEF 3 A_Wander;
    Goto See;
  Scared:
    SAMS ABCD 4;
    Goto See;
  Hurt:
  Pain:
    SAMH ABCD 3;
    Goto See;
  Exhausted:
    SAME ABCD 5;
    Goto See;
  Crouch:
    SAMC ABCD 5;
    Goto See;
  Walk:
    SAMW ABCDEF 3 A_Wander;
    Goto See;
  Turn:
    SAMT ABCD 4;
    Goto See;
  Fall:
    SAMF ABCDEF 5;
    Goto See;
  Death:
    SAMF ABCDEF 5;
    Stop;
  }
}

class SamHiding : Actor
{
  Default
  {
    Radius 12;
    Height 42;
    +NOBLOCKMAP;
    +USESPECIAL;
    Tag "Sam";
  }
  States { Spawn: SAMC A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_Log("SAM: Stay away! You're not my dad!");
    A_Log("ADAM: Sam... it's me. Please.");
    A_Log("Only a broken zombie noise comes out.");
    A_PlaySound("sam/samfar", CHAN_VOICE);
    Destroy();
    return true;
  }
}

class SamCompanion : Actor
{
  Default
  {
    Health 250;
    Radius 12;
    Height 52;
    Speed 15;
    PainChance 120;
    Monster;
    +FRIENDLY;
    +NOBLOCKMONST;
    +LOOKALLAROUND;
    +NOTARGETSWITCH;
    Tag "Sam";
  }

  override void BeginPlay()
  {
    Super.BeginPlay();
    if(players[0].mo != null) SetFriendPlayer(players[0]);
  }

  States
  {
  Spawn:
    SAMW ABCDEF 4 A_Look;
    Loop;
  See:
    SAMR ABCDEF 3 A_Chase;
    Loop;
  Pain:
    SAMH ABCD 3 A_Pain;
    Goto See;
  Death:
    SAMF ABCDEF 5;
    SAMC A 35;
    Goto Spawn;
  }
}

class MopokeGlimpse : Actor
{
  Default
  {
    Radius 1;
    Height 1;
    +NOBLOCKMAP;
    +NOINTERACTION;
    RenderStyle "Translucent";
    Alpha 0.72;
  }
  States
  {
  Spawn:
    MPKE A 24;
    MPKE B 8;
    MPKE A 10;
    TNT1 A -1;
    Stop;
  }
}

class TheMopoke : Actor
{
  Default
  {
    Health 520;
    Radius 25;
    Height 80;
    Speed 15;
    Monster;
    +FLOORCLIP;
  }
  States
  {
  Spawn:
    MPKE AB 8 A_Look;
    Loop;
  See:
    MPKE CDEF 4 A_Chase;
    Loop;
  Melee:
    MPKE G 5 A_FaceTarget;
    MPKE H 4 A_CustomMeleeAttack(20);
    MPKE I 5;
    Goto See;
  Pain:
    MPKE JK 4 A_Pain;
    Goto See;
  Death:
    MPKE L 6 A_Scream;
    MPKE M 6;
    MPKE N 6 A_NoBlocking;
    MPKE O 20 A_MopokeDie;
    Stop;
  }
  action void A_MopokeDie()
  {
    A_Log("The Mopoke folds into the dark. Sam, move!");
    Level.ExitLevel(0, false);
  }
}


class SamEscapeRunner : Actor
{
  int waypoint;
  Default
  {
    Radius 10; Height 48; Speed 9;
    +NOBLOCKMAP +NOCLIP +NOGRAVITY +NOINTERACTION +FRIENDLY;
    Tag "Sam";
  }
  override void Tick()
  {
    Super.Tick();
    if(level.levelnum != 1) { Vel.X=0; Vel.Y=0; return; }
    double tx; double ty;
    switch(waypoint)
    {
      case 0: tx=620; ty=1210; break; // long sunroom
      case 1: tx=620; ty=1090; break; // laundry
      case 2: tx=520; ty=1060; break; // kitchen
      case 3: tx=410; ty=960; break;  // hallway
      case 4: tx=410; ty=820; break;
      case 5: tx=410; ty=620; break;
      case 6: tx=410; ty=500; break;  // entry
      case 7: tx=410; ty=360; break;  // front door
      case 8: tx=410; ty=120; break;  // front path
      case 9: tx=410; ty=-430; break; // Arnold Street
      case 10: tx=-420; ty=-430; break;
      case 11: tx=-980; ty=-430; break;
      case 12: tx=-1280; ty=-560; break;
      case 13: tx=-1600; ty=-760; break;
      case 14: tx=-1920; ty=-900; break;
      default: Destroy(); return;
    }
    double dx=tx-Pos.X; double dy=ty-Pos.Y; double d=sqrt(dx*dx+dy*dy);
    if(d<24) { waypoint++; Vel.X=0; Vel.Y=0; return; }
    Vel.X=dx/d*Speed; Vel.Y=dy/d*Speed; Vel.Z=0;
  }
  States { Spawn: SAMR ABCDEF 3; Loop; }
}

class HouseDoorbell : Actor
{
  Default { Radius 5; Height 16; Scale 0.45; +USESPECIAL +NOBLOCKMAP; Tag "Doorbell"; }
  States { Spawn: DBEL A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_PlaySound("sam/doorbell",CHAN_BODY);
    A_Log("The doorbell rings inside the empty house.");
    return true;
  }
}

class HouseStreetLamp : Actor
{ Default { Radius 7; Height 104; +SOLID; } States { Spawn: STLP A -1; Stop; } }

class HouseTree : Actor
{ Default { Radius 18; Height 96; +SOLID; } States { Spawn: TREE A -1; Stop; } }

class HouseTree2 : Actor
{ Default { Radius 17; Height 112; +SOLID; } States { Spawn: TRE2 A -1; Stop; } }

class HouseCarLight : Actor
{ Default { Radius 34; Height 30; +SOLID; } States { Spawn: CARW A -1; Stop; } }

class HouseCarDark : Actor
{ Default { Radius 34; Height 30; +SOLID; } States { Spawn: CARD A -1; Stop; } }

class ParkBench42 : Actor
{ Default { Radius 20; Height 24; +SOLID; } States { Spawn: BNCH A -1; Stop; } }

class ParkSwing42 : Actor
{ Default { Radius 24; Height 72; +SOLID; } States { Spawn: SWNG A -1; Stop; } }

class ParkSlide42 : Actor
{ Default { Radius 22; Height 60; +SOLID; } States { Spawn: SLID A -1; Stop; } }

class ParkClimber42 : Actor
{ Default { Radius 22; Height 54; +SOLID; } States { Spawn: CLMB A -1; Stop; } }

class HouseWheelieBin : Actor
{ Default { Radius 8; Height 32; +SOLID; } States { Spawn: WBIN A -1; Stop; } }

class HouseHiluxWorkmate : Actor
{ Default { Radius 34; Height 40; +SOLID; Tag "Hilux Workmate"; } States { Spawn: HILX A -1; Stop; } }

class HouseBinRed : Actor
{ Default { Radius 8; Height 32; +SOLID; } States { Spawn: BINR A -1; Stop; } }

class HouseBinYellow : Actor
{ Default { Radius 8; Height 32; +SOLID; } States { Spawn: BINY A -1; Stop; } }

class HouseShrub : Actor
{ Default { Radius 10; Height 28; } States { Spawn: SHRB A -1; Stop; } }

class DogDigEvidence : Actor
{
  Default { Radius 12; Height 8; +USESPECIAL +NOBLOCKMAP; Tag "Disturbed ground"; }
  States { Spawn: DOGD A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_Log("Fresh dirt. Scratches under the fence. The dog dug through here.");
    return true;
  }
}


class LincolnPhone42 : Actor
{
  Default { Radius 5; Height 3; +USESPECIAL +NOBLOCKMAP; Tag "Lincoln's phone"; }
  States { Spawn: PHON A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_Log("LINCOLN: Sam ran away to the park. I'm going after him. I've locked the doors behind us so it can't get us. If it's really still you, Dad, help us stay safe.");
    if(!u.FindInventory("LincolnPhoneRead")) u.GiveInventory("LincolnPhoneRead",1);
    return true;
  }
}

class FrontDoorPuzzleNote : Actor
{
  Default { Radius 3; Height 6; Scale 0.30; +USESPECIAL +NOBLOCKMAP; Tag "Note taped to the inside of the front door"; }
  States { Spawn: FDNT A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    if(!u.FindInventory("LincolnPhoneRead"))
    {
      A_Log("A note is taped to the inside of the front door. I should check Lincoln's room first.");
      return true;
    }
    A_Log("LINCOLN: I've hidden the key in Sam's puzzle box. Code is: e-scooters, Xbox, eggs, projector.");
    if(!u.FindInventory("FrontDoorNoteRead")) u.GiveInventory("FrontDoorNoteRead",1);
    return true;
  }
}

class HousePuzzleBox : Actor
{
  Default { Radius 10; Height 10; +USESPECIAL +NOBLOCKMAP; Tag "Sam's puzzle box"; }
  States { Spawn: PBOX A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    if(!u.FindInventory("FrontDoorNoteRead"))
      A_Log("Sam's puzzle box. Four number buttons. I don't know what to enter yet.");
    else
      A_Log("Sam's puzzle box. Four digits. Use the numbered buttons beside it.");
    return true;
  }
}

class PuzzleDigitBase : Actor
{
  Default { Radius 3; Height 8; +USESPECIAL +NOBLOCKMAP; }
  bool PressDigit(Actor u, int d)
  {
    if(!u || !u.player) return false;
    if(!u.FindInventory("FrontDoorNoteRead"))
    {
      A_Log("The keypad means nothing to me yet.");
      return true;
    }
    if(u.FindInventory("HouseFrontDoorKey"))
    {
      A_Log("The puzzle box is already open.");
      return true;
    }

    bool a = u.FindInventory("PuzzleStep1") != null;
    bool b = u.FindInventory("PuzzleStep2") != null;
    bool c = u.FindInventory("PuzzleStep3") != null;

    if(!a && !b && !c && d==2)
    {
      u.GiveInventory("PuzzleStep1",1);
      A_Log("2 _ _ _");
      return true;
    }
    if(a && !b && !c && d==3)
    {
      u.TakeInventory("PuzzleStep1",99);
      u.GiveInventory("PuzzleStep2",1);
      A_Log("2 3 _ _");
      return true;
    }
    if(!a && b && !c && d==3)
    {
      u.TakeInventory("PuzzleStep2",99);
      u.GiveInventory("PuzzleStep3",1);
      A_Log("2 3 3 _");
      return true;
    }
    if(!a && !b && c && d==0)
    {
      u.TakeInventory("PuzzleStep3",99);
      u.GiveInventory("HouseFrontDoorKey",1);
      A_PlaySound("sam/key",CHAN_ITEM);
      A_Log("2 3 3 0. Click. Sam's puzzle box opens. The front-door key is inside.");
      return true;
    }

    u.TakeInventory("PuzzleStep1",99);
    u.TakeInventory("PuzzleStep2",99);
    u.TakeInventory("PuzzleStep3",99);
    if(d==2)
    {
      u.GiveInventory("PuzzleStep1",1);
      A_Log("2 _ _ _");
    }
    else A_Log("Wrong. The puzzle box resets.");
    return true;
  }
}

class PuzzleDigit0 : PuzzleDigitBase { States { Spawn: D0BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,0); } }
class PuzzleDigit1 : PuzzleDigitBase { States { Spawn: D1BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,1); } }
class PuzzleDigit2 : PuzzleDigitBase { States { Spawn: D2BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,2); } }
class PuzzleDigit3 : PuzzleDigitBase { States { Spawn: D3BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,3); } }
class PuzzleDigit4 : PuzzleDigitBase { States { Spawn: D4BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,4); } }
class PuzzleDigit5 : PuzzleDigitBase { States { Spawn: D5BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,5); } }
class PuzzleDigit6 : PuzzleDigitBase { States { Spawn: D6BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,6); } }
class PuzzleDigit7 : PuzzleDigitBase { States { Spawn: D7BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,7); } }
class PuzzleDigit8 : PuzzleDigitBase { States { Spawn: D8BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,8); } }
class PuzzleDigit9 : PuzzleDigitBase { States { Spawn: D9BT A -1; Stop; } override bool Used(Actor u){ return PressDigit(u,9); } }

class GarageEScooter42 : Actor
{
  Default { Radius 8; Height 34; +NOBLOCKMAP; Tag "E-scooter"; }
  States { Spawn: ESCO A -1; Stop; }
}

class LoungeXboxTV42 : Actor
{
  Default { Radius 8; Height 24; +NOBLOCKMAP; Tag "Xbox and TV"; }
  States { Spawn: XBOX A -1; Stop; }
}

class KitchenFridge42 : Actor
{
  Default { Radius 12; Height 56; +USESPECIAL; Tag "Fridge"; }
  States { Spawn: FRDG A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_Log("Inside the fridge: three eggs.");
    return true;
  }
}

class ProjectorCountdown42 : Actor
{
  Default { Radius 1; Height 1; +NOBLOCKMAP +NOINTERACTION; RenderStyle "Add"; Alpha 0.72; }
  States
  {
  Spawn:
    PJCT A 25 Bright;
    PJCT B 25 Bright;
    PJCT C 25 Bright;
    PJCT D -1 Bright;
    Stop;
  }
}

class MasterProjector42 : Actor
{
  bool activated;
  Default { Radius 6; Height 8; +USESPECIAL +NOBLOCKMAP; Tag "Projector"; }
  States { Spawn: PROJ A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    if(!activated)
    {
      activated=true;
      A_Log("The projector clicks on: 3... 2... 1... 0.");
      Vector3 wallspot = Pos;
      wallspot.X = 118;
      wallspot.Y = 820;
      wallspot.Z = 52;
      Spawn("ProjectorCountdown42",wallspot,ALLOW_REPLACE);
    }
    else A_Log("The projector stays on 0.");
    return true;
  }
}

class SamGateNote42 : Actor
{
  Default { Radius 3; Height 6; Scale 0.30; +USESPECIAL +NOBLOCKMAP; Tag "Sam's note taped to the gate"; }
  States { Spawn: SGNT A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_Log("SAM: I left the key in the neighbour's letterbox.");
    if(!u.FindInventory("GateNoteRead")) u.GiveInventory("GateNoteRead",1);
    return true;
  }
}

class NeighbourLetterbox42 : Actor
{
  bool looted;
  Default { Radius 8; Height 34; +USESPECIAL; Tag "Neighbour's letterbox"; }
  States { Spawn: LBOX A -1; Stop; }
  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    if(!u.FindInventory("GateNoteRead"))
    {
      A_Log("The neighbour's letterbox. No reason to search it.");
      return true;
    }
    if(!looted)
    {
      looted=true;
      u.GiveInventory("PlaygroundGateKey",1);
      A_PlaySound("sam/key",CHAN_ITEM);
      A_Log("A small key is tucked inside. It fits the playground gate padlock.");
    }
    else A_Log("The letterbox is empty now.");
    return true;
  }
}
