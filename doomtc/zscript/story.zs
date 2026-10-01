class SamStoryHandler : EventHandler
{
  int lastLevel;
  bool beatA;
  bool beatB;
  bool beatC;

  void StartMapBeat(int n)
  {
    switch(n)
    {
      case 1:
        Console.Printf("Cold grass... the backyard. Wait... Sam?");
        break;
      case 2:
        Console.Printf("He's ahead. Don't scare him again. Just keep moving.");
        break;
      case 3:
        Console.Printf("Black-gums. Every path looks like the last one. Watch the landmarks.");
        break;
      case 4:
        Console.Printf("Graves, paths, locked stone. Sam has to be close.");
        break;
      case 5:
        Console.Printf("Those carved sockets are deliberate. The fingers belong somewhere.");
        break;
      case 6:
        Console.Printf("SAM: ...Dad?");
        Console.Printf("ADAM: Yeah, mate. It's me. Lincoln -- is he with you?");
        Console.Printf("SAM: I don't know. Just don't leave me.");
        break;
      case 7:
        Console.Printf("He's staying with me now. Whatever happens, get Sam through.");
        break;
      case 8:
        Console.Printf("The shelves are moving. Remember the routes. Keep Sam close.");
        break;
    }
  }

  override void WorldTick()
  {
    if(players[0].mo == null) return;

    int n = level.levelnum;
    double x = players[0].mo.Pos.X;\n    double y = players[0].mo.Pos.Y;

    if(n != lastLevel)
    {
      lastLevel = n;
      beatA = false;
      beatB = false;
      beatC = false;
      StartMapBeat(n);
    }

    if(n == 1)
    {
      if(!beatA && y < 1380)
      {
        beatA = true;
        Console.Printf("Sam! Wait! ...He only hears the zombie noise.");
      }
      if(!beatB && y < 100)
      {
        beatB = true;
        Console.Printf("He's through the front door. He's running west up Arnold Street.");
      }
      if(!beatC && x < -1540 && y < -680)
      {
        beatC = true;
        Console.Printf("There -- the playground beside the reserve. Sam ran straight off Arnold into it.");
      }
    }
    else if(n == 2)
    {
      if(!beatA && x > 1000)
      {
        beatA = true;
        Console.Printf("There -- behind the equipment. Sam!");
      }
    }
    else if(n == 3)
    {
      if(!beatA && x > 900)
      {
        beatA = true;
        Console.Printf("Those tracks are too neat. Something wants me to follow them.");
      }
      if(!beatB && x > 1650)
      {
        beatB = true;
        Console.Printf("That shape between the trees... Mopoke.");
      }
      if(!beatC && x > 2050)
      {
        beatC = true;
        Console.Printf("Sam's trail is real here. Fresh mud. Torn strap.");
      }
    }
    else if(n == 4)
    {
      if(!beatA && x > 1450)
      {
        beatA = true;
        Console.Printf("I can hear him breathing. Sam's hiding somewhere close.");
      }
      if(!beatB && x > 1950)
      {
        beatB = true;
        Console.Printf("He ran again. Not because he hates me. Because he still sees a monster.");
      }
    }
    else if(n == 5)
    {
      if(!beatA && x > 900)
      {
        beatA = true;
        Console.Printf("Goat. Crow. Possum. The carvings match the fingers.");
      }
      if(!beatB && x > 1650)
      {
        beatB = true;
        Console.Printf("Lincoln's marks again. He knew this route before I did.");
      }
    }
    else if(n == 6)
    {
      if(!beatA && x > 700)
      {
        beatA = true;
        Console.Printf("SAM: I can understand you now... sort of.");
      }
      if(!beatB && x > 1750)
      {
        beatB = true;
        Console.Printf("ADAM: Stay behind me. If we get split up, keep moving to the lights.");
      }
    }
    else if(n == 7)
    {
      if(!beatA && x > 1200)
      {
        beatA = true;
        Console.Printf("SAM: Dad... something's following us through the shops.");
      }
      if(!beatB && x > 2600)
      {
        beatB = true;
        Console.Printf("No more chasing clues. We are getting out together.");
      }
    }
    else if(n == 8)
    {
      if(!beatA && x > 900)
      {
        beatA = true;
        Console.Printf("Same shelves. Different way out. The library is folding back on itself.");
      }
      if(!beatB && x > 1750)
      {
        beatB = true;
        Console.Printf("Mopoke is here. Don't stop.");
      }
      if(!beatC && x > 3150)
      {
        beatC = true;
        Console.Printf("Use what we learned. Open the route, protect Sam, then move.");
      }
    }
  }
}
