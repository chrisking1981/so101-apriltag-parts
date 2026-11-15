from cadgen import step, build123d as bd
from lib.geometry import base, panel, placement
@step(out='../STEP/assembly.step')
def assembly():
    b=base(); b.color=bd.Color(0.3,0.35,0.4)
    l=placement(-1)*panel(-1);l.color=bd.Color(0.2,0.55,0.7)
    r=placement(1)*panel(1);r.color=bd.Color(0.35,0.65,0.45)
    return bd.Compound(children=[b,l,r])
if __name__=='__main__':
    assembly()
