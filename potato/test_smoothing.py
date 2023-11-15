# pyright: reportUnknownMemberType=false

import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

def smooth_path(path):
    num_points = max(10, math.ceil(len(arr) / 5))
    tck, u = interpolate.splprep(path.T, s=0)
    u = np.linspace(0.0, 1.0, num_points)
    return np.column_stack(interpolate.splev(u, tck))

arr = np.array([(0, 0), (1, 0.4), (2, 1.0), (3, 1.4), (4, 1.8), (4.6, 2), (5, 2.2), (6, 2.6), (7, 3.0), (8, 3.4), (9, 3.8), (9.6, 4), (10, 4.2), (11, 4.6), (12, 5.0), (13, 5.4), (14, 5.8), (14.6, 6), (15, 6.2), (16, 6.6), (17, 7.0), (18, 7.2), (19, 7.6), (20, 8.0), (21, 8.4), (22, 8.8), (23, 9.0), (24, 10.0), (25, 11.0), (25.0, 12), (25.0, 13), (26, 14.0), (27, 15.0), (28, 15.4), (29, 16.0), (30, 16.4), (31, 16.8), (32, 17.0), (33, 17.4), (34, 17.8), (34.6, 18), (35, 18.2), (36, 18.8), (36.6, 19), (37, 19.2), (38, 19.6), (39, 20.0), (40, 20.0), (41, 20.4), (42, 20.8), (43, 21.0), (44, 22.0), (45, 23.0), (45.4, 24), (46, 25.0), (46.4, 26), (46.8, 27), (47, 28.0), (48, 29.0), (49, 29.8), (49.2, 30), (50, 30.6), (50.4, 31), (51, 31.4), (51.8, 32), (52, 32.2), (53, 33.0), (54, 34.0), (55, 35.0), (56, 36.0), (57, 37.0), (58, 38.0), (59, 39.0)])
x, y = zip(*arr)
B = smooth_path(arr)
plt.scatter(x, y)
plt.plot(B[:, 0], B[:, 1])
plt.show()