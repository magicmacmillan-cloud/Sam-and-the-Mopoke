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
  Spawn: MPKE A 8 A_Look; Loop;
  See: MPKE ABCDEFGH 3 A_Chase; Loop;
  Melee:
    MPKE E 5 A_FaceTarget;
    MPKE F 5 A_CustomMeleeAttack(20);
    Goto See;
  Pain:
    MPKE G 4 A_Pain;
    Goto See;
  Death:
    MPKE H 6;
    MPKE G 6 A_Scream;
    MPKE F 6 A_NoBlocking;
    MPKE E 20 A_MopokeDie;
    Stop;
  }
  action void A_MopokeDie()
  {
    A_Log("The Mopoke folds into the dark. Sam, move!");
    Level.ExitLevel(0, false);
  }
}
