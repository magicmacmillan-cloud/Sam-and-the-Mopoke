from pathlib import Path
import json, shutil, struct, zipfile

from house42_map import build_house42_map, AREAS
from house42_assets import generate_house42_assets

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"house42_handoff_build"

def wad_name(raw):
    if isinstance(raw,bytes):
        return raw.rstrip(b"\0").decode("ascii")
    return str(raw)

def write_wad(path,lumps,ident=b"PWAD"):
    data=bytearray()
    directory=[]
    pos=12
    for name,body in lumps:
        if isinstance(name,str):
            nb=name.encode("ascii")[:8].ljust(8,b"\0")
        else:
            nb=name[:8].ljust(8,b"\0")
        directory.append((pos,len(body),nb))
        data.extend(body)
        pos+=len(body)
    diroff=12+len(data)
    with path.open("wb") as f:
        f.write(ident)
        f.write(struct.pack("<II",len(directory),diroff))
        f.write(data)
        for p,size,name in directory:
            f.write(struct.pack("<II8s",p,size,name))

def geometry_map_lumps():
    lumps,stats=build_house42_map()
    clean=[]
    for name,body in lumps:
        if wad_name(name)=="THINGS":
            # Clean handoff: only a player start. Story/scenery placements are supplied
            # in JSON so another AI does not inherit unknown custom actor classes.
            body=struct.pack("<hhhhh",420,1500,270,1,7)
        clean.append((name,body))
    return clean,stats

def collect_assets():
    generate_house42_assets(ROOT)
    tex=sorted((ROOT/"textures").glob("H42*.png"))
    flats=sorted(list((ROOT/"flats").glob("H42*.png"))+
                 [p for p in (ROOT/"flats").glob("H??ROOF.png")])
    sprite_names=("DBELA0","SMCLA0","STLPA0","TREEA0","CARWA0","CARDA0",
                  "BNCHA0","SWNGA0","SLIDA0","CLMBA0","WBINA0")
    sprites=[ROOT/"sprites"/f"{n}.png" for n in sprite_names if (ROOT/"sprites"/f"{n}.png").exists()]
    gfx=[ROOT/"graphics"/"H42ATLAS.png"] if (ROOT/"graphics"/"H42ATLAS.png").exists() else []
    return tex,flats,sprites,gfx

