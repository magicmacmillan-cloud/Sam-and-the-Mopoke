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
  Spawn: SAMR ABCDEFGH 2 A_Wander; Loop;
  See: SAMR ABCDEFGH 2 A_Wander; Loop;
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
    A_Log("The Mopoke folds into the dark. The way forward opens.");
    Level.ExitLevel(0, false);
  }
}
