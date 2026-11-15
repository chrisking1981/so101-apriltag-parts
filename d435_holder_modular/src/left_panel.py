from cadgen import step
from lib.geometry import panel
@step(out='../STEP/left_panel.step')
def left_panel():
    return panel(-1)
if __name__=='__main__':
    left_panel()
