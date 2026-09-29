class SamCharge : Ammo
{
  Default
  {
    Inventory.MaxAmount 100;
    Ammo.BackpackAmount 20;
    Ammo.BackpackMaxAmount 200;
    Inventory.PickupMessage "Cursed charge.";
    Inventory.Icon "CHGRA0";
  }
  States { Spawn: CHGR A -1; Stop; }
}

class SamCursedBolt : FastProjectile
{
  Default
  {
    Radius 5;
    Height 6;
    Speed 30;
    Damage 11;
    Projectile;
    +RANDOMIZE;
  }
  States
  {
  Spawn: MORB AB 2 Bright; Loop;
  Death:\n    MORB C 0 Bright A_PlaySound("sam/cursefire",CHAN_BODY);\n    MORB CDE 3 Bright;\n    Stop;
  }
}

class SamHeavyBolt : FastProjectile
{
  Default
  {
    Radius 12;
    Height 12;
    Speed 26;
    Damage 65;
    Projectile;
    +RANDOMIZE;
  }
  States
  {
  Spawn: MORB AB 2 Bright; Loop;
  Death:
    MORB C 2 Bright;
    MORB D 0 Bright A_PlaySound("sam/gauntlet",CHAN_BODY);\n    MORB D 0 Bright A_Explode(110, 120, XF_HURTSOURCE, false, 120);
    MORB E 4 Bright;
    Stop;
  }
}

class ZombieHands : Weapon
{
  Default
  {
    Tag "Zombie Hands";
    Inventory.PickupMessage "Your dead hands still work.";
    Weapon.SelectionOrder 5000;
    +WEAPON.MELEEWEAPON;
  }
  States
  {
  Ready:
    ZHND A 2 A_WeaponReady;
    ZHND B 2 A_WeaponReady;
    ZHND A 2 A_WeaponReady;
    Loop;
  Deselect: ZHND A 1 A_Lower; Loop;
  Select: ZHND A 1 A_Raise; Loop;
  Fire:
    ZHND A 0 A_PlaySound("sam/zombiehand",CHAN_WEAPON);
    ZHND B 2;
    ZHND C 2 A_CustomPunch(14, false, 0, "BulletPuff", 82);
    ZHND D 3;
    ZHND E 3;
    Goto Ready;
  }
}

class DemonStaff : Weapon
{
  Default
  {
    Tag "Demon Staff";
    Inventory.PickupMessage "Demon Staff";
    Weapon.SelectionOrder 4000;
    Weapon.AmmoType1 "SamCharge";
    Weapon.AmmoUse1 2;
  }
  States
  {
  Spawn: WSTA A -1; Stop;
  Ready: DMST A 2 A_WeaponReady; DMST B 2 A_WeaponReady; DMST A 2 A_WeaponReady; Loop;
  Deselect: DMST A 1 A_Lower; Loop;
  Select: DMST A 1 A_Raise; Loop;
  Fire:
    DMST A 0 A_PlaySound("sam/stafffire",CHAN_WEAPON);
    DMST B 2;
    DMST C 2 Bright A_FireCustomMissile("SamCursedBolt");
    DMST D 3 Bright;
    DMST E 4;
    Goto Ready;
  }
}

class ForbiddenAmulet : Weapon
{
  Default { Tag "Forbidden Amulet"; Weapon.SelectionOrder 3900; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 2; }
  States
  {
  Spawn: WAMU A -1; Stop;
  Ready: AMUL A 1 A_WeaponReady; Loop;
  Deselect: AMUL A 1 A_Lower; Loop;
  Select: AMUL A 1 A_Raise; Loop;
  Fire:
    AMUL A 0 A_PlaySound("sam/cursefire",CHAN_WEAPON);
    AMUL B 2;
    AMUL C 2 Bright A_FireBullets(7,5,7,5,"BulletPuff");
    AMUL D 4;
    Goto Ready;
  }
}

class ZombieFireVirus : Weapon
{
  Default { Tag "Zombie Fire Virus"; Weapon.SelectionOrder 3800; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 1; }
  States
  {
  Spawn: WVIR A -1; Stop;
  Ready: VIRS A 1 A_WeaponReady; Loop;
  Deselect: VIRS A 1 A_Lower; Loop;
  Select: VIRS A 1 A_Raise; Loop;
  Fire:
    VIRS B 1;
    VIRS C 1 Bright A_FireBullets(2,2,1,7,"BulletPuff");
    VIRS D 2;
    VIRS E 1 Bright A_FireBullets(2,2,1,7,"BulletPuff");
    VIRS F 2;
    Goto Ready;
  }
}

class CursedDoll : Weapon
{
  Default { Tag "Cursed Doll"; Weapon.SelectionOrder 3700; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 3; }
  States
  {
  Spawn: WDOL A -1; Stop;
  Ready: DOLL A 1 A_WeaponReady; Loop;
  Deselect: DOLL A 1 A_Lower; Loop;
  Select: DOLL A 1 A_Raise; Loop;
  Fire:
    DOLL A 0 A_PlaySound("sam/whisper",CHAN_WEAPON);
    DOLL B 3;
    DOLL C 2 Bright A_FireCustomMissile("SamCursedBolt",0,true,0,0);
    DOLL D 5;
    Goto Ready;
  }
}

class BloodOfTimShakomontus : Weapon
{
  Default { Tag "Blood of Tim Shakomontus"; Weapon.SelectionOrder 3600; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 2; }
  States
  {
  Spawn: WBLO A -1; Stop;
  Ready: BLOD A 1 A_WeaponReady; Loop;
  Deselect: BLOD A 1 A_Lower; Loop;
  Select: BLOD A 1 A_Raise; Loop;
  Fire:
    BLOD A 0 A_PlaySound("sam/hitflesh",CHAN_WEAPON);
    BLOD B 2;
    BLOD C 2 Bright A_FireBullets(9,7,9,6,"BulletPuff");
    BLOD D 5;
    Goto Ready;
  }
}

