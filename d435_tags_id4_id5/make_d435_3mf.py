"""Bambu project (P1S, AMS) with the glue-on tags id 4 and 5 for the D435, printed face up (white 1 mm base on the
bed = filament 1, black 0.2 mm top layer = filament 2). Settings copied from the foot-tag project (same as the tag-2
print). Also renders the top view of each tag to print/tagN_face.png. Sim venv: python make_d435_3mf.py"""
import struct
import uuid
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

D = Path(__file__).resolve().parent
OUT = D / 'print'; OUT.mkdir(exist_ok=True)
TEMPLATE = D.parents[1] / 'scene/custom_mounts/foot_tags/so101_full_underfoot_cap_apriltag_holders.3mf'


def load(p):
    b = p.read_bytes(); n = struct.unpack('<I', b[80:84])[0]
    return np.frombuffer(b[84:84 + n * 50], dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]))['v'].astype(float)


def mesh_xml(oid, T):
    V, inv = np.unique(T.reshape(-1, 3).round(5), axis=0, return_inverse=True)
    F = inv.reshape(-1, 3); F = F[(F[:, 0] != F[:, 1]) & (F[:, 1] != F[:, 2]) & (F[:, 0] != F[:, 2])]
    vs = '\n'.join(f'     <vertex x="{x:.5f}" y="{y:.5f}" z="{z:.5f}"/>' for x, y, z in V)
    ts = '\n'.join(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in F)
    return f'  <object id="{oid}" p:UUID="{uuid.uuid4()}" type="model">\n   <mesh>\n    <vertices>\n{vs}\n    </vertices>\n    <triangles>\n{ts}\n    </triangles>\n   </mesh>\n  </object>', len(F)


objects = []
for k, tid in enumerate((4, 5)):
    white = load(D / f'tag{tid}_sticker_WHITE.stl'); black = load(D / f'tag{tid}_sticker_BLACK.stl')
    objects.append((f'tag{tid} D435 (face up)', [(f'tag{tid} WHITE (filament 1)', white, 1), (f'tag{tid} BLACK (filament 2)', black, 2)], (90.0 + 76 * k, 128.0)))
    S, M, W = 12, 40, 60
    img = Image.new('L', (W * S + 2 * M, W * S + 2 * M), 255); dr = ImageDraw.Draw(img)
    for t in black:
        if np.ptp(t[:, 2]) < 1e-6 and t[0, 2] > 0.9:
            dr.polygon([(M + p[0] * S, M + (W - p[1]) * S) for p in t], fill=0)
    img.save(OUT / f'tag{tid}_face.png')

mesh_objs, model_objs, build, cfg = [], [], [], []
oid = 1
for k, (oname, parts, (bx, by)) in enumerate(objects):
    allv = np.concatenate([p[1].reshape(-1, 3) for p in parts])
    lo, hi = allv.min(0), allv.max(0); ctr = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]])
    comps, pcfg = [], []
    for pname, T, ext in parts:
        T = T - ctr; pc = (T.reshape(-1, 3).min(0) + T.reshape(-1, 3).max(0)) / 2
        x, nf = mesh_xml(oid, T - pc); mesh_objs.append(x)
        comps.append(f'    <component p:path="/3D/Objects/object_1.model" objectid="{oid}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 {pc[0]:.6f} {pc[1]:.6f} {pc[2]:.6f}"/>')
        pcfg.append(f'''    <part id="{oid}" subtype="normal_part">
      <metadata key="name" value="{pname}"/>
      <metadata key="matrix" value="1 0 0 {pc[0]:.6f} 0 1 0 {pc[1]:.6f} 0 0 1 {pc[2]:.6f} 0 0 0 1"/>
      <metadata key="extruder" value="{ext}"/>
      <mesh_stat face_count="{nf}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>''')
        oid += 1
    aid = 100 + k
    model_objs.append(f'  <object id="{aid}" p:UUID="{uuid.uuid4()}" type="model">\n   <components>\n' + '\n'.join(comps) + '\n   </components>\n  </object>')
    build.append(f'  <item objectid="{aid}" p:UUID="{uuid.uuid4()}" transform="1 0 0 0 1 0 0 0 1 {bx} {by} 0" printable="1"/>')
    cfg.append(f'  <object id="{aid}">\n    <metadata key="name" value="{oname}"/>\n    <metadata key="extruder" value="1"/>\n' + '\n'.join(pcfg) + '\n  </object>')

NS = 'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p"'
main = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" {NS}>
 <metadata name="Application">BambuStudio-02.07.01.62</metadata>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <metadata name="Title">SO-101 D435 tags 4 and 5</metadata>
 <resources>
{chr(10).join(model_objs)}
 </resources>
 <build p:UUID="{uuid.uuid4()}">
{chr(10).join(build)}
 </build>
</model>
'''
objs = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" {NS}>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <resources>
{chr(10).join(mesh_objs)}
 </resources>
 <build/>
</model>
'''
inst = '\n'.join(f'    <model_instance>\n      <metadata key="object_id" value="{100 + k}"/>\n      <metadata key="instance_id" value="0"/>\n    </model_instance>' for k in range(len(objects)))
settings = '<?xml version="1.0" encoding="UTF-8"?>\n<config>\n' + '\n'.join(cfg) + f'''
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value=""/>
    <metadata key="locked" value="false"/>
    <metadata key="filament_map_mode" value="Auto For Flush"/>
    <metadata key="filament_maps" value="1 1 1 1"/>
    <metadata key="filament_volume_maps" value="0 0 0 0"/>
{inst}
  </plate>
  <assemble>
  </assemble>
</config>
'''
ctypes = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Default Extension="config" ContentType="text/xml"/>
</Types>
'''
rels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
'''
mrels = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
'''
path = OUT / 'd435_tags_4_5_AMS.3mf'
with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', ctypes); z.writestr('_rels/.rels', rels)
    z.writestr('3D/3dmodel.model', main); z.writestr('3D/_rels/3dmodel.model.rels', mrels)
    z.writestr('3D/Objects/object_1.model', objs); z.writestr('Metadata/model_settings.config', settings)
    with zipfile.ZipFile(TEMPLATE) as t:
        for n in ('Metadata/project_settings.config', 'Metadata/slice_info.config', 'Metadata/filament_sequence.json'):
            z.writestr(n, t.read(n))
print('wrote', path, path.stat().st_size, 'bytes')
