import cv2
import numpy as np
import random
from typing import List, Tuple, Union
from data import Img


def find_triangles(screen: np.ndarray, yellow: bool) -> List[Tuple[int, int]]:
    screen = screen & np.uint8(0b11000000)

    if yellow:
        target_bgr1 = np.array([[[128, 192, 192]]], dtype=np.uint8)  # yellow
        target_bgr2 = np.array([[[192, 192, 192]]], dtype=np.uint8)  # white
    else:
        target_bgr1 = np.array([[[128, 128, 192]]], dtype=np.uint8)  # red
        target_bgr2 = np.array([[[64, 64, 192]]], dtype=np.uint8)  # red red

    screen1 = (screen - target_bgr1).sum(axis=2)
    screen2 = (screen - target_bgr2).sum(axis=2)

    screen = np.full((screen.shape[0], screen.shape[1]), 0)
    screen[(screen1 != 0) & (screen2 != 0)] = 255
    screen[Img.deadzone_image < 100] = 255
    screen = screen.astype(np.uint8)

    res1 = cv2.matchTemplate(screen, Img.triangle_template, cv2.TM_SQDIFF_NORMED)
    res2 = cv2.matchTemplate(screen, Img.triangle_big_template, cv2.TM_SQDIFF_NORMED)

    result = []

    # res2
    loc = np.where(res2 < 0.15)
    locks = zip(*loc[::-1])
    for x, y in locks:  # Switch columns and rows
        x, y = x + 100, y + 110
        # check if its already exists
        for rx, ry in result:
            diff = abs(x - rx) + abs(y - ry)
            if diff < 100:
                break
        else:  # add
            result.append((x, y))

    # res1
    loc = np.where(res1 < 0.15)
    locks = zip(*loc[::-1])
    for x, y in locks:  # Switch columns and rows
        x, y = x + 100, y + 110
        # check if its already exists
        for rx, ry in result:
            diff = abs(x - rx) + abs(y - ry)
            if diff < 100:
                break
        else:  # add
            result.append((x, y))

    return result


def get_safe_point(x: int, y: int) -> Union[None, Tuple[int, int]]:
    for _ in range(64):
        px, py = x + random.randint(-32, 32), y + random.randint(-32, 32)
        if px < 0 or py < 0 or px >= 1920 or py >= 1080:
            continue
        if Img.deadzone_image[py, px] > 100:  # white deadzone
            return px, py
    return None
