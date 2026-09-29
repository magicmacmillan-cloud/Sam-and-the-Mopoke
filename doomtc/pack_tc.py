from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"build"/"sam-and-the-mopoke.pk3"
OUT.parent.mkdir(parents=True,exist_ok=True)
exclude={"build","__pycache__"}
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel=p.relative_to(ROOT)
        if any(part in exclude for part in rel.parts):
            continue
        if p.name in {"build_map.py","generate_assets.py","pack_tc.py","sam_weapon_assets.py","README.md"}:
            continue
        if p.suffix in {".pyc"}:
            continue
        z.write(p,rel.as_posix())
print(OUT)
