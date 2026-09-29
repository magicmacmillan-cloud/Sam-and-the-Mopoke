class SamRunner : Actor
{
  Default
  {
    Radius 14;
    Height 54;
    +NOBLOCKMAP;
    +NOINTERACTION;
  }
  States
  {
  Spawn: SAMR ABCDEFGH 3; Loop;
  }
}

class TheMopoke : Demon
{
  Default
  {
    Health 350;
    Radius 25;
    Height 60;
    Speed 11;
    PainChance 80;
  }
  States
  {
  Spawn: MPKE A 8 A_Look; Loop;
  See: MPKE ABCDEFGH 4 A_Chase; Loop;
  Melee:
    MPKE E 5 A_FaceTarget;
    MPKE F 5 A_CustomMeleeAttack(18);
    Goto See;
  Pain:
    MPKE G 4;
    MPKE H 4 A_Pain;
    Goto See;
  Death:
    MPKE H 6;
    MPKE G 6 A_Scream;
    MPKE F 6 A_NoBlocking;
    MPKE E -1;
    Stop;
  }
}
