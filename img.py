import cv2
import numpy as np
from typing import List, Tuple, Union


def which(screen: np.ndarray, templates: List[np.ndarray]) -> int:
    best_val, best_i = -1, -1
    for i, tem in enumerate(templates):
        res = cv2.matchTemplate(screen, tem, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > best_val:
            best_val = max_val
            best_i = i
    return best_i


def find_zones(screen: np.ndarray, template: np.ndarray, threshold: float) -> List[Tuple[int, int, int, int]]:
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    locks = zip(*loc[::-1])
    result = []
    for pt in locks:  # Switch columns and rows
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


def find_best(screen: np.ndarray, template: np.ndarray, threshold: float = 0.95) -> Union[None, Tuple[int, int]]:
    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > threshold:
        return max_loc
    else:
        return None


def is_deadzone(x: int, y: int):
    return (x > 1750) or (x > 1000 and y > 880) or (x < 1100 and y < 245) or (x < 186)


def find_zones_color(
    screen: np.ndarray, color_bgr: Tuple[int, int, int], size: Tuple[int, int]
) -> List[Tuple[int, int]]:
    template = np.zeros((*size, 3), dtype=np.uint8)
    template[:, :] = color_bgr

    res = cv2.matchTemplate(screen, template, cv2.TM_SQDIFF_NORMED)
    loc = np.where(res < 0.01)
    locks = zip(*loc[::-1])

    result = []
    for pt in locks:  # Switch columns and rows
        x, y = pt[0] + 40, pt[1] + 35
        if is_deadzone(x, y):  # ignore stars & buttons
            continue
        # check if its already exists
        for rx, ry in result:
            diff = abs(x - rx) + abs(y - ry)
            if diff < 100:
                break
        else:  # add
            result.append((x, y))

    return result


def check_zone(screen: np.ndarray, template: np.ndarray, x: int, y: int) -> float:
    w, h = template.shape[::-1]
    y2, x2 = y + h, x + w
    cropped = screen[y:y2, x:x2]

    res = cv2.absdiff(template, cropped)
    percentage = res.sum() / 255.0 / res.size

    return 1.0 - percentage
