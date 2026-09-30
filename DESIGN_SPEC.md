# Sam and the Mopoke — campaign rebuild direction

## Core mandate

Rework the entire campaign map, scripting, pacing and encounter design. Do not merely decorate rectangular levels. Every location must be architecturally believable, distinctive, explorable and deliberately designed like a strong Doom II level.

This is a Doom II-style 2.5D horror adventure, not a straight corridor shooter and not a sequence of rectangular arenas. Progress comes from observing the environment, remembering landmarks, searching rooms, working out routes, finding keys and clues, opening shortcuts, solving environmental problems and occasionally backtracking. The player should feel that they figured something out.

Horror and suspense come first; combat comes second. Use quiet stretches, distant sounds, glimpses of movement, locked routes, false trails, darkness, partial views, loops and sudden encounters. High-action Doom combat is allowed as a contrast, not as the default room state.

Every ordinary wall must be solid and opaque. No accidental see-through walls, HOMs, missing textures or broken portals.

## Campaign pacing

### MAP01 — Arnold Street house — target ~10 minutes
A believable suburban Australian house: bedrooms, hall, lounge, kitchen, bathroom, laundry, cupboards, backyard access, carport and connecting spaces. Adam wakes confused. Sam is seen early, recognises only an undead threat, and runs. The player searches the house, follows clues, discovers blocked routes and eventually works out how to leave. Re-enterable loops and shortcuts are preferred over a straight path. Keep combat light and use subtle supernatural events.

### MAP02 — Playground — target ~6 minutes
Must unmistakably read as a real playground: equipment, paths, benches, fences, trees and believable circulation around the play structures. Include a small environmental/navigation problem. Sam can be glimpsed, but not caught. Enemy ecology differs from the house.

### MAP03 — Black-Gum woods — target ~15 minutes
First major navigation challenge. Branching trails, deadfall, creek/ditch-like routes, rocks, dense tree clusters, clearings, abandoned structures, landmarks, loops and misleading paths. The player learns the forest rather than following one corridor. Use audio cues, Mopoke sightings and false trails. Stronger evidence of Sam appears near the end.

### MAP04 — Cemetery — target ~10–12 minutes
Proper grave rows, mausoleums, paths, statues, fences, maintenance pockets, crypt approaches and shortcuts. Progress is clue/navigation-driven more than kill-driven. This is the first major Sam hiding encounter: Adam approaches, Sam is frightened, Adam can only make zombie sounds, and the encounter is interrupted so Sam runs again.

### MAP05 — Tomb / crypt — target ~8–10 minutes
Tight, oppressive puzzle-oriented exploration with chambers, burial niches, collapsed routes, symbols, relics and animal-finger progression. Goat, Crow and Possum Finger keys are physical progression objects used on matching gates. Their logic should be readable rather than arbitrary.

### MAP06 — Underground station — target ~12 minutes
A believable station: ticket hall, platforms, tracks, stairs, service rooms, staff areas, maintenance corridors and alternate sides of the platform. Use station-specific threats. A route puzzle controls movement between public and service areas. This map contains the major Sam recognition scene. Sam finally understands Zombie Dad is his father, Lincoln is referenced, and Sam becomes a companion.

### MAP07 — Cursed shopping centre / Diddy Mart — target ~15 minutes
One of the largest spaces: concourses, shopfronts, storerooms, food-court areas, toilets, stairs/escalator equivalents, service halls, loading zones and Diddy Mart itself. Multiple initial directions should later reveal how the complex connects. This is the largest action spike, but quiet and suspenseful stretches remain between fights. Sam follows the player.

### MAP08 — Impossible Library — target ~12–15 minutes
Reality breaks without becoming random or unfair. Repeating rooms, changed routes, shelves forming mazes, reading rooms, stairs, archives and visual landmarks create impossible connections the player can learn. The final stretch becomes an escalating escape/pursuit with Sam while Mopoke hunts them. Earlier keys, clues, supernatural rules or landmarks should matter. Do not reduce the finale to “shoot boss until health reaches zero.”

## Story arc

Sam is not a map marker.

At the beginning Adam sees Sam and internally recognises him: “Wait… Sam? Sam! It’s Dad…” Sam hears only Zombie Dad noises and panics.

For several zones the player follows evidence: footprints, belongings, drawings, notes, disturbed objects, distant sounds and occasional sightings.

In MAP04 Sam is found hiding. Adam tries to communicate. Sam is still frightened and runs again after the scene is interrupted.

In MAP06 Adam and Sam finally establish enough understanding that Sam realises the creature is his dad. The dialogue is short, believable and emotional, with Lincoln remaining part of the larger story. From this point Sam follows as an NPC companion.

The companion must be practical rather than irritating: keep up, avoid blocking combat, recover from separation where possible and avoid becoming a babysitting chore.

The final maps change the objective from “reach the exit” to “get Sam out alive.”

## Enemy ecology

Do not reuse every monster everywhere.

- House: only a small number of appropriate threats.
- Playground: light feral/wildlife pressure, different from house threats.
- Forest: Crow Fiends, Possum Crawlers and Mopoke stalking/glimpses.
- Cemetery: Cemetery Ghouls and related undead.
- Tomb: crypt creatures and wisps.
- Station: Station Husks/Revenants.
- Shopping centre: Mall Brutes/Husks.
- Library: Library Shades.
- Mopoke: sparse scripted presence before the finale; silhouettes, brief crossings and distant stalking are more effective than making it common.

## Doom II level-design rules

Use loops, windows/sightlines into future spaces, visible locked areas, height/material changes, interconnected rooms, meaningful shortcuts, ambush spaces, secrets, distinctive landmarks and routes that fold back on themselves.

The real-world location must remain legible. A house must read like a house, a shopping centre like a shopping centre, a station like a station. Do not make a rectangle and scatter themed props inside it.

Difficulty should come from navigation, tension, tactical decisions and discoverable puzzle logic. Avoid blind pixel hunting, arbitrary hidden switches and endless enemy spawning.

Exploration should reward the player with items, clues, secrets, safer routes and shortcuts rather than punish curiosity.

## Existing canon that must be preserved

Preserve Zombie Dad, Sam, Lincoln traces, the current Mopoke design, the 13 cursed weapons, animal-finger keys and gates, existing Sam sprite identity, clues, searchable loot, music system and established visual assets. Do not replace them with generic pistols, keycards or stock Doom monsters.

## Completion standard

Before calling a campaign pass complete, logically simulate every map from entry to exit and verify:

- multiple meaningful spaces
- believable architecture
- working progression
- proper zone-specific enemy placement
- no transparent walls or HOMs
- no broken geometry
- no softlocks
- no unreachable mandatory objectives
- no mandatory blind pixel hunting
- no simple straight-line solution
- Sam story progression works in the intended order
- finger keys are obtainable before their matching gates
- the final pursuit uses what the player learned earlier

The target experience is creepy, emotional, surprising, occasionally frantic and genuinely fun to solve.
