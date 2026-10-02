# 42 Arnold Street — MAP01 builder handoff v3

This branch replaces the generic MAP01 house blockout with a source-driven reconstruction based on the supplied walkthrough video, aerial screenshots and front-facade image.

## What changed

- Rebuilt the **house as separate rooms with real wall gaps and door openings** instead of a union of overlapping rectangles.
- Corrected the **right/east driveway and carport**, front porch, long backyard and large rear shed.
- Added **Arnold Street, Collenso Street, No. 44, No. 40, houses opposite, the reserve and playground** as spatial context.
- Removed the earlier invented separate WC. The walkthrough bathroom contains the toilet.
- Added explicit front/side/rear window segments, the east-side brick chimney, black front metal rail/gate treatment and cream weatherboard exterior.
- Added a new source-matched material set for MAP01: brown carpet, polished timber, tan vinyl, cream wall tile, pink bathroom tile, timber kitchen cabinetry, cream weatherboards, brick chimney, concrete, asphalt, pavers, grass, fences, windows, blinds and domestic doors.
- The route from the house to the playground is now physically represented in MAP01 before the exit to MAP02.

## Source hierarchy

When evidence conflicts, use this order:

1. **Walkthrough video** for room order, door adjacency, finishes and rear-house flow.
2. **Supplied aerials** for property footprint, driveway, backyard, shed, neighbouring houses, streets and playground relationship.
3. **Supplied front photo** for facade proportions/materials: cream weatherboards, dark tiled roof, right-side brick chimney, porch, black metal railings and driveway gate.
4. This reconstruction for dimensions where the source media does not provide measurable geometry.

The internal dimensions are still an approximation, not a cadastral or architectural survey.

## Walkthrough chronology

| Video time | Area |
| --- | --- |
| 0–24 s | Arnold Street / front boundary / driveway approach |
| 24–56 s | Front garden, driveway, porch approach |
| 56–60 s | Front entry and tiled hall |
| 62–70 s | Lounge |
| 72–82 s | Front-left bedroom |
| 82–88 s | Second bedroom / hall |
| 88–100 s | Bathroom including toilet |
| 102–112 s | Lounge return |
| 114–122 s | Hall toward rear |
| 122–138 s | Third bedroom, polished floorboards and robe |
| 138–166 s | Meals / long timber kitchen |
| 166–176 s | Laundry / utility |
| 178–186 s | Enclosed rear veranda / sunroom |
| 186–258 s | Patio, backyard, shed and exterior walls |

## MAP01 coordinate convention

- 64 Doom units ≈ 1 metre.
- +Y = north / backyard.
- +X = east / driveway / No. 40.
- 42 Arnold lot = approximately `x 0..960, y 0..2944`.
- Arnold Street is immediately south of the property.
- No. 44 is west/left; No. 40 is east/right.
- Collenso Street and the reserve/playground sit west/south-west.

The detailed machine-readable dimensions, door openings and window segments are in `doomtc/house42_layout.json`.

## Material names

### Walls / textures

- `H42WALL` — warm cream painted plaster with skirting
- `H42GREY` — pale grey painted plaster
- `H42PANL` — brown vertical timber wall panelling
- `H42KTCH` — timber kitchen cabinets + brown marbled benchtop + cream backsplash
- `H42BATH` — pink/cream bathroom tile
- `H42SIDN` — cream horizontal weatherboards
- `H42BRIK` — orange/brown chimney brick
- `H42SHED` — grey corrugated shed/carport metal
- `H42FENC` — dark timber side/rear fence
- `H42GATE` — black metal front railing/gate
- `H42WIND` — dark glazed window with pale frame
- `H42BLND` — off-white vertical blinds
- `H42DOOR` — varnished timber domestic door
- `H42WDR` — white painted domestic door
- `H42CURB` — aged concrete kerb
- `H42PLAY` — playground/equipment material cue

### Floors / flats

- `H42CARP` — brown/tan mottled carpet
- `H42WOOD` — polished warm timber boards
- `H42VNYL` — tan patterned vinyl/lino
- `H42TILF` — cream domestic tile
- `H42CONC` — aged concrete
- `H42ASPH` — residential asphalt
- `H42GRAS` — suburban grass
- `H42PAVE` — patio/rear paving
- `H42CEIL` — off-white ceiling
- `H42ROOF` — dark tiled-roof massing

## HOUSE PROGRESSION AND INTERNAL LAYOUT — NON-NEGOTIABLE

This section overrides every earlier MAP01 shortcut, generic Doom-loop preference, route suggestion or blockout that conflicts with it. If another file disagrees with this section for the opening of MAP01, this section wins.

### Opening story and route

Dad starts in the backyard. Sam is seen running away from Dad toward the side driveway gate. Sam gets through the **see-through black iron gate**, padlocks it behind him and continues toward Arnold Street / the park. Dad can see the driveway and Hilux through the gate but cannot follow.

Lincoln has separately locked the actual rear house door to keep the Mopoke out.

The mandatory opening flow is:

