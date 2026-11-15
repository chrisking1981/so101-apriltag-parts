from cadgen import step,build123d as bd
from lib.geometry import base,panel
@step(out='../STEP/print_layout.step')
def print_layout():
    b=bd.Pos(0,0,7)*base();b.color=bd.Color(.3,.35,.4)
    l=bd.Pos(-70,80,0)*panel(-1);l.color=bd.Color(.2,.55,.7)
    r=bd.Pos(5,80,0)*panel(1);r.color=bd.Color(.35,.65,.45)
    return bd.Compound(children=[b,l,r])
if __name__=='__main__':
    print_layout()
