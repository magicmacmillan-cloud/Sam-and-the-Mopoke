class SamColaClue : CustomInventory {
 Default { Inventory.PickupMessage "A crushed cola can. Sam always leaves these."; +INVENTORY.ALWAYSPICKUP; }
 States { Spawn: SMCL A -1; Stop; Pickup: TNT1 A 0 A_Log("Fresh. Sam was here."); Stop; }
}
class SamMudPrint : Actor { Default { Radius 6; Height 1; +NOBLOCKMAP +NOINTERACTION; } States { Spawn: SMFP ABCD 12; Stop; } }
class SamWallNote : CustomInventory {
 Default { Scale 0.24; Inventory.PickupMessage "A note in Sam's writing."; +INVENTORY.ALWAYSPICKUP; }
 States { Spawn: SMNT A -1; Stop; Pickup: TNT1 A 0 A_Log("SAM: Dad? Don't come this way."); Stop; }
}
class SamBackpackClue : CustomInventory {
 Default { Inventory.PickupMessage "Sam's backpack strap. Fresh mud."; +INVENTORY.ALWAYSPICKUP; }
 States { Spawn: SMCL A -1; Stop; Pickup: TNT1 A 0 A_Log("Sam was here. He was moving fast."); Stop; }
}
class FalseSamTrail : Actor { Default { Radius 4; Height 1; Scale 0.20; +NOBLOCKMAP +NOINTERACTION; } States { Spawn: FMSG A -1; Stop; } }