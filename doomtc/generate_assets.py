from pathlib import Path
from sam_weapon_assets import generate_sam_assets

ROOT = Path(__file__).resolve().parent
generate_sam_assets(ROOT)
print("Sam and the Mopoke Doom II sprites generated")
