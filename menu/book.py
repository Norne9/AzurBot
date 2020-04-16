from data import Btn, Img
import img
import utils
import adb
import random
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
    points = img.find_zones(zone, Img.book_color, 0.9)
    filtered_points = []
    for x, y, _, _ in points:
        exist = False
        for x1, y1 in filtered_points:
            if abs(x - x1) < 130:
                exist = True
                break
            if abs(y - y1) < 220:
                exist = True
                break
        if not exist:
            filtered_points.append((x, y))

    return [((x + 290) // 3, (y + 445) // 3) for x, y in filtered_points]
