import numpy as np
from matplotlib.colors import hsv_to_rgb


def get_colors(num_colors):
    x = np.linspace(0.0, 1.0, num_colors)
    a = np.floor(x * x * np.sqrt(num_colors))
    v = 1.0 - a / (np.max(a) + 1)
    h = x * x * (np.max(a) + 1)
    h = h - np.floor(h)
    hsv = np.ones([num_colors, 3])
    hsv[:, 0] = h
    hsv[:, 1] = v
    hsv[:, 2] = 1.0
    rgb = hsv_to_rgb(hsv)
    rgba = np.ones([num_colors, 4])
    rgba[:, 0:3] = rgb
    return rgba
