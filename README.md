# Sam and the Mopoke

**Sam and the Mopoke** is a standalone Doom II-engine horror game project.

## Runtime format

The Android build ships one game-data file:

`sam-and-the-mopoke.wad`

That file is a real **IWAD** (`IWAD` header), not a PWAD/PK3 mod stack. It contains the custom MAP01, ZScript gameplay, weapons, Zombie Dad player art, Sam/Mopoke actors, finger keys and gates, clues, story logic, textures, sounds, music and HUD resources.

The IWAD is assembled from free/open Freedoom Phase 2 base resources plus original Sam and the Mopoke content. The APK boots it directly with:

`-iwad sam-and-the-mopoke.wad +map MAP01`

No commercial Doom or Doom II data is included.

## Game route

House → playground → forest → cemetery → tomb → station → shopping centre → impossible library.

The current design preserves the established horror/action pacing, Sam pursuit, Lincoln traces, false trails, searchable loot, survivors, the Goat/Crow/Possum Finger progression gates, and the cursed weapon discoveries.

## Build

GitHub Actions validates that the shipped game file has an `IWAD` header and rejects builds that still include `freedoom2.wad`, a separate Sam PK3, or a separate Sam PWAD.


## Environment/combat pass

MAP01 now uses separate material sectors for house, playground, forest, cemetery, tomb, station, mall and library rather than one shared floor/ceiling. Outdoor zones use the night sky; indoor zones have distinct roof/ceiling materials and heights. Location-specific wall textures include baked trim, grime, cracks or signage motifs.

Enemy variety now includes shamblers, undead goats, rot possums, cursed crows, ranged station husks, mall brutes and library shades before the final Mopoke. Cursed weapons keep distinct silhouettes and now have weapon-specific firing/impact sound cues.


## Definitive Sam sprite set

The uploaded Sam reference sheet is the source of truth for Sam. The IWAD build installs a 44-frame set covering look-back, scared, hurt, exhausted, crouch/hide, walk, run, turn, and fall/get-up states, replacing the earlier procedural Sam runner art.


## Music system

The supplied soundtrack is stored under anonymous internal names MUSIC01–MUSIC10. MUSIC01 is the title/menu cue. MAP01 changes cues by authored location using a one-second fade-out, switch at silence, and one-second fade-in. MUSIC09 is reserved for the final approach/fight and MUSIC10 for the ending.
