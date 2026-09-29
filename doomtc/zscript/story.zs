class SamStoryHandler : EventHandler {
 bool woke, sawSam, voiceTruth, forestWarn, lincolnTrace, impossible, mallPeak, finale;
 override void WorldTick(){
  if(players[0].mo==null)return;
  double x=players[0].mo.Pos.X;
  if(!woke){woke=true;Console.Printf("Cold... No. I remember this. I died.");}
  if(!sawSam&&x>900){sawSam=true;Console.Printf("Wait... is that... my son? Sam. My boy. Where's Lincoln?");}
  if(!voiceTruth&&x>1250){voiceTruth=true;Console.Printf("Sam, it's me... Dad. Why is he running? ...He only hears that noise. That noise is me.");}
  if(!forestWarn&&x>2400){forestWarn=true;Console.Printf("Those tracks... too neat. Something wants me to follow them.");}
  if(!lincolnTrace&&x>3500){lincolnTrace=true;Console.Printf("Lincoln. You left this for me. Keep moving, mate.");}
  if(!impossible&&x>4550){impossible=true;Console.Printf("This place shouldn't connect to here.");}
  if(!mallPeak&&x>6000){mallPeak=true;Console.Printf("Sam! I saw you. I'm still coming.");}
  if(!finale&&x>7480){finale=true;Console.Printf("Whatever brought me back is waiting ahead.");}
 }
}