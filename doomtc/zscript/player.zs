class SamDad : DoomPlayer
{
  Default
  {
    Player.DisplayName "Dad";
    Player.Face "DAD";
    Player.StartItem "ZombieHands";
    Player.StartItem "SamCharge", 12;
    Player.WeaponSlot 1, "ZombieHands", "PossessedSausage", "UnholyJandal";
    Player.WeaponSlot 2, "DemonStaff", "ForbiddenAmulet";
    Player.WeaponSlot 3, "ZombieFireVirus", "CursedDoll";
    Player.WeaponSlot 4, "BloodOfTimShakomontus", "MagicStatueOfFeeb";
    Player.WeaponSlot 5, "SqueezeBabyOfDacron", "ScooterWeapon";
    Player.WeaponSlot 6, "MopokeFeatherWand";
    Player.WeaponSlot 7, "JarOfDadToenails";
    Player.WeaponSlot 8, "GauntletOfStones";
  }
  States
  {
  Spawn: ZDAD A -1; Stop;
  See: ZDAD ABCD 4; Loop;
  Missile: ZDAD E 8; Goto Spawn;
  Pain: ZDAD F 4; ZDAD F 4 A_Pain; Goto Spawn;
  Death:
    ZDAD G 8;
    ZDAD H 8 A_PlayerScream;
    ZDAD I 8 A_NoBlocking;
    ZDAD J 8;
    ZDAD K -1;
    Stop;
  }
}
