# FreeCADCmd script: glue-on AprilTag tag36h11 ids 4 and 5 for the D435 (same design as the printed tag-2 sticker:
# 60 x 60 x 1 mm, 50 mm black square like the foot tags, black = top 0.2 mm, printed face up: white on the bed).
# Grids from cv2.aruco DICT_APRILTAG_36h11 generateImageMarker(id, 8), '1' = black (id 2 matches the printed sticker).
# Run: "C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe" make_d435_tags.py
import os

import FreeCAD as App
import MeshPart
import Part

HERE = r'C:\projects\robots\so101\cad_parts\d435_tags'
V = App.Vector
INSERT, DET, INS_T, BLACK_T, GROW = 60.0, 50.0, 1.0, 0.2, 0.01   # same size as the foot tags id 0/1 (60 mm, 50 mm black)
GRIDS = {4: ('11111111', '11011101', '11111101', '11010111', '10000101', '11100001', '11010001', '11111111'),
         5: ('11111111', '11100101', '11000111', '10010101', '11001001', '10111001', '11100001', '11111111')}

q = (INSERT - DET) / 2; cell = DET / 8
for tid, grid in GRIDS.items():
    cells = [Part.makeBox(cell + 2 * GROW, cell + 2 * GROW, BLACK_T, V(q + c * cell - GROW, q + (7 - r) * cell - GROW, INS_T - BLACK_T))
             for r, bits in enumerate(grid) for c, b in enumerate(bits) if b == '1']
    black = cells[0].multiFuse(cells[1:]).removeSplitter()
    white = Part.makeBox(INSERT, INSERT, INS_T).cut(black).removeSplitter()
    for shp, col in ((white, 'WHITE'), (black, 'BLACK')):
        m = MeshPart.meshFromShape(Shape=shp, LinearDeflection=0.03, AngularDeflection=0.2)
        m.harmonizeNormals()
        fn = 'tag%d_sticker_%s.stl' % (tid, col)
        print(fn, 'valid', shp.isValid(), 'facets', m.CountFacets, 'solid', m.isSolid(), 'non-manifolds', m.hasNonManifolds())
        m.write(os.path.join(HERE, fn))
