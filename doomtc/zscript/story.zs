class SamStoryHandler : EventHandler
{
  bool woke, sawSam, voiceTruth, forestWarn, lincolnTrace, impossible, mallPeak, finale;
  int musicZone;
  int targetMusicZone;
  int fadeState;
  int fadeTick;

  String MusicForZone(int z)
  {
    switch(z)
    {
      case 0: return "MUSIC02";
      case 1: return "MUSIC03";
      case 2: return "MUSIC04";
      case 3: return "MUSIC05";
      case 4: return "MUSIC05";
      case 5: return "MUSIC06";
      case 6: return "MUSIC07";
      case 7: return "MUSIC08";
      case 8: return "MUSIC09";
    }
    return "MUSIC02";
  }

  int MusicZoneForX(double x)
  {
    if(x > 8050) return 8;
    if(x >= 7488) return 7;
    if(x >= 5952) return 6;
    if(x >= 4544) return 5;
    if(x >= 4256) return 4;
    if(x >= 3520) return 3;
    if(x >= 2432) return 2;
    if(x >= 1344) return 1;
    return 0;
  }

  void UpdateMusic(double x)
  {
    int z = MusicZoneForX(x);
    if(z != targetMusicZone) targetMusicZone = z;

    if(fadeState == 0 && targetMusicZone != musicZone)
    {
      fadeState = 1;
      fadeTick = 0;
    }

    if(fadeState == 1)
    {
      fadeTick++;
      double v = 1.0 - (double(fadeTick) / 35.0);
      if(v <= 0.0 || fadeTick >= 35)
      {
        SetMusicVolume(0.0);
        S_ChangeMusic(MusicForZone(targetMusicZone), 0, true, true);
        musicZone = targetMusicZone;
        fadeState = 2;
        fadeTick = 0;
      }
      else SetMusicVolume(v);
    }
    else if(fadeState == 2)
    {
      fadeTick++;
      double v = double(fadeTick) / 35.0;
      if(v >= 1.0 || fadeTick >= 35)
      {
        SetMusicVolume(1.0);
        fadeState = 0;
        fadeTick = 0;
      }
      else SetMusicVolume(v);
    }
  }

  override void WorldTick()
  {
    if(players[0].mo == null) return;
    double x = players[0].mo.Pos.X;
    UpdateMusic(x);

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
