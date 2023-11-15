import math
import numpy as np
from scipy import interpolate
from nptyping import NDArray, Float, Shape


def smooth_path(path: list[tuple[float, float]]) -> NDArray[Shape["20, 2"], Float]:
    path_as_array = np.array(path)
    num_points = max(10, math.ceil(len(path) / 5))
    tck, u = interpolate.splprep(path_as_array.T, s=0) # type: ignore
    u = np.linspace(0.0, 1.0, num_points)
    return np.column_stack(interpolate.splev(u, tck)) # type: ignore