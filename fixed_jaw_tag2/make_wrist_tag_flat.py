# FreeCADCmd script (15 Nov 2026): flat press-on holder for the stick-on tag 2 (replaces the pocket version, whose
# 36 mm pocket floor became a sagging bridge when printed face down).
# Same fit on the official Wrist_Cam_Mount_32x32_UVC_Module_SO101 fixed jaw as make_wrist_tag_clip.py: Ø9.85 peg in
# the Ø10 hole (2 mm below the tag centre -> fits one way only), two side lips clamping the side walls (no turning).
# New: the front is a plain flat 36 x 36 mm face, exactly the size of the tag; the tag (36 x 36 x 1) is glued on it.
# The hook lip under the block is dropped so nothing sticks out beyond the 36 x 36 square.
# Print: flat face on the bed, peg and lips up: no bridges, no support.
# Run: "C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe" make_wrist_tag_flat.py
import json
import os

import FreeCAD as App
import Mesh
import MeshPart
import Part

HERE = r'C:\projects\robots\so101\cad_parts\wrist_tag'
SRC = r'C:\projects\robots\so101\scene\custom_mounts\wrist_cam_mount_download\mount_binary.stl'
V = App.Vector

BACK_X = -35.2
PLATE_T = 3.0
X_OUT = BACK_X - PLATE_T                # flat face; the 1 mm tag goes on it -> tag face at X_OUT - 1
CY, CZ = 0.0, 26.35                     # tag centre
SIDE = 36.0                             # plate = tag size
PEG_Y, PEG_Z, PEG_D, PEG_L, PEG_CH = 0.13, 24.35, 9.85, 6.0, 0.8
WALL_Y, CLAMP = 16.0, 0.05
LIP_T, LIP_X1, LIP_Z = 2.0, -28.0, (9.0, 31.0)
inner = WALL_Y - CLAMP
assert inner + LIP_T <= SIDE / 2 and LIP_Z[0] >= CZ - SIDE / 2

mesh = Mesh.Mesh(SRC)
mesh.removeDuplicatedPoints(); mesh.removeDuplicatedFacets(); mesh.fixIndices(); mesh.fixDegenerations(0.0); mesh.harmonizeNormals()
jaw = sorted(mesh.getSeparateComponents(), key=lambda c: -c.CountFacets)[0]
sh = Part.Shape(); sh.makeShapeFromMesh(jaw.Topology, 0.05); jaw_solid = Part.makeSolid(sh)

plate = Part.makeBox(PLATE_T, SIDE, SIDE, V(X_OUT, CY - SIDE / 2, CZ - SIDE / 2))
lips = [Part.makeBox(LIP_X1 - BACK_X, LIP_T, LIP_Z[1] - LIP_Z[0], V(BACK_X - 0.01, inner if s > 0 else -inner - LIP_T, LIP_Z[0])) for s in (1, -1)]
ribs = [Part.makeBox(0.5, SIDE / 2 - inner, LIP_Z[1] - LIP_Z[0], V(BACK_X - 0.3, inner if s > 0 else -SIDE / 2, LIP_Z[0])) for s in (1, -1)]
peg = Part.makeCylinder(PEG_D / 2, PEG_L - PEG_CH, V(BACK_X - 0.01, PEG_Y, PEG_Z), V(1, 0, 0))
tip = Part.makeCone(PEG_D / 2, PEG_D / 2 - PEG_CH, PEG_CH, V(BACK_X - 0.01 + PEG_L - PEG_CH, PEG_Y, PEG_Z), V(1, 0, 0))
holder = plate.fuse([*lips, *ribs, peg, tip]).removeSplitter()
bb = holder.BoundBox
print('holder valid', holder.isValid(), 'solids', len(holder.Solids), 'volume mm3', round(holder.Volume),
      'bbox y %.2f..%.2f z %.2f..%.2f x %.2f..%.2f' % (bb.YMin, bb.YMax, bb.ZMin, bb.ZMax, bb.XMin, bb.XMax))
print('overlap with the official jaw (mm3): %.2f' % holder.common(jaw_solid).Volume)
for name, s in (('peg', peg.fuse(tip)), ('plate', plate), ('lips', lips[0].fuse(lips[1]))):
    print('  overlap', name, round(s.common(jaw_solid).Volume, 3))

doc = App.newDocument('WristTag2_Flat')
o = doc.addObject('Part::Feature', 'Tag2_Flat_Holder'); o.Shape = holder
doc.recompute(); doc.saveAs(os.path.join(HERE, 'wrist_tag2_flat.FCStd'))
Part.export([o], os.path.join(HERE, 'wrist_tag2_flat.step'))
MeshPart.meshFromShape(Shape=holder, LinearDeflection=0.03, AngularDeflection=0.2).write(os.path.join(HERE, 'wrist_tag2_flat.stl'))
json.dump(dict(tag_id=2, family='tag36h11', black_square_mm=30.0, tag_centre_mm=[X_OUT - 1.0, CY, CZ], tag_normal=[-1, 0, 0], tag_up=[0, 0, 1],
               frame='Wrist_Cam_Mount_32x32_UVC_Module_SO101.stl coordinates (mm)',
               part='wrist_tag2_flat.stl (press-on) + glued 36x36x1 tag (tag2_sticker_*.stl)'),
          open(os.path.join(HERE, 'wrist_tag2_flat_info.json'), 'w'), indent=1)
print('done')
