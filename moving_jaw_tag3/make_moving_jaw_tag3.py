# FreeCADCmd script (15 Nov 2026): new moving jaw = official TheRobotStudio Moving_Jaw_SO101.stl (GitHub, mm, same
# frame as the URDF mesh moving_jaw_so101_v1.stl) + an integrated platform with a flat 36 x 36 face for a glue-on
# AprilTag tag36h11 id 3 (the 36 x 36 x 1 two-colour tag from cad_parts/wrist_tag/tag3_sticker_*.stl).
#
# Where: as close to the pivot as the gripper allows. At the height of tag 2 (jaw y ~ -2) the gripper servo and the
# wrist sweep through the space outside the jaw over the joint range (free_space.py), free space starts at y ~ -15.
# Platform: face plane x = XF (normal +x = outside of the jaw, radial to the joint axis), y Y0..Y0-36, z +-18.
# Each cross-section is a trapezoid from the finger's outer face (x = 7.51 + 0.1055 (y + 24), half-height h(y)) out to
# the face; the slanted sides are >= 45 deg so nothing overhangs when the jaw is printed tag face down.
# Run: "C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe" make_moving_jaw_tag3.py
import json
import os

import FreeCAD as App
import Mesh
import MeshPart
import Part

HERE = r'C:\projects\robots\so101\cad_parts\moving_jaw_tag'
SRC = os.path.join(HERE, 'download', 'Moving_Jaw_SO101.stl')
V = App.Vector
XF = 15.0
Y0 = -16.0                          # pivot-side edge of the tag face
SIDE = 36.0
H = {-60: 7.28, -58: 7.43, -56: 7.57, -54: 7.71, -52: 7.85, -50: 7.99, -48: 8.13, -46: 8.27, -44: 8.42, -42: 8.57,
     -40: 8.73, -38: 8.93, -36: 9.13, -34: 9.38, -32: 9.63, -30: 9.90, -28: 10.23, -26: 10.65, -24: 11.33}
xo = lambda y: 7.51 + 0.1055 * (y + 24)
h = lambda y: H[max(min(int(round(y / 2.0)) * 2, -24), -60)]

mesh = Mesh.Mesh(SRC)
mesh.removeDuplicatedPoints(); mesh.removeDuplicatedFacets(); mesh.fixIndices(); mesh.fixDegenerations(0.0); mesh.harmonizeNormals()
comps = mesh.getSeparateComponents()
print('official jaw: facets', mesh.CountFacets, 'components', len(comps), 'solid', mesh.isSolid(), 'bb', mesh.BoundBox)
sh = Part.Shape(); sh.makeShapeFromMesh(mesh.Topology, 0.05); jaw = Part.makeSolid(sh)
print('jaw solid valid', jaw.isValid(), 'vol', round(jaw.Volume))

wires = []
ys = [Y0 - SIDE + k * SIDE / 12 for k in range(13)]
min_angle = 90
for y in ys:
    x0 = xo(y) - 1.0; hz = h(y) - 0.6          # start 1 mm inside the finger so the fuse is solid
    wires.append(Part.makePolygon([V(x0, y, -hz), V(XF, y, -SIDE / 2), V(XF, y, SIDE / 2), V(x0, y, hz), V(x0, y, -hz)]))
    import math
    min_angle = min(min_angle, math.degrees(math.atan2(XF - x0, SIDE / 2 - hz)))
plat = Part.makeLoft(wires, True, True)
print('platform valid', plat.isValid(), 'vol', round(plat.Volume), 'steepest side vs bed (deg) %.1f (>= 45 ok)' % min_angle)
new = jaw.fuse(plat).removeSplitter()
print('new jaw valid', new.isValid(), 'solids', len(new.Solids), 'vol', round(new.Volume), 'added', round(new.Volume - jaw.Volume))

doc = App.newDocument('MovingJawTag3')
o = doc.addObject('Part::Feature', 'Moving_Jaw_Tag3'); o.Shape = new
doc.recompute(); doc.saveAs(os.path.join(HERE, 'Moving_Jaw_SO101_tag3.FCStd'))
Part.export([o], os.path.join(HERE, 'Moving_Jaw_SO101_tag3.step'))
mm = MeshPart.meshFromShape(Shape=new, LinearDeflection=0.02, AngularDeflection=0.15); mm.harmonizeNormals()
print('mesh facets', mm.CountFacets, 'solid', mm.isSolid(), 'non-manifold', mm.hasNonManifolds())
mm.write(os.path.join(HERE, 'Moving_Jaw_SO101_tag3.stl'))
MeshPart.meshFromShape(Shape=plat, LinearDeflection=0.02, AngularDeflection=0.15).write(os.path.join(HERE, 'platform_only.stl'))
json.dump(dict(tag_id=3, family='tag36h11', black_square_mm=30.0, tag_centre_mm=[XF + 1.0, Y0 - SIDE / 2, 0.0], tag_normal=[1, 0, 0],
               tag_up='glue with tag row 0 towards -y (finger tip) or +y: state which when calibrating',
               frame='Moving_Jaw_SO101.stl / moving_jaw_so101_v1.stl mesh coordinates (mm)',
               face=dict(x=XF, y=[Y0 - SIDE, Y0], z=[-SIDE / 2, SIDE / 2])),
          open(os.path.join(HERE, 'moving_jaw_tag3_info.json'), 'w'), indent=1)
print('done')