**Backyard → see Sam escape through side iron gate → gate is padlocked and blocks Dad → try locked rear door → garage → hidden spare back-door key → rear door → long sunroom → small laundry → kitchen → Lincoln's room → return to kitchen → main hallway → lounge/bathroom + Sam/master room pairs → Lincoln's front-door clue → Sam's puzzle box → front-door key → Arnold Street → playground entrance gate → Sam's gate note → neighbour's letterbox → playground gate key → unlock gate → enter playground → MAP02.**

There is **NO usable backyard-to-front shortcut**.

### Backyard and side gate

The backyard must contain the real rear façade, long enclosed sunroom/veranda, accessible garage/shed, lawn/garden, side/rear fences, dog-dug-under-fence evidence, the driveway gate and the Hilux visible beyond it.

The driveway gate must:

- be a see-through black iron gate
- visibly carry a small padlock
- physically block Dad
- have no gap around either side
- not open during the opening sequence
- not be climbable or bypassable
- not allow a route between house/fence/vehicle
- give restrained feedback when used: **Padlocked. Sam locked it behind him.**

Sam is allowed to pass through it only as a scripted opening event. The player is not.

If Dad can simply walk down the driveway to Arnold Street from the backyard, MAP01 is wrong.

### Locked rear door and spare key

Lincoln has locked the rear door to keep the Mopoke out.

The rear door:

- faces the backyard
- is visually different from the Arnold Street front door
- uses rear/sunroom materials
- is a real working Doom door
- stays locked until Dad has the spare rear-door key
- uses sensible locked/opening feedback
- permanently allows entry after unlocking

A spare back-door house key is hidden inside the garage near believable storage/workbench clutter. It must require a small amount of searching and must not be a giant glowing arcade pickup.

The first puzzle is:

**See Sam escape → side gate blocks Dad → rear door is locked → search garage → find spare key → enter house.**

### Rear interior route

The unlocked rear door opens directly into the **long sunroom**.

The route is then:

**long sunroom → small laundry → kitchen**

The sunroom must read as the actual elongated rear space from the walkthrough: broad glazing, rear-house finishes, domestic scale, storage/furniture and appropriate lighting. Do not convert it into a maze.

The small laundry must remain compact and domestic with believable washer/trough/storage/floor treatment.

The kitchen must match the walkthrough's cabinets, benchtops, splashback, appliances, floor transition and openings. Do not enlarge it into a generic Doom room.

### Lincoln's room and phone

**Lincoln's room comes directly off the kitchen and is not a through-route.**

Dad enters Lincoln's room, investigates, reads Lincoln's phone, then returns to the kitchen.

The phone message to Dad is:

> Sam ran away to the park, I'm going after him. I've locked the doors behind us so it can't get us. If it's really still you Dad, help us stay safe.

The phone must be normal domestic scale and exist naturally in Lincoln's bedroom.

Reading it unlocks the narrative clue chain for the front door.

### Main hallway and required room relationships

From the kitchen Dad enters the main hallway.

The hallway must preserve these exact opposite-room relationships:

- **Lounge opposite Bathroom**
- **Sam's bedroom opposite Master bedroom**

The four principal rooms off the hallway are:

1. Lounge
2. Bathroom
3. Sam's bedroom
4. Master bedroom

Minor Doom-grid dimension adjustments are allowed; these spatial relationships are not.

The rooms must read as ordinary suburban rooms, not Doom arenas.

The lounge contains **three Xbox consoles hooked to TVs**.

The master bedroom contains a usable projector.

### Front-door clue and 2330 puzzle

The Arnold Street front door is locked and requires its own key.

After Lincoln's phone has been read, Dad can read the natural-sized note taped to the **inside of the front door**:

> I've hidden the key in Sam's puzzle box. Code is: e-scooters, Xbox, eggs, projector.

Do not display 2330 on this note.

The player deduces the code from physical evidence:

- **2** e-scooters in the garage
- **3** Xbox consoles hooked to TVs in the lounge
- **3** eggs in the kitchen fridge
- the master-bedroom projector counts **3 → 2 → 1 → 0** when switched on and then remains displaying **0** on the wall

Therefore the puzzle-box code is **2330**.

Sam's puzzle box is in Sam's bedroom. It uses an in-world four-digit keypad. Entering 2330 opens it and gives Dad the front-door key.

Wrong entries may reset the keypad but must not softlock progression.

The front door remains locked until this key is obtained.

### Street to playground and MAP01 ending

After leaving the real Arnold Street front door, Dad follows the street toward the reserve/playground shown in the aerial references.

The entrance gate to the playground is padlocked.

A normal-sized handwritten note taped to the gate in Sam's handwriting says:

> I left the key in the neighbour's letterbox.

Reading this note enables the next clue.

Dad must search the neighbour's letterbox, retrieve the playground-gate key, return to the gate and unlock it.

The gate itself is the final progression lock. There is no giant EXIT billboard.

**MAP01 ends only after Dad unlocks the playground gate and crosses into the start of the playground. MAP02 begins on the playground side.**

