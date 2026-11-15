from cadgen import step
from lib.geometry import base as make_base
@step(out='../STEP/base.step')
def base():
    return make_base()
if __name__=='__main__':
    base()
