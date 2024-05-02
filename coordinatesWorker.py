import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

from constants import BLACK_COLOR


def getImageCoordinates(data):
    xy = []
    for row_ind, row in enumerate(data):
        for col_ind, color in enumerate(row):
            if color == BLACK_COLOR:
                # Получаем координаты синих точек с изображения.
                # Инвертируем систему координат
                # (у изображений начало координат слева сверху - нам же нужно слева снизу).
                xy.append((col_ind, len(data) - row_ind - 1))
    return xy

def scale(numbers_list, min, max):
    np_arr = np.array(numbers_list)
    normalized = (np_arr - np_arr.min()) / np_arr.max()
    return normalized * (max - min) + min


def getGraphicFunction(x, y):
    return interpolate.interp1d(x, y, kind='linear')