def make_svg(path,layout):
    xmin,ymin,xmax,ymax=-2400,-1408,2000,2944
    W,H=1500,1500
    pad=40
    sx=(W-2*pad)/(xmax-xmin)
    sy=(H-2*pad)/(ymax-ymin)
    scale=min(sx,sy)
    def pt(x,y):
        return pad+(x-xmin)*scale, H-pad-(y-ymin)*scale

    palette={
      "ROAD":"#55595a","FOOT":"#c8c7c0","VERGE":"#839d66","YARD":"#7f9d63",
      "LOT":"#879f6c","RESERVE":"#809b62","PLAY":"#c07b48","PLAYEQ":"#9b5f3f",
      "DRIVE":"#aaa9a3","CARPORT":"#969793","PATIO":"#a58e78","GARDEN":"#705a43",
      "SHED":"#777b7c","PORCH":"#b3afa4","ENTRY":"#cbbfa7","HALL":"#cbbfa7",
      "LOUNGE":"#8e7867","BED":"#9f8a78","BEDWOOD":"#a07652","BATH":"#bc8e95",
      "MEALS":"#a98b62","KITCH":"#93663f","LAUNDRY":"#9f805e","SUNROOM":"#aea99c",
      "NBR44":"#8b6a59","NBR40":"#6e6861","NBR39":"#946953","NBR37":"#9b6d55",
      "NBR35":"#866353","NBR1":"#81736a","NBR2":"#766a63",
      "FURNWOOD":"#65452f","FURNFAB":"#75665a","FIXWHITE":"#e4e1d8",
      "FIXPINK":"#c998a0","APPLI":"#d1cec4","POST":"#77736c","DOOR":"#4d4138"
    }

    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg.append('<rect width="100%" height="100%" fill="#f2f0ea"/>')
    for x0,y0,x1,y1,style in AREAS:
        ax,ay=pt(x0,y1); bx,by=pt(x1,y0)
        c=palette.get(style,"#b8b4aa")
        svg.append(f'<rect x="{ax:.1f}" y="{ay:.1f}" width="{bx-ax:.1f}" height="{by-ay:.1f}" fill="{c}" stroke="#2b2b2b" stroke-width="0.45" data-style="{style}"/>')

    labels=[
      ("42 ARNOLD",480,240),("44",-470,220),("40",1450,220),
      ("ARNOLD STREET",350,-445),("COLLENSO ST",-1100,850),
      ("PLAYGROUND",-1880,-900),("RESERVE",-1880,500),
      ("BACKYARD",380,1500),("SHED",730,2050),
      ("LOUNGE",585,535),("BED 1",210,470),("BED 2",210,715),
      ("BATH",205,885),("BED 3",585,825),("KITCHEN",450,1065),
      ("LAUNDRY",630,1065),("SUNROOM",390,1235)
    ]
    for t,x,y in labels:
        px,py=pt(x,y)
        svg.append(f'<text x="{px:.1f}" y="{py:.1f}" font-size="12" font-family="Arial,sans-serif" text-anchor="middle" fill="#111">{t}</text>')

    route=layout.get("story_flow",{}).get("sam_escape",[])
    if route:
        pts=" ".join(f"{pt(x,y)[0]:.1f},{pt(x,y)[1]:.1f}" for x,y in route)
        svg.append(f'<polyline points="{pts}" fill="none" stroke="#b32121" stroke-width="3" stroke-dasharray="8 5"/>')
        for i,(x,y) in enumerate(route):
            if i in (0,len(route)-1):
                px,py=pt(x,y)
                svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#fff" stroke="#b32121" stroke-width="2"/>')

    svg.append('<text x="40" y="25" font-size="18" font-family="Arial,sans-serif" font-weight="bold">42 Arnold Street — MAP01 handoff</text>')
    svg.append('<text x="40" y="45" font-size="11" font-family="Arial,sans-serif">Source-driven reconstruction from supplied walkthrough + satellite/front references. North/backyard is up.</text>')
    svg.append('</svg>')
    path.write_text("\n".join(svg),encoding="utf-8")

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT/"textures").mkdir(parents=True)
    (OUT/"flats").mkdir()
    (OUT/"sprites").mkdir()
    (OUT/"references").mkdir()

    layout=json.loads((ROOT/"house42_layout.json").read_text())
    map_lumps,stats=geometry_map_lumps()
    tex,flats,sprites,gfx=collect_assets()

    wad_lumps=[
      ("MAPINFO",b'map MAP01 "42 Arnold Street" { next = "MAP02" }\n'),
    ]
    wad_lumps.extend(map_lumps)
    wad_lumps.append(("TX_START",b""))
    for p in tex:
        wad_lumps.append((p.stem.upper()[:8],p.read_bytes()))
    wad_lumps.append(("TX_END",b""))
    wad_lumps.append(("F_START",b""))
    for p in flats:
        wad_lumps.append((p.stem.upper()[:8],p.read_bytes()))
    wad_lumps.append(("F_END",b""))

    wad=OUT/"42-Arnold-MAP01-geometry-and-textures.wad"
    write_wad(wad,wad_lumps)

    for p in tex: shutil.copy2(p,OUT/"textures"/p.name)
    for p in flats: shutil.copy2(p,OUT/"flats"/p.name)
    for p in sprites: shutil.copy2(p,OUT/"sprites"/p.name)
    for p in gfx: shutil.copy2(p,OUT/"references"/p.name)

    shutil.copy2(ROOT/"house42_map.py",OUT/"house42_map.py")
    shutil.copy2(ROOT/"house42_layout.json",OUT/"house42_layout.json")
    handoff=ROOT.parent/"HOUSE42_HANDOFF.md"
    if handoff.exists(): shutil.copy2(handoff,OUT/"README_MAP_HANDOFF.md")

    make_svg(OUT/"42-Arnold-overhead-plan.svg",layout)

    manifest={
      "format":"42-arnold-map-handoff-v1",
      "map":"MAP01",
      "engine_dependency":"none; classic Doom-format PWAD geometry with PNG GZDoom texture namespaces",
      "stats":{"sectors":stats[0],"linedefs":stats[1],"source_things":stats[2],"handoff_wad_things":1},
      "files":{
        "wad":wad.name,
        "layout":"house42_layout.json",
        "source":"house42_map.py",
        "overhead":"42-Arnold-overhead-plan.svg"
      },
      "textures":[p.name for p in tex],
      "flats":[p.name for p in flats],
      "detail_sprites":[p.name for p in sprites],
      "important_notes":[
        "Dad/player start is in the backyard.",
        "Sam route metadata runs backyard -> rear house -> hall -> front door -> Arnold Street -> Collenso-side playground.",
        "The playground is up the street at the reserve/Collenso side, not behind the backyard.",
        "Neighbouring houses, footpaths, nature strips, driveways, reserve and playground are part of MAP01.",
        "The WAD intentionally contains no custom gameplay actors; their placements remain in house42_layout.json."
      ]
    }
    (OUT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")

    source_notes="""# Source fidelity notes

This handoff contains MAP01 only. It does **not** contain an Android engine, APK,
player weapon art, HUD, or character sprite set.

Priority of evidence:
1. supplied walkthrough video: room sequence, finishes, door/window/furniture cues;
2. supplied satellite/top-down screenshots: lot, neighbours, streets, reserve and playground;
3. supplied front photo: facade, porch, cream weatherboards, roof, chimney, rail/gate;
4. reconstructed dimensions only where the source media cannot be measured.

Key exterior layout:
- 42 Arnold is on the north side of Arnold Street;
- driveway/carport is on the east/right side toward No.40;
- No.44 is the west/left neighbour between 42 and Collenso Street;
- No.40 is the east/right neighbour;
- Nos.39, 37 and 35 are represented opposite Arnold Street;
- Collenso Street is west of No.44;
- the reserve is west of Collenso;
- the playground is southwest/west of the Arnold/Collenso corner in the reserve,
  reached from Arnold Street — it is not behind the backyard.

The next builder should improve dimensions only when video/satellite evidence supports it,
not replace the map with a generic suburban or Doom layout.
"""
    (OUT/"SOURCE_FIDELITY.md").write_text(source_notes,encoding="utf-8")

    zpath=ROOT.parent/"42-Arnold-MAP01-AI-HANDOFF.zip"
    if zpath.exists(): zpath.unlink()
    with zipfile.ZipFile(zpath,"w",zipfile.ZIP_DEFLATED) as z:
        for p in OUT.rglob("*"):
            if p.is_file(): z.write(p,p.relative_to(OUT))
    print(zpath)
    print(manifest["stats"])

if __name__=="__main__":
    main()
