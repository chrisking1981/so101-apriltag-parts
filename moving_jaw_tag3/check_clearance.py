"""Clearance of the new jaw's platform + 1 mm tag against the swept gripper obstacles (swept_obstacles_mm.npy from
free_space.py, all fixed parts over the full joint range, in the jaw mesh frame). Sim venv."""
import json
import struct

import numpy as np
from scipy.spatial import cKDTree


def load(p):
    b = open(p, 'rb').read(); n = struct.unpack('<I', b[80:84])[0]
    return np.frombuffer(b[84:84 + n * 50], dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]))['v'].astype(float)


def sample(T, step=0.4):
    A = np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1) / 2
    k = np.maximum(1, (A / step ** 2).astype(int)); i = np.repeat(np.arange(len(T)), k)
    u = np.random.default_rng(1).random((len(i), 2)); s = u.sum(1) > 1; u[s] = 1 - u[s]
    return T[i, 0] + u[:, :1] * (T[i, 1] - T[i, 0]) + u[:, 1:] * (T[i, 2] - T[i, 0])


info = json.load(open('moving_jaw_tag3_info.json'))
f = info['face']
P = sample(load('platform_only.stl'))
yy, zz = np.meshgrid(np.linspace(*f['y'], 60), np.linspace(*f['z'], 60))
tag = np.c_[np.full(yy.size, f['x'] + 1.0), yy.ravel(), zz.ravel()]
O = np.load('swept_obstacles_mm.npy').astype(float)
tree = cKDTree(O)
for name, Q in (('platform', P), ('tag face (x + 1 mm)', tag)):
    dd, ii = tree.query(Q)
    k = dd.argmin()
    print('%-20s min clearance %.1f mm at %s (obstacle at %s)' % (name, dd[k], np.round(Q[k], 1), np.round(O[ii[k]], 1)))
# also: how close could the face come to the pivot? clearance of the tag edge row y = f['y'][1]
edge = tag[np.isclose(tag[:, 1], f['y'][1])]
print('pivot-side tag edge min clearance %.1f mm' % tree.query(edge)[0].min())
