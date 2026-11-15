from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent/'src'))
from lib.geometry import base,panel,placement
from cadgen import build123d as bd
import trimesh
root=Path(__file__).parent
parts={'base':base(),'left_panel':panel(-1),'right_panel':panel(1)}
results={}
for name,s in parts.items():
    assert s.is_valid and len(s.solids())==1
    # Shift each part to the bed without changing its support-free orientation.
    s=bd.Pos(0,0,-s.bounding_box().min.Z)*s
    out=root/'STL'/f'{name}.stl'
    bd.export_stl(s,str(out),tolerance=.01,angular_tolerance=.1)
    m=trimesh.load(out)
    assert m.is_watertight and m.is_winding_consistent,(name,'mesh')
    results[name]={'valid':True,'watertight':True,'bounds_mm':tuple(s.bounding_box().size)}
b=parts['base']
for side,name in [(-1,'left_panel'),(1,'right_panel')]:
    p=placement(side)*parts[name]
    intersection=b&p
    volume=intersection.volume if intersection else 0
    assert volume<1e-5,(name,volume)
    results[name]['assembly_interference_mm3']=volume
results['clearance_per_side_mm']=.2
results['physical_fit_tested']=False
(root/'verification.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
