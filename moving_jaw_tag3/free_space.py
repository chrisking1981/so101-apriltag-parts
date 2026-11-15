"""Swept obstacles in the moving-jaw mesh frame (mm) over the gripper range, and clearance of candidate tag plates.
Sim venv: python free_space.py"""
import json

import mujoco
import numpy as np
from scipy.spatial import cKDTree

R = 'C:/projects/robots/so101/'
spec = mujoco.MjSpec.from_file(R + 'scene/so101.xml')
g = spec.body('gripper'); fol = [x for x in g.geoms if x.meshname == 'wrist_roll_follower_so101_v1'][0]
spec.add_mesh(name='mount', file=R + 'scene/custom_mounts/wrist_cam_mount_download/mount_binary.stl', scale=[0.001] * 3, inertia=mujoco.mjtMeshInertia.mjMESH_INERTIA_SHELL)
g.add_geom(name='mountg', type=mujoco.mjtGeom.mjGEOM_MESH, meshname='mount', pos=fol.pos, quat=fol.quat, contype=0, conaffinity=0)
spec.add_mesh(name='t2h', file=R + 'cad_parts/wrist_tag/wrist_tag2_flat.stl', scale=[0.001] * 3, inertia=mujoco.mjtMeshInertia.mjMESH_INERTIA_SHELL)
g.add_geom(name='t2hg', type=mujoco.mjtGeom.mjGEOM_MESH, meshname='t2h', pos=fol.pos, quat=fol.quat, contype=0, conaffinity=0)
m = spec.compile(); d = mujoco.MjData(m)
mjb = m.body('moving_jaw_so101_v1').id
jg = [x for x in range(m.ngeom) if m.geom_bodyid[x] == mjb and m.geom_dataid[x] >= 0 and mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_MESH, m.geom_dataid[x]) == 'moving_jaw_so101_v1'][0]
j = [i for i in range(m.njnt) if m.jnt_bodyid[i] == mjb][0]
lo, hi = m.jnt_range[j]


def surf(gid, step=0.0007):
    mid = m.geom_dataid[gid]; va = m.mesh_vertadr[mid]; fa = m.mesh_faceadr[mid]
    V = m.mesh_vert[va:va + m.mesh_vertnum[mid]]; F = m.mesh_face[fa:fa + m.mesh_facenum[mid]]
    T = V[F]; A = np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1) / 2
    k = np.maximum(1, (A / step ** 2).astype(int)); idx = np.repeat(np.arange(len(T)), k)
    u = np.random.default_rng(0).random((len(idx), 2)); s = u.sum(1) > 1; u[s] = 1 - u[s]
    return T[idx, 0] + u[:, :1] * (T[idx, 1] - T[idx, 0]) + u[:, 1:] * (T[idx, 2] - T[idx, 0])


# mesh-file frame of the moving jaw <- its geom frame (MuJoCo recentred the mesh)
mid = m.geom_dataid[jg]
Rm = np.zeros(9); mujoco.mju_quat2Mat(Rm, m.mesh_quat[mid]); Rm = Rm.reshape(3, 3); pm = m.mesh_pos[mid]
fixed = [x for x in range(m.ngeom) if m.geom_bodyid[x] != mjb and m.geom_type[x] == mujoco.mjtGeom.mjGEOM_MESH
         and 'convex' not in (mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_MESH, m.geom_dataid[x]) or '')]
S = {x: surf(x) for x in fixed}
pts = []
for q in np.radians(np.arange(np.degrees(lo), np.degrees(hi) + 0.1, 2.0)):
    d.qpos[:] = 0; d.qpos[m.jnt_qposadr[j]] = q; mujoco.mj_forward(m, d)
    Rj = d.geom_xmat[jg].reshape(3, 3); pj = d.geom_xpos[jg]
    for x, P in S.items():
        W = P @ d.geom_xmat[x].reshape(3, 3).T + d.geom_xpos[x]
        Lg = (W - pj) @ Rj                      # in the jaw geom frame
        Lm = Lg @ Rm.T + pm                      # in the jaw mesh-file frame
        k = (np.abs(Lm[:, 2]) < 0.04) & (Lm[:, 0] > -0.03) & (Lm[:, 0] < 0.05) & (Lm[:, 1] > -0.09) & (Lm[:, 1] < 0.04)
        pts.append(Lm[k])
P = np.concatenate(pts) * 1000
print('swept obstacle points', len(P))
np.save('swept_obstacles_mm.npy', P.astype(np.float32))
# free outer boundary: per (y, z) cell, the max x of obstacles (for x > 0 region) -> a plate must stay above it
ys = np.arange(-40, 22, 3); zs = np.arange(-24, 25, 4)
print('max obstacle x (mm) per cell, only points with x > -2; rows z, cols y from', ys[0])
for z in zs[::-1]:
    row = []
    for y in ys:
        k = (abs(P[:, 1] - y) < 1.5) & (abs(P[:, 2] - z) < 2) & (P[:, 0] > -2)
        row.append('  .' if not k.any() else '%3d' % round(P[k, 0].max()))
    print('%4d ' % z + ' '.join(row))
