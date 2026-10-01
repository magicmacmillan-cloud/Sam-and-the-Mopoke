class MopokeShambler : Actor {
 Default { Health 45; Speed 8; Radius 20; Height 56; Monster; +FLOORCLIP; PainChance 150; SeeSound "sam/zombie"; }
 States {
  Spawn: SHAM AB 8 A_Look; Loop;
  See: SHAM CDEF 5 A_Chase; Loop;
  Melee: SHAM G 4 A_FaceTarget; SHAM HI 4 A_CustomMeleeAttack(7,"sam/scratch"); Goto See;
  Pain: SHAM JK 3 A_Pain; Goto See;
  Death: SHAM L 5 A_Scream; SHAM M 5; SHAM N 5 A_NoBlocking; SHAM O -1; Stop;
 }
}

class UndeadGoat : Actor {
 Default { Health 90; Speed 13; Radius 24; Height 48; Monster; +FLOORCLIP; SeeSound "sam/goat"; ActiveSound "sam/goat"; }
 States {
  Spawn: GOAT AB 8 A_Look; Loop;
  See: GOAT CDEF 4 A_Chase; Loop;
  Melee: GOAT G 3 A_FaceTarget; GOAT HI 3 A_CustomMeleeAttack(12,"sam/goat"); Goto See;
  Pain: GOAT JK 3 A_Pain; Goto See;
  Death: GOAT L 4 A_Scream; GOAT M 5; GOAT N 5 A_NoBlocking; GOAT O -1; Stop;
 }
}

class RotPossum : Actor {
 Default { Health 38; Speed 16; Radius 18; Height 24; Monster; +FLOORCLIP; PainChance 180; }
 States {
  Spawn: ROTP AB 7 A_Look; Loop;
  See: ROTP CDEF 3 A_Chase; Loop;
  Melee: ROTP G 2 A_FaceTarget; ROTP HI 3 A_CustomMeleeAttack(8,"sam/scratch"); Goto See;
  Pain: ROTP JK 2 A_Pain; Goto See;
  Death: ROTP L 3 A_Scream; ROTP M 4; ROTP N 4 A_NoBlocking; ROTP O -1; Stop;
 }
}

class CursedCrow : Actor {
 Default { Health 26; Speed 18; Radius 14; Height 22; Monster; +NOGRAVITY +FLOAT; PainChance 200; }
 States {
  Spawn: CROW AB 7 A_Look; Loop;
  See: CROW CDEF 3 A_Chase; Loop;
  Melee: CROW G 2 A_FaceTarget; CROW HI 2 A_CustomMeleeAttack(6,"sam/scratch"); Goto See;
  Pain: CROW JK 2 A_Pain; Goto See;
  Death: CROW L 3 A_Scream; CROW M 4; CROW N 4 A_NoBlocking; CROW O -1; Stop;
 }
}

class HuskBolt : FastProjectile {
 Default { Radius 4; Height 4; Speed 22; Damage 7; Projectile; +RANDOMIZE; }
 States { Spawn: MORB AB 2 Bright; Loop; Death: MORB CDE 2 Bright; Stop; }
}

class StationHusk : Actor {
 Default { Health 115; Speed 9; Radius 20; Height 58; Monster; PainChance 100; SeeSound "sam/zombie"; }
 States {
  Spawn: HUSK AB 8 A_Look; Loop;
  See: HUSK CDEF 5 A_Chase; Loop;
  Missile:
   HUSK G 4 A_FaceTarget;
   HUSK H 3 A_CustomMissile("HuskBolt",32,0,0);
   HUSK I 4;
   Goto See;
  Melee: HUSK G 3 A_FaceTarget; HUSK HI 3 A_CustomMeleeAttack(10,"sam/scratch"); Goto See;
  Pain: HUSK JK 3 A_Pain; Goto See;
  Death: HUSK L 5 A_Scream; HUSK M 5; HUSK N 5 A_NoBlocking; HUSK O -1; Stop;
 }
}

class MallBrute : Actor {
 Default { Health 190; Speed 7; Radius 30; Height 64; Monster; Mass 300; PainChance 55; }
 States {
  Spawn: BRUT AB 9 A_Look; Loop;
  See: BRUT CDEF 5 A_Chase; Loop;
  Melee: BRUT G 4 A_FaceTarget; BRUT HI 4 A_CustomMeleeAttack(22,"sam/hitflesh"); Goto See;
  Pain: BRUT JK 3 A_Pain; Goto See;
  Death: BRUT L 6 A_Scream; BRUT M 6; BRUT N 6 A_NoBlocking; BRUT O -1; Stop;
 }
}

class LibraryShade : Actor {
 Default { Health 78; Speed 17; Radius 18; Height 62; Monster; +SHADOW; PainChance 145; }
 States {
  Spawn: SHAD AB 7 A_Look; Loop;
  See: SHAD CDEF 3 A_Chase; Loop;
  Melee: SHAD G 2 A_FaceTarget; SHAD HI 3 A_CustomMeleeAttack(14,"sam/whisper"); Goto See;
  Pain: SHAD JK 2 A_Pain; Goto See;
  Death: SHAD L 4 A_Scream; SHAD M 4; SHAD N 5 A_NoBlocking; SHAD O -1; Stop;
 }
}

