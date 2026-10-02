from pathlib import Path
import zipfile

from sam_weapon_assets import generate_sam_assets
from world_assets import generate_world_assets
from polish_assets import generate_polish_assets
from visual_stability import apply_visual_stability
from house42_assets import generate_house42_assets

ROOT = Path(__file__).resolve().parent

# Base generators provide the complete weapon/pickup/world resource inventory.
generate_sam_assets(ROOT)
generate_world_assets(ROOT)

# Sam's uploaded 44-frame sheet is the source of truth for Sam. Reinstall it after
# the base generators so no procedural fallback frame can overwrite his identity.
sam_zip = ROOT / "sam_frames.zip"
if not sam_zip.is_file():
    raise RuntimeError("missing sam_frames.zip")

sam_prefixes = ("SAML","SAMS","SAMH","SAME","SAMC","SAMW","SAMR","SAMT","SAMF")
for p in (ROOT / "sprites").glob("SAM*.png"):
    if p.stem[:4] in sam_prefixes:
        p.unlink()

expected = {
    *(f"SAML{c}0.png" for c in "ABCDEF"),
    *(f"SAMS{c}0.png" for c in "ABCD"),
    *(f"SAMH{c}0.png" for c in "ABCD"),
    *(f"SAME{c}0.png" for c in "ABCD"),
    *(f"SAMC{c}0.png" for c in "ABCD"),
    *(f"SAMW{c}0.png" for c in "ABCDEF"),
    *(f"SAMR{c}0.png" for c in "ABCDEF"),
    *(f"SAMT{c}0.png" for c in "ABCD"),
    *(f"SAMF{c}0.png" for c in "ABCDEF"),
}
with zipfile.ZipFile(sam_zip, "r") as z:
    names=set(z.namelist())
    missing=sorted(expected-names)
    if missing:
        raise RuntimeError(f"Sam frame archive missing: {missing}")
    for name in sorted(expected):
        body=z.read(name)
        if not body.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError(f"{name} is not PNG")
        (ROOT/"sprites"/name).write_bytes(body)

# Restore the detailed visual pass we had already developed: proper undead Dad hands,
# held cursed weapons, standalone pickups, Zombie Dad HUD faces, 8-direction monsters,
# canonical Mopoke, location props and richer textures.
generate_polish_assets(ROOT)

# Reinstall the source-matched 42 Arnold domestic texture/detail pack after the generic
# polish pass so MAP01 keeps the walkthrough-specific materials.
generate_house42_assets(ROOT)

# Final cleanup prevents the two bugs seen in the older APKs: first-person sprites
# hovering in the top-left and mixed A0/A1..A8 monster frames flickering between art sets.
apply_visual_stability(ROOT)

print(f"Installed {len(expected)} definitive Sam sprite frames from uploaded sheet")
print("Sam and the Mopoke polished Doom II assets generated, including 42 Arnold source-matched MAP01 materials")
