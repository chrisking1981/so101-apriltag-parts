from cadgen import step
from lib.geometry import panel
@step(out='../STEP/right_panel.step')
def right_panel():
    return panel(1)
if __name__=='__main__':
    right_panel()
