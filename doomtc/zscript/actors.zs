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
    Radius 10;
    Height 48;
    Speed 10;
    +NOBLOCKMAP;
    +NOCLIP;
    +NOGRAVITY;
    +NOINTERACTION;
    +FRIENDLY;
    Tag "Sam";
  }

  override void Tick()
  {
    Super.Tick();
    if(level.levelnum != 1)
    {
      Vel.X = 0;
      Vel.Y = 0;
      return;
    }

    double tx;
    double ty;
    switch(waypoint)
    {
      case 0:  tx=350;   ty=1330;  break; // backyard -> rear/sunroom door
      case 1:  tx=350;   ty=1240;  break; // inside enclosed rear veranda
      case 2:  tx=455;   ty=1160;  break; // kitchen/rear opening
      case 3:  tx=420;   ty=1060;  break; // kitchen/meals
      case 4:  tx=410;   ty=960;   break; // rear hall opening
      case 5:  tx=410;   ty=760;   break; // central hall
      case 6:  tx=410;   ty=520;   break; // tiled front hall
      case 7:  tx=410;   ty=390;   break; // front entry
      case 8:  tx=410;   ty=345;   break; // through the real front door
      case 9:  tx=410;   ty=120;   break; // front path
      case 10: tx=410;   ty=-420;  break; // Arnold Street
      case 11: tx=-420;  ty=-430;  break; // west/up Arnold
      case 12: tx=-980;  ty=-430;  break; // Arnold/Collenso corner
      case 13: tx=-1280; ty=-560;  break; // cross toward reserve
      case 14: tx=-1540; ty=-690;  break; // playground-side path
      case 15: tx=-1740; ty=-790;  break; // playground entrance
      case 16: tx=-1940; ty=-880;  break; // deep into playground
      default:
        Vel.X=0;
        Vel.Y=0;
        Destroy();
        return;
    }

    double dx=tx-Pos.X;
    double dy=ty-Pos.Y;
    double dist=sqrt(dx*dx+dy*dy);
    if(dist < 24)
    {
      waypoint++;
      Vel.X=0;
      Vel.Y=0;
      return;
    }

    Vel.X=dx/dist*Speed;
    Vel.Y=dy/dist*Speed;
    Vel.Z=0;
  }

  States
  {
  Spawn:
    SAMR ABCDEF 3;
    Loop;
  Gone:
    TNT1 A -1;
    Stop;
  }
}

class HouseDoorbell : Actor
{
  Default
  {
    Radius 5;
    Height 16;
    Scale 0.45;
    +USESPECIAL;
    +NOBLOCKMAP;
    Tag "Doorbell";
  }
  States { Spawn: DBEL A -1; Stop; }

  override bool Used(Actor u)
  {
    if(!u || !u.player) return false;
    A_PlaySound("sam/doorbell", CHAN_BODY);
    A_Log("The doorbell rings inside the empty house.");
    return true;
  }
}


class HouseStreetLamp : Actor
{
  Default { Radius 7; Height 104; +SOLID; +NOBLOCKMAP; }
  States { Spawn: STLP A -1; Stop; }
}

class HouseTree : Actor
{
  Default { Radius 18; Height 96; +SOLID; +NOBLOCKMAP; }
  States { Spawn: TREE A -1; Stop; }
}

class HouseCarLight : Actor
{
  Default { Radius 34; Height 30; +SOLID; +NOBLOCKMAP; }
  States { Spawn: CARW A -1; Stop; }
}

class HouseCarDark : Actor
{
  Default { Radius 34; Height 30; +SOLID; +NOBLOCKMAP; }
  States { Spawn: CARD A -1; Stop; }
}

class ParkBench42 : Actor
{
  Default { Radius 20; Height 24; +SOLID; +NOBLOCKMAP; }
  States { Spawn: BNCH A -1; Stop; }
}

class ParkSwing42 : Actor
{
  Default { Radius 24; Height 72; +SOLID; +NOBLOCKMAP; }
  States { Spawn: SWNG A -1; Stop; }
}

class ParkSlide42 : Actor
{
  Default { Radius 22; Height 60; +SOLID; +NOBLOCKMAP; }
  States { Spawn: SLID A -1; Stop; }
}

class ParkClimber42 : Actor
{
  Default { Radius 22; Height 54; +SOLID; +NOBLOCKMAP; }
  States { Spawn: CLMB A -1; Stop; }
}

class HouseWheelieBin : Actor
{
  Default { Radius 8; Height 32; +SOLID; +NOBLOCKMAP; }
  States { Spawn: WBIN A -1; Stop; }
}
