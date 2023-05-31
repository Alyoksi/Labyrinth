from constants import *


def calc_width(width):
    return ((width * 2 - 1) // 2 + 1) * width_line + ((width * 2 - 1) // 2) * width_walls + border * 2


def cacl_height(height):
    return ((height * 2 - 1) // 2 + 1) * width_line + ((height * 2 - 1) // 2) * width_walls + border * 2
