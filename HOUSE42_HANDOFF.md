# 42 Arnold Street — MAP01 AI builder handoff

This is an engine-independent MAP01 handoff based on the supplied walkthrough video, satellite/top-down screenshots and front-facade image. It contains map geometry, layout data and source-matched environment assets only — no APK or Android engine.

## What changed

- Rebuilt the **house as separate rooms with real wall gaps and door openings** instead of a union of overlapping rectangles.
- Corrected the **right/east driveway and carport**, front porch, long backyard and large rear shed.
- Added **Arnold Street, Collenso Street, No. 44, No. 40, houses opposite, the reserve and playground** as spatial context.
- Removed the earlier invented separate WC. The walkthrough bathroom contains the toilet.
- Added explicit front/side/rear window segments, the east-side brick chimney, black front metal rail/gate treatment and cream weatherboard exterior.
- Added a new source-matched material set for MAP01: brown carpet, polished timber, tan vinyl, cream wall tile, pink bathroom tile, timber kitchen cabinetry, cream weatherboards, brick chimney, concrete, asphalt, pavers, grass, fences, windows, blinds and domestic doors.
- Dad starts in the backyard; Sam flees through the rear house, central hall and real front door, then west/up Arnold Street to the Collenso-side playground before the MAP02 exit.
- The exterior block now includes neighbour massing, lawns, footpaths/nature strips, street lamps/poles, parked cars, reserve trees, bins and recognisable playground equipment.

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
- Collenso Street and the reserve sit west of the house. The playground is reached from Arnold Street at that Collenso/reserve side; it is not behind the backyard.

The detailed machine-readable dimensions, door openings, window segments, story route and satellite-derived street dressing are in `doomtc/house42_layout.json`.

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

## Handoff files

- `doomtc/house42_map.py` — detailed MAP01 classic-Doom map compiler
- `doomtc/house42_assets.py` — source-matched texture/flat/reference-sprite generator
- `doomtc/house42_layout.json` — machine-readable layout/evidence
- `doomtc/build_house42_handoff.py` — builds the standalone MAP01 handoff PWAD/ZIP
- `doomtc/house42_assets.py` — generates only the H42 house/street/park material and prop set

The CI handoff artifact contains the generated IWAD, map WAD, layout JSON, handoff notes and the generated H42 textures/flats so another AI can inspect or continue without reconstructing the asset names.


## Non-negotiable exterior relationships

- No.44 sits between No.42 and Collenso Street.
- No.40 is immediately east/right of No.42.
- Nos.39, 37 and 35 are represented opposite Arnold Street.
- Arnold Street has separate asphalt, footpaths and grass nature strips.
- The reserve is west of Collenso Street and includes the winding pedestrian path visible in the satellite reference.
- The playground sits at the Arnold/Collenso reserve side. It is **not** behind the backyard.
- Keep visible suburban dressing: lawns, garden beds, driveways, rear sheds/outbuildings, street lamps/poles, parked cars, bins, reserve trees, bench, swings and slide/climber.


## V2 exterior detail upgrade

This handoff now carries the suburban dressing in the actual MAP01 PWAD rather
than leaving it only as prose for the next builder.

- Dedicated **white Toyota Hilux Workmate-style single-cab tray ute** in the
  east/right driveway of No.42, using an eight-rotation Doom sprite.
- Three wheelie bins positioned on the Arnold Street nature strip at the kerb:
  red-lid, yellow-lid and green/garden treatment.
- Mature street/reserve trees placed around No.42, No.44, No.40, the opposite
  verge and the reserve/playground.
- Additional low shrubs/garden planting around the front garden and immediate
  neighbours so the yards do not read as empty flat rectangles.
- Street lamps/poles retained along Arnold and Collenso.
- Parked cars retained on Arnold Street and neighbouring driveways; No.42 uses
  the dedicated Workmate instead of a generic car.
- Playground bench, swings, slide and climber remain present as both sector
  geometry and scenery objects.
- Outdoor materials are split into distinct mown lawn, nature strip, footpath,
  driveway, residential asphalt and garden-bed surfaces.

The map-only PWAD contains environment scenery actors and their PNG sprites, but
continues to omit Sam, enemies, weapons, HUD, Android code and all APK/engine files.


## V3 corrected front/rear elevations

The map orientation is now explicitly locked so the house cannot be rendered backwards.

- **SOUTH / Arnold Street = FRONT of the house.**
- The front lawn, covered porch, dark front door, doorbell, black front rail/gate and front windows exist only on this south/Arnold Street elevation.
- **NORTH / backyard = REAR of the house.**
- The rear elevation is the enclosed veranda/sunroom side with its own rear glazing, plain rear door and small landing/patio leading into the backyard.
- The rear shed remains farther north in the backyard.
- The east/right side remains the driveway and covered carport toward No.40.
- Separate texture IDs are used for front and rear elements: `H42FRNT` / `H42FWIN` for the front, and `H42RDR` / `H42RWIN` / `H42REAR` for the rear.
- Do **not** mirror or reuse the Arnold Street porch/front door on the backyard side.

This correction is part of the actual MAP01 geometry and texture assignment, not just a concept-image instruction.
