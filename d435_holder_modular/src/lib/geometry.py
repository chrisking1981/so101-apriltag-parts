from math import sin, cos, radians
from cadgen import build123d as bd

ANGLE = 30
PANEL_SIZE = 64
THICKNESS = 4.5
POCKET = 60.4
DEPTH = 1.1
TAB_WIDTH = 16
TAB_LENGTH = 20
SLOT_WIDTH = 16.4
SLOT_THICKNESS = 4.9

def panel(side):
    # Printed flat, marker facing +Z. Tongue is coplanar with the panel.
    body = bd.Pos(0, 0, THICKNESS/2) * bd.Box(64,64,THICKNESS)
    tongue = bd.Pos(-side*20, -41, THICKNESS/2)*bd.Box(TAB_WIDTH,22,THICKNESS)
    body += tongue
    pocket = bd.Pos(0,0,THICKNESS-DEPTH/2+0.5)*bd.Box(POCKET,POCKET,DEPTH+1)
    body -= pocket
    body.label = 'Left marker panel' if side == -1 else 'Right marker panel'
    return body.clean()

def placement(side):
    # Front marker surfaces point in the camera lens direction, toward -Y.
    return bd.Pos(side*(14+20*cos(radians(30))),24,66)*bd.Rot(0,0,side*30)*bd.Rot(90,0,0)

def socket_transform(side):
    # Tongue local coordinates center X=-side*20, Y=-42, Z=2.25.
    return placement(side)*bd.Pos(-side*20,-42,THICKNESS/2)

def base():
    # Flat bottom; slots open upward. Mounting holes run through the rear bar.
    body=bd.Pos(0,17,3.5)*bd.Box(62,34,21)
    for side in (-1,1):
        pose=socket_transform(side)
        socket=pose*bd.Box(21,20,9.5)
        body += socket
    for side in (-1,1):
        # Open above top face, closed floor at Z=14 for the tongue tips.
        pose=socket_transform(side)
        slot=pose*bd.Pos(0,0.5,0)*bd.Box(SLOT_WIDTH,21,SLOT_THICKNESS)
        body -= slot
    for x in (-22.5,22.5):
        # Counterbore from rear leaves a 4 mm wall against camera.
        bore=bd.Pos(x,17,0)*bd.Rot(90,0,0)*bd.Cylinder(1.7,36)
        access=bd.Pos(x,20,0)*bd.Rot(90,0,0)*bd.Cylinder(3.2,32)
        body=body-bore-access
    body.label='D435 base with two angled sockets'
    return body.clean()
