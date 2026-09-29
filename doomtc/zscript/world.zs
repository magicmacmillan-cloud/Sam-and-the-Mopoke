class MopokeShambler : Actor {
 Default { Health 45; Speed 8; Radius 20; Height 56; Monster; +FLOORCLIP; PainChance 150; }
 States { Spawn: MZOM A 10 A_Look; Loop; See: MZOM ABCDEFGH 4 A_Chase; Loop; Melee: MZOM E 3 A_FaceTarget; MZOM FG 3 A_CustomMeleeAttack(7); Goto See; Pain: MZOM A 4 A_Pain; Goto See; Death: MZOM H 6 A_NoBlocking; Stop; }
}
class UndeadGoat : Actor {
 Default { Health 90; Speed 13; Radius 24; Height 48; Monster; +FLOORCLIP; }
 States { Spawn: GOAT A 10 A_Look; Loop; See: GOAT ABCDEFGH 3 A_Chase; Loop; Melee: GOAT DE 2 A_FaceTarget; GOAT FG 2 A_CustomMeleeAttack(12); Goto See; Pain: GOAT A 3 A_Pain; Goto See; Death: GOAT H 6 A_NoBlocking; Stop; }
}
class DyingSurvivor : Actor {
 Default { Radius 16; Height 32; +USESPECIAL; }
 States { Spawn: SURV A -1; Stop; }
 override bool Used(Actor u){ if(u&&u.player){A_Log("Kid with a backpack? Cemetery. Don't follow the crying.");return true;} return false; }
}
class SamHealth : Health { Default { Inventory.Amount 10; Inventory.PickupMessage "Something still sealed. Good enough."; } States { Spawn: LOOT A -1; Stop; } }
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
  Destroy(); return true;
 }
}
class CupboardCache : SearchableCache { Default { Tag "Cupboard"; } }
class LockerCache : SearchableCache { Default { Tag "Locker"; } }
class BinCache : SearchableCache { Default { Tag "Bin"; } }
class GraveCache : SearchableCache { Default { Tag "Disturbed Grave"; } }
class AbandonedCarCache : SearchableCache { Default { Tag "Abandoned Car"; } }
class VendingCache : SearchableCache { Default { Tag "Vending Machine"; } }
class SamMessage : Actor { Default { Radius 10; Height 24; +USESPECIAL +NOBLOCKMAP; } States { Spawn: SMSG A -1; Stop; } override bool Used(Actor u){A_Log("SAM: DAD? DON'T COME THIS WAY.");return true;} }
class FalseMessage : Actor { Default { Radius 10; Height 24; +USESPECIAL +NOBLOCKMAP; } States { Spawn: FMSG A -1; Stop; } override bool Used(Actor u){A_Log("IT KNOWS YOU ARE FOLLOWING.");return true;} }
class LincolnMessage : Actor {
 Default { Radius 10; Height 24; +USESPECIAL +NOBLOCKMAP; }
 States { Spawn: LNTE A -1; Stop; }
 override bool Used(Actor u){
  if(!u||!u.player)return false; int r=Random[lincolnnote](0,4);
  if(r==0) A_Log("LINCOLN: Dad, if you find this, Sam went ahead.");
  else if(r==1) A_Log("LINCOLN: Sam said not to follow the crying.");
  else if(r==2) A_Log("LINCOLN: Dad? We were here. I don't know where this place goes.");
  else if(r==3) A_Log("LINCOLN: The hallway changed. Sam saw it too.");
  else A_Log("LINCOLN: I'm going to find Sam. Please find us.");
  return true;
 }
}