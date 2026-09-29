from pathlib import Path
from sam_weapon_assets import generate_sam_assets
from world_assets import generate_world_assets

ROOT = Path(__file__).resolve().parent
generate_sam_assets(ROOT)
generate_world_assets(ROOT)
print("Sam and the Mopoke Doom II assets generated")