### Door and clue rules

All relevant doors must be real, working Doom doors with correct collision, proportions, textures and sound.

Never use:

- fake painted-on doors
- visible doors that do nothing
- invisible blockers across open doorways
- random door orientation
- oversized note/billboard clues
- giant objective text replacing environmental storytelling

Notes, phone, puzzle box, keys and padlocks must remain believable world objects at domestic scale.

### Mandatory clean-start acceptance test

1. Dad spawns in backyard.
2. Sam runs toward/through the side iron driveway gate and disappears toward Arnold Street.
3. The gate is visibly padlocked; Dad cannot follow or bypass it.
4. Dad can see the driveway/Hilux beyond the gate.
5. Rear house door is locked because Lincoln locked the house.
6. Dad searches the garage.
7. Dad finds the hidden spare rear-door key.
8. Dad returns and unlocks the real rear door.
9. Dad enters the long sunroom.
10. Dad proceeds to the small laundry.
11. Dad enters the kitchen.
12. Dad investigates Lincoln's room directly off the kitchen.
13. Dad reads Lincoln's phone message.
14. Dad returns to the kitchen.
15. Dad enters the main hallway.
16. Lounge is opposite bathroom.
17. Sam's bedroom is opposite master bedroom.
18. Dad can inspect two garage e-scooters, three lounge Xbox/TV setups, three eggs in the fridge and the master-bedroom projector.
19. Dad reads the note on the inside of the locked front door.
20. Dad deduces and enters 2330 into Sam's puzzle box.
21. The puzzle box gives the front-door key.
22. Dad unlocks the front door and reaches Arnold Street.
23. Dad reaches the padlocked playground entrance gate.
24. Dad reads Sam's gate note.
25. Dad retrieves the playground-gate key from the neighbour's letterbox.
26. Dad unlocks the playground gate.
27. Dad crosses into the playground and MAP01 ends / MAP02 begins.

If any required lock can be bypassed, any key is unnecessary, Lincoln's room is not off the kitchen, the opposite-room pairings are wrong, or MAP01 can end before the playground gate is unlocked, the build fails acceptance.

## OPTIONAL SECRET — NO. 44 WANTED-POSTER ARMOURY

This section adds to V35/V34.2. It must never replace or bypass the mandatory 42 Arnold progression.

- Secret entrance is on the Arnold Street side of neighbour No. 44, accessible only after Dad has legitimately reached the street.
- Entering the inner threshold counts as one Doom secret.
- Inside is one compact hallway with eight small side rooms.
- Every room has a different wanted-poster texture on its working Doom door.
- Every room contains a different weapon, a useful ammo/charge pickup, and armour on the floor.
- Weapon rooms are rewards, not required progression. The player can leave without clearing them.
- The eight current weapon rewards are DoomEdNums 15001 through 15008.
- The room ammo is ArmoryChargePack (15800). Seven rooms use standard green armour; the final room uses blue armour.
- A concealed rear compartment contains a group of ambush zombies.
- The hidden rear door is a real closed Doom door sector with tag 77.
- Crossing the weapon pickup line in any room uses classic Doom W1 Door Open Stay (special 2, tag 77), opening the hidden compartment and releasing the zombies.
- The ambush trigger must happen only inside the secret armoury and must not alter the rear/front/playground locks.
- The secret house must not connect to 42 Arnold's backyard, side yard, driveway, garage, sunroom, or any route before the real front-door unlock.
- Poster art must remain wall/door texture scale. Never make the posters giant freestanding billboards.

Acceptance check: eight poster doors, eight distinct weapons, eight ammo packs, armour in all eight rooms, one counted secret, one tag-77 hidden door, and a hidden zombie group that is released when the player commits to a weapon room.

## Detail pass for the next IWAD builder

Keep the supplied geometry and materials as the baseline, then add Doom-sector/midtexture detail where useful:

- skirting boards and door architraves
- window recesses/sills and vertical blinds
- front porch posts and black railings
- kitchen benches, overhead cupboards, sink, stove and fridge
- pink bath, basin, toilet and shower
- laundry trough/washer
- wardrobes
- chimney, gutters and downpipes
- carport posts/roof
- driveway gate, rear fences, concrete paths and garden beds
- wheelie bins, clothesline, shrubs, trees, poles and playground equipment

Do not enlarge rooms into oversized Doom corridors. The house should read as a real small suburban home.

## Build files

- `doomtc/house42_map.py` — detailed MAP01 classic-Doom map compiler
- `doomtc/house42_assets.py` — source-matched texture/flat/reference-sprite generator
- `doomtc/house42_layout.json` — machine-readable layout/evidence
- `doomtc/build_map.py` — invokes the detailed MAP01 compiler
- `doomtc/generate_assets.py` — installs the 42 Arnold material pass after generic polish

The CI handoff artifact contains the generated IWAD, map WAD, layout JSON, handoff notes and the generated H42 textures/flats so another AI can inspect or continue without reconstructing the asset names.