class MagicStatueOfFeeb : Weapon
{
  Default { Tag "Statue of Feeb"; Weapon.SelectionOrder 3500; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 1; }
  States
  {
  Spawn: WFEE A -1; Stop;
  Ready: FEEB A 1 A_WeaponReady; Loop;
  Deselect: FEEB A 1 A_Lower; Loop;
  Select: FEEB A 1 A_Raise; Loop;
  Fire:
    FEEB B 2;
    FEEB C 2 Bright A_FireBullets(1,1,1,18,"BulletPuff");
    FEEB D 4;
    Goto Ready;
  }
}

class SqueezeBabyOfDacron : Weapon
{
  Default { Tag "Squeeze Baby of Dacron"; Weapon.SelectionOrder 3400; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 2; }
  States
  {
  Spawn: WDAC A -1; Stop;
  Ready: DACR A 1 A_WeaponReady; Loop;
  Deselect: DACR A 1 A_Lower; Loop;
  Select: DACR A 1 A_Raise; Loop;
  Fire:
    DACR A 0 A_PlaySound("sam/mopokecry",CHAN_WEAPON);
    DACR B 2;
    DACR C 1 Bright A_FireBullets(4,4,3,5,"BulletPuff");
    DACR D 1 Bright A_FireBullets(4,4,3,5,"BulletPuff");
    DACR E 4;
    Goto Ready;
  }
}

class ScooterWeapon : Weapon
{
  Default { Tag "Scooter"; Weapon.SelectionOrder 3300; +WEAPON.MELEEWEAPON; }
  States
  {
  Spawn: WSCO A -1; Stop;
  Ready: SCOT A 1 A_WeaponReady; Loop;
  Deselect: SCOT A 1 A_Lower; Loop;
  Select: SCOT A 1 A_Raise; Loop;
  Fire:
    SCOT B 2;
    SCOT C 2 A_CustomPunch(28,false,0,"BulletPuff",96);
    SCOT D 3;
    SCOT E 4;
    Goto Ready;
  }
}

class GauntletOfStones : Weapon
{
  Default { Tag "Gauntlet of Stones"; Weapon.SelectionOrder 100; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 8; }
  States
  {
  Spawn: WGAU A -1; Stop;
  Ready: GAUN A 2 A_WeaponReady; GAUN B 2 A_WeaponReady; GAUN A 2 A_WeaponReady; Loop;
  Deselect: GAUN A 1 A_Lower; Loop;
  Select: GAUN A 1 A_Raise; Loop;
  Fire:
    GAUN A 0 A_PlaySound("sam/gauntlet",CHAN_WEAPON);
    GAUN B 3;
    GAUN C 2 Bright;
    GAUN D 0 A_FireCustomMissile("SamHeavyBolt");
    GAUN E 3 Bright;
    GAUN F 4;
    GAUN G 5;
    GAUN H 6;
    Goto Ready;
  }
}

class MopokeFeatherWand : Weapon
{
  Default { Tag "Feather Wand"; Weapon.SelectionOrder 3200; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 1; }
  States
  {
  Spawn: WFEA A -1; Stop;
  Ready: FEAT A 1 A_WeaponReady; Loop;
  Deselect: FEAT A 1 A_Lower; Loop;
  Select: FEAT A 1 A_Raise; Loop;
  Fire:
    FEAT B 1;
    FEAT C 1 Bright A_FireCustomMissile("SamCursedBolt");
    FEAT D 2;
    Goto Ready;
  }
}

class PossessedSausage : Weapon
{
  Default { Tag "Possessed Sausage"; Weapon.SelectionOrder 3100; +WEAPON.MELEEWEAPON; }
  States
  {
  Spawn: WSAU A -1; Stop;
  Ready: SAUS A 1 A_WeaponReady; Loop;
  Deselect: SAUS A 1 A_Lower; Loop;
  Select: SAUS A 1 A_Raise; Loop;
  Fire:
    SAUS B 2;
    SAUS C 2 A_CustomPunch(20,false,0,"BulletPuff",88);
    SAUS D 4;
    Goto Ready;
  }
}

class JarOfDadToenails : Weapon
{
  Default { Tag "Jar of Dad Toenails"; Weapon.SelectionOrder 3000; Weapon.AmmoType1 "SamCharge"; Weapon.AmmoUse1 2; }
  States
  {
  Spawn: WTOE A -1; Stop;
  Ready: TOES A 1 A_WeaponReady; Loop;
  Deselect: TOES A 1 A_Lower; Loop;
  Select: TOES A 1 A_Raise; Loop;
  Fire:
    TOES B 2;
    TOES C 2 Bright A_FireBullets(12,9,11,4,"BulletPuff");
    TOES D 5;
    Goto Ready;
  }
}

class UnholyJandal : Weapon
{
  Default { Tag "Unholy Jandal"; Weapon.SelectionOrder 2900; +WEAPON.MELEEWEAPON; }
  States
  {
  Spawn: WJAN A -1; Stop;
  Ready: JAND A 1 A_WeaponReady; Loop;
  Deselect: JAND A 1 A_Lower; Loop;
  Select: JAND A 1 A_Raise; Loop;
  Fire:
    JAND A 0 A_PlaySound("sam/jandal",CHAN_WEAPON);
    JAND B 2;
    JAND C 2 A_CustomPunch(24,false,0,"BulletPuff",100);
    JAND D 4;
    Goto Ready;
  }
}
