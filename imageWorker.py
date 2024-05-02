import cv2 as cv
import matplotlib.pyplot as plt

from constants import *


def makeBlackAndWhite(image):
    threshold = 128
    img_binary = cv.threshold(image, threshold, 255, cv.THRESH_BINARY)[1]
    return img_binary


def removeHorizontalAxes(image):
    rows_count = len(image)
    cols_count = len(image[0])

    img_binary_without_rows = image.copy()
    last_row_ind = 0
    first_row_ind = 0

    for row_ind in range(rows_count):
        counter = 0
        for col_ind in range(cols_count):
            if image[row_ind][col_ind] == BLACK_COLOR:
                counter += 1
        if counter >= LINE_THRESHOLD * cols_count:
            last_row_ind = row_ind
            for col_ind in range(cols_count):
                img_binary_without_rows[row_ind][col_ind] = WHITE_COLOR
            if first_row_ind == 0:
                first_row_ind = row_ind

    if last_row_ind == first_row_ind:
        last_row_ind = rows_count

    return img_binary_without_rows, first_row_ind, last_row_ind


def removeVerticalAxes(image):
    rows_count = len(image)
    cols_count = len(image[0])
    img_binary_without_cols = image.copy()

    first_col_ind = 0
    last_col_ind = 0
    for col_ind in range(cols_count):
        counter = 0
        for row_ind in range(rows_count):
            if image[row_ind][col_ind] == BLACK_COLOR:
                counter += 1
        if counter >= LINE_THRESHOLD * rows_count:
            for row_ind in range(rows_count):
                img_binary_without_cols[row_ind][col_ind] = WHITE_COLOR
            last_col_ind = col_ind
            if first_col_ind == 0:
                first_col_ind = col_ind

    if last_col_ind == first_col_ind:
        last_col_ind = cols_count

    return img_binary_without_cols, first_col_ind, last_col_ind
