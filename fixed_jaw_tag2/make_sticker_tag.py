# FreeCADCmd script: AprilTag tag36h11 id 2 sticker (36 mm, 30 mm black, 1 mm thick, 0.2 mm black layer on top).
# Black cells are grown by 0.01 mm so cells that only touch at a corner overlap a little: the black part and the white
# part are then clean manifold solids (Bambu reported non-manifold edges / reversed faces on the corner-touching grid).
# Run: "C:\Program Files\FreeCAD 1.1\bin\FreeCADCmd.exe" make_sticker_tag.py
import os

import FreeCAD as App
import MeshPart
import Part

HERE = r'C:\projects\robots\so101\cad_parts\wrist_tag'
V = App.Vector
INSERT, DET, INS_T, BLACK_T, GROW = 36.0, 30.0, 1.0, 0.2, 0.01
GRID = ('11111111', '11000111', '11101111', '10110111', '11111101', '11011011', '10001001', '11111111')   # OpenCV id 2

q = (INSERT - DET) / 2; cell = DET / 8
cells = [Part.makeBox(cell + 2 * GROW, cell + 2 * GROW, BLACK_T, V(q + c * cell - GROW, q + (7 - r) * cell - GROW, INS_T - BLACK_T))
         for r, bits in enumerate(GRID) for c, b in enumerate(bits) if b == '1']
black = cells[0].multiFuse(cells[1:]).removeSplitter()
white = Part.makeBox(INSERT, INSERT, INS_T).cut(black).removeSplitter()
for n, s in (('black', black), ('white', white)):
    print(n, 'valid', s.isValid(), 'solids', len(s.Solids), 'closed', all(sh.isClosed() for sh in s.Shells), 'vol', round(s.Volume, 2))
for shp, fn in ((white, 'tag2_sticker_WHITE.stl'), (black, 'tag2_sticker_BLACK.stl')):
    m = MeshPart.meshFromShape(Shape=shp, LinearDeflection=0.03, AngularDeflection=0.2)
    m.harmonizeNormals()
    print(fn, 'facets', m.CountFacets, 'solid', m.isSolid(), 'non-manifolds', m.hasNonManifolds())
    m.write(os.path.join(HERE, fn))