class CemeteryGhoul : Actor {
 Default { Health 82; Speed 10; Radius 20; Height 56; Monster; +FLOORCLIP; PainChance 135; SeeSound "sam/zombie"; }
 States {
  Spawn: CGHL AB 8 A_Look; Loop;
  See: CGHL CDEF 5 A_Chase; Loop;
  Melee: CGHL G 4 A_FaceTarget; CGHL HI 4 A_CustomMeleeAttack(11,"sam/scratch"); Goto See;
  Pain: CGHL JK 3 A_Pain; Goto See;
  Death: CGHL L 5 A_Scream; CGHL M 5; CGHL N 5 A_NoBlocking; CGHL O -1; Stop;
 }
}

class TombWisp : Actor {
 Default {
  Health 46; Speed 15; Radius 14; Height 36; Monster;
  +NOGRAVITY +FLOAT +SHADOW;
  PainChance 190;
  RenderStyle "Translucent";
  Alpha 0.72;
 }
 States {
  Spawn: SHAD AB 7 A_Look; Loop;
  See: SHAD CDEF 3 A_Chase; Loop;
  Melee: SHAD G 2 A_FaceTarget; SHAD HI 2 Bright A_CustomMeleeAttack(9,"sam/whisper"); Goto See;
  Pain: SHAD JK 2 Bright A_Pain; Goto See;
  Death: SHAD L 3 Bright A_Scream; SHAD M 4 Bright; SHAD N 4 Bright A_NoBlocking; SHAD O -1 Bright; Stop;
 }
}

class DyingSurvivor : Actor {
 Default { Radius 16; Height 32; +USESPECIAL; }
 States { Spawn: SURV A -1; Stop; }
 override bool Used(Actor u){
  if(u&&u.player){
   A_Log("Kid with a backpack? Cemetery. Don't follow the crying.");
   A_PlaySound("sam/survivor",CHAN_VOICE);
   return true;
  }
  return false;
 }
}

class SamHealth : Health {
 Default { Inventory.Amount 10; Inventory.PickupMessage "Something still sealed. Good enough."; }
 States { Spawn: LOOT A -1; Stop; }
}

class SearchableCache : Actor {
 Default { Radius 18; Height 28; +USESPECIAL; Tag "Search"; }
 States { Spawn: LOOT A -1; Stop; }
 override bool Used(Actor u){
  if(!u||!u.player)return false;
  int r=Random[loot](0,7);
  if(r<=2) A_Log("Empty. Just dust and rubbish.");
  else if(r<=4){u.GiveInventory("SamCharge",4);A_Log("Found cursed charges.");}
  else if(r<=6){u.GiveInventory("SamHealth",1);A_Log("Found something useful.");}
  else {u.GiveInventory("SamCharge",10);A_Log("Rare cache. Something inside is humming.");}
  A_PlaySound("sam/loot",CHAN_ITEM);
  Destroy();
  return true;
 }
}

class CupboardCache : SearchableCache { Default { Tag "Cupboard"; } }
class LockerCache : SearchableCache { Default { Tag "Locker"; } }
class BinCache : SearchableCache { Default { Tag "Bin"; } }
class GraveCache : SearchableCache { Default { Tag "Disturbed Grave"; } }
class AbandonedCarCache : SearchableCache { Default { Tag "Abandoned Car"; } }
class VendingCache : SearchableCache { Default { Tag "Vending Machine"; } }

class SamMessage : Actor {
 Default { Radius 5; Height 12; Scale 0.30; +USESPECIAL +NOBLOCKMAP; }
 States { Spawn: SMSG A -1; Stop; }
 override bool Used(Actor u){A_Log("SAM: DAD? DON'T COME THIS WAY.");return true;}
}

class FalseMessage : Actor {
 Default { Radius 10; Height 24; +USESPECIAL +NOBLOCKMAP; }
 States { Spawn: FMSG A -1; Stop; }
 override bool Used(Actor u){A_Log("IT KNOWS YOU ARE FOLLOWING.");return true;}
}

class LincolnMessage : Actor {
 Default { Radius 10; Height 24; +USESPECIAL +NOBLOCKMAP; }
 States { Spawn: LNTE A -1; Stop; }
 override bool Used(Actor u){
  if(!u||!u.player)return false;
  int r=Random[lincolnnote](0,4);
  if(r==0) A_Log("LINCOLN: Dad, if you find this, Sam went ahead.");
  else if(r==1) A_Log("LINCOLN: Sam said not to follow the crying.");
  else if(r==2) A_Log("LINCOLN: Dad? We were here. I don't know where this place goes.");
  else if(r==3) A_Log("LINCOLN: The hallway changed. Sam saw it too.");
  else A_Log("LINCOLN: I'm going to find Sam. Please find us.");
  return true;
 }
}


