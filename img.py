import cv2
import numpy as np
from typing import List, Tuple


def find_zones(screen, template, threshold: float) -> List[Tuple[int, int, int, int]]:
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    locks = zip(*loc[::-1])
    result = []
    for pt in locks:  # Switch collumns and rows
        x, y = pt[0], pt[1]

        # check if its already exists
        in_result = False
        for (rx, ry, _, _) in result:
            diff = abs(x - rx) + abs(y - ry)
            if diff < 5:
                in_result = True
                break
        # if exists - not add
        if in_result:
            continue
        # add
        result.append((x, y, w, h))

    return result


def check_zone(screen: np.ndarray, template: np.ndarray, x: int, y: int) -> float:
    w, h = template.shape[::-1]
    y2, x2 = y + h, x + w
    cropped = screen[y:y2, x:x2]

    res = cv2.absdiff(template, cropped)
    percentage = res.sum() / 255.0 / res.size

    return 1.0 - percentage
