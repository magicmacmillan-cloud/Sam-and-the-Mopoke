class GoatFinger : Key {
 Default { Inventory.PickupMessage "Goat Finger"; Inventory.Icon "GTFGA0"; Tag "Goat Finger"; }
 States { Spawn: GTFG A -1; Stop; }
}
class CrowFinger : Key {
 Default { Inventory.PickupMessage "Crow Finger"; Inventory.Icon "CRFGA0"; Tag "Crow Finger"; }
 States { Spawn: CRFG A -1; Stop; }
}
class PossumFinger : Key {
 Default { Inventory.PickupMessage "Possum Finger"; Inventory.Icon "PSFGA0"; Tag "Possum Finger"; }
 States { Spawn: PSFG A -1; Stop; }
}

class GoatFingerGate : Actor {
 Default { Radius 30; Height 64; +SOLID +USESPECIAL; Tag "Carved goat-finger door"; }
 States { Spawn: GTGT A -1; Stop; }
 override bool Used(Actor u) {
  if(!u||!u.player)return false;
  if(u.FindInventory("GoatFinger")){
   A_Log("The goat finger fits. Stone grinds open.");
   A_PlaySound("sam/door",CHAN_BODY);
   Destroy();
   return true;
  }
  A_Log("A carved socket. Something finger-shaped is missing.");
  return true;
 }
}
class CrowFingerGate : Actor {
 Default { Radius 30; Height 64; +SOLID +USESPECIAL; Tag "Crow-finger service gate"; }
 States { Spawn: CRGT A -1; Stop; }
 override bool Used(Actor u) {
  if(!u||!u.player)return false;
  if(u.FindInventory("CrowFinger")){
   A_Log("The crow finger turns the mechanism.");
   A_PlaySound("sam/door",CHAN_BODY);
   Destroy();
   return true;
  }
  A_Log("The mechanism has a narrow blackened socket.");
  return true;
 }
}
class PossumFingerGate : Actor {
 Default { Radius 30; Height 64; +SOLID +USESPECIAL; Tag "Possum-finger archive gate"; }
 States { Spawn: PSGT A -1; Stop; }
 override bool Used(Actor u) {
  if(!u||!u.player)return false;
  if(u.FindInventory("PossumFinger")){
   A_Log("The possum finger clicks into place. The archive opens.");
   A_PlaySound("sam/door",CHAN_BODY);
   Destroy();
   return true;
  }
  A_Log("Three brass claws surround an empty finger socket.");
  return true;
 }
}
