"""Render the gripper (model meshes) + wrist cam mount + tag-2 holder and an optional new moving jaw. Sim venv.
python render_gripper.py OUT.png [moving_jaw_stl_mm] [gripper_deg]
"""
import sys

import mujoco
import numpy as np
from PIL import Image, ImageDraw

R = 'C:/projects/robots/so101/'
out = sys.argv[1]; newjaw = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
qdeg = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
spec = mujoco.MjSpec.from_file(R + 'scene/so101.xml')
spec.visual.global_.offwidth = 800; spec.visual.global_.offheight = 800
g = spec.body('gripper'); fol = [x for x in g.geoms if x.meshname == 'wrist_roll_follower_so101_v1'][0]
for name, f, rgba in (('mount', R + 'scene/custom_mounts/wrist_cam_mount_download/mount_binary.stl', [0.95, 0.75, 0.25, 1]),
                      ('t2h', R + 'cad_parts/wrist_tag/wrist_tag2_flat.stl', [1, 0.45, 0.72, 1])):
    spec.add_mesh(name=name, file=f, scale=[0.001] * 3, inertia=mujoco.mjtMeshInertia.mjMESH_INERTIA_SHELL)
    g.add_geom(type=mujoco.mjtGeom.mjGEOM_MESH, meshname=name, pos=fol.pos, quat=fol.quat, rgba=rgba, contype=0, conaffinity=0, group=1)
fol.rgba = [0, 0, 0, 0]
mj = spec.body('moving_jaw_so101_v1'); mjg = [x for x in mj.geoms if x.meshname == 'moving_jaw_so101_v1'][0]
if newjaw:
    spec.add_mesh(name='newjaw', file=newjaw, scale=[0.001] * 3, inertia=mujoco.mjtMeshInertia.mjMESH_INERTIA_SHELL)
    mj.add_geom(type=mujoco.mjtGeom.mjGEOM_MESH, meshname='newjaw', pos=mjg.pos, quat=mjg.quat, rgba=[0.45, 0.8, 1, 1], contype=0, conaffinity=0, group=1)
    mjg.rgba = [0, 0, 0, 0]
m = spec.compile(); d = mujoco.MjData(m)
j = [i for i in range(m.njnt) if m.jnt_bodyid[i] == m.body('moving_jaw_so101_v1').id][0]
d.qpos[m.jnt_qposadr[j]] = np.radians(qdeg); mujoco.mj_forward(m, d)
gb = m.body('gripper').id; Rg = d.xmat[gb].reshape(3, 3); pg = d.xpos[gb]
look = pg + Rg @ np.array([-0.01, 0.0, -0.06])
r = mujoco.Renderer(m, 600, 600); opt = mujoco.MjvOption(); opt.geomgroup[:] = 1
W = Image.new('RGB', (1800, 600))
for k, (nme, v) in enumerate((('from -x (tag 2 side)', np.array([-1, 0, 0.0])), ('from +x (moving jaw outside)', np.array([1, 0, 0.0])), ('from +y (side)', np.array([0, 1, 0.0])))):
    vw = Rg @ v; vw /= np.linalg.norm(vw)
    c = mujoco.MjvCamera(); c.lookat[:] = look; c.distance = 0.20
    c.azimuth = np.degrees(np.arctan2(-vw[1], -vw[0])); c.elevation = np.degrees(np.arcsin(-vw[2]))
    r.update_scene(d, c, opt); im = Image.fromarray(r.render()); ImageDraw.Draw(im).text((8, 8), nme, fill=(0, 0, 0)); W.paste(im, (k * 600, 0))
W.save(out); print('saved', out)
