# FreeCADCmd script (14 Nov 2026): export the pink underfoot cap with the two AprilTag holders (ids 0, 1) and the tag
# inserts from the user's review FCStd, in the FCStd global frame (mm), and print where everything is.
# FCStd frame: base_so101_v2.stl (mm) rotated +90 deg about X ("plat op onderzijde"), see SO101_Foot_Mesh placement.
# Run: "C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe" export_foot_tags.py   (FCSTD path below)
import json
import os

import FreeCAD as App
import Mesh
import MeshPart

HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else r'C:\projects\robots\so101\scene\custom_mounts\foot_tags'
FCSTD = os.environ.get('FOOT_FCSTD', os.path.join(HERE, 'so101_foot_with_apriltag_holders_review.FCStd'))
doc = App.openDocument(FCSTD)
info = {}
for name in ('SO101_Underfoot_Cap_AprilTag_Holders', 'AprilTag_Left_ID0_White', 'AprilTag_Left_ID0_Black',
             'AprilTag_Right_ID1_White', 'AprilTag_Right_ID1_Black'):
    o = doc.getObject(name)
    sh = o.Shape.copy()          # Shape already carries the object's Placement
    m = MeshPart.meshFromShape(Shape=sh, LinearDeflection=0.05, AngularDeflection=0.3)
    m.write(os.path.join(HERE, name + '.stl'))
    bb = sh.BoundBox
    info[name] = dict(min=[bb.XMin, bb.YMin, bb.ZMin], max=[bb.XMax, bb.YMax, bb.ZMax], center=[bb.Center.x, bb.Center.y, bb.Center.z])
fm = doc.getObject('SO101_Foot_Mesh')
mb = fm.Mesh.BoundBox
info['SO101_Foot_Mesh'] = dict(min=[mb.XMin, mb.YMin, mb.ZMin], max=[mb.XMax, mb.YMax, mb.ZMax],
                               placement=[list(fm.Placement.Base), list(fm.Placement.Rotation.Axis), fm.Placement.Rotation.Angle])
json.dump(info, open(os.path.join(HERE, 'foot_tags_info.json'), 'w'), indent=1)
print(json.dumps(info, indent=1))
