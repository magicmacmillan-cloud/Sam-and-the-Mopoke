from pathlib import Path
import zipfile

from sam_weapon_assets import generate_sam_assets
from world_assets import generate_world_assets

ROOT = Path(__file__).resolve().parent

generate_sam_assets(ROOT)
generate_world_assets(ROOT)

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
    names = set(z.namelist())
    missing = sorted(expected - names)
    if missing:
        raise RuntimeError(f"Sam frame archive missing: {missing}")
    for name in sorted(expected):
        body = z.read(name)
        if not body.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError(f"{name} is not PNG")
        (ROOT / "sprites" / name).write_bytes(body)

print(f"Installed {len(expected)} definitive Sam sprite frames from uploaded sheet")
print("Sam and the Mopoke Doom II assets generated")
