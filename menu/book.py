from data import Btn, Img
import utils
import adb
import random
import cv2
import numpy as np
from log import log
from typing import List, Tuple


def learn_book():
    utils.click(3, 70, 11, 24, 2.0)  # open left panel
    utils.click(200, 207, 41, 10, 1.0)
    log("Completing books")
    while Btn.book_confirm.click(adb.screenshot()):
        points = find_green()
        if len(points) == 0:
            log("ERROR: books not found")
            break
        x, y = random.choice(points)
        utils.click(x, y, 10, 10, 2.0)
        utils.click(558, 302, 40, 14, 2.0)
        if Btn.book_confirm.click(adb.screenshot()):
            log("Learning started")
    log("Books done")


def find_green() -> List[Tuple[int, int]]:
    zone = adb.screenshot(False)[405:783, 290:1631]

    res = cv2.matchTemplate(zone, Img.book_color, cv2.TM_SQDIFF_NORMED)
    loc = np.where(res < 0.01)
    locks = zip(*loc[::-1])

    points = []
    for x, y in locks:
        for x1, y1 in points:
            if abs(x - x1) < 130 and abs(y - y1) < 220:
                break
        else:
            points.append((int(x), int(y)))
    points = [((x + 290) // 3, (y + 445) // 3) for x, y in points]

    return points
