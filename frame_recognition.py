from typing import List, Tuple, Union
from scipy import ndimage
import numpy as np
import cv2
from dataclasses import dataclass
from data import Img


@dataclass
class Frame:
    player: Union[Tuple[int, int], None]
    enemys: List[Tuple[int, int]]
    bombs: List[Tuple[int, int]]
    auto_button: bool
    air_button: bool
    torp_button: bool
    barrage_button: bool


def process_frame(screen: np.ndarray) -> Frame:
    auto_button, air_button, torp_button, barrage_button = get_buttons(screen)
    quad: np.ndarray = cv2.resize(screen, (screen.shape[1] // 4, screen.shape[0] // 4), interpolation=cv2.INTER_LINEAR)

    bombs = get_bomb_points(quad)
    player = get_ally_point(quad)
    enemys = get_enemy_points(quad, player)

    return Frame(player, enemys, bombs, auto_button, air_button, torp_button, barrage_button)


def show_frame(screen: np.ndarray, frame: Frame):
    if frame.player:
        cv2.drawMarker(screen, frame.player, (0, 255, 0), markerType=cv2.MARKER_STAR, markerSize=64)

    for point in frame.enemys:
        cv2.drawMarker(screen, point, (255, 0, 0), markerType=cv2.MARKER_STAR, markerSize=64)

    for point in frame.bombs:
        cv2.drawMarker(screen, point, (0, 0, 255), markerType=cv2.MARKER_STAR, markerSize=64)

    text = ""
    if frame.auto_button:
        text += "auto, "
    if frame.air_button:
        text += "air, "
    if frame.torp_button:
        text += "torp, "
    if frame.barrage_button:
        text += "barrage"

    cv2.putText(screen, text, (32, screen.shape[0] - 32), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255))

    cv2.imshow("debug", screen)
    cv2.waitKey(1)

    return screen


def get_buttons(screen: np.ndarray) -> Tuple[bool, bool, bool, bool]:
    # cut auto button and make it b/w
    auto_sector = screen[49:82, 23:103]
    auto_sector = (auto_sector[:, :, 0] == 255) & (auto_sector[:, :, 1] > 200) & (auto_sector[:, :, 2] > 200)
    auto_sector = auto_sector.astype(np.float)

    # Mean Squared Error for auto button
    err = np.sum((auto_sector - Img.auto_template) ** 2)
    err /= float(auto_sector.shape[0] * auto_sector.shape[1])
    auto_button = err < 0.1

    # cut barrage sector
    barrage_sector = screen[860:863, 1766:1782]
    err = (255.0 - barrage_sector).sum()
    barrage_button = err < 1.0

    # cut torp sector
    torp_sector = screen[860:863, 1547:1563]
    err = (255.0 - torp_sector).sum()
    torp_button = err < 1.0

    # cut air sector
    air_sector = screen[860:863, 1328:1344]
    err = (255.0 - air_sector).sum()
    air_button = err < 1.0

    return auto_button, air_button, torp_button, barrage_button


def get_enemy_points(quad: np.ndarray, player_point: Union[Tuple[int, int], None]) -> List[Tuple[int, int]]:
    if not player_point:  # if no player - np enemy
        return []

    # hide some spaces
    quad[14:22, 114:350] = 0
    # cut from player point
    x_offset = player_point[0] // 4 + 40
    quad = quad[:, x_offset:]  # -22

    res = 1.0 - cv2.matchTemplate(quad, Img.enemy_color, cv2.TM_SQDIFF_NORMED)
    res[res < 0.99] = 0

    label, count = ndimage.label(res)
    if count == 0:
        return []

    cords = ndimage.measurements.center_of_mass(res, label, range(1, count + 1))

    result = []
    for py, px in cords:
        if x_offset + px > 480 - 23:
            result.append((int((x_offset + px) * 4), int(py * 4)))
        else:
            result.append((int((x_offset + px) * 4), int(py * 4) + 170))

    return result


def get_ally_point(quad: np.ndarray) -> Union[Tuple[int, int], None]:
    res: np.ndarray = 1.0 - cv2.matchTemplate(quad[:, 40:240], Img.ally_color, cv2.TM_SQDIFF_NORMED)
    res[res < 0.99] = 0
    if res.sum() == 0:
        return None

    py, px = ndimage.measurements.center_of_mass(res)
    return int((px + 40) * 4) + 30, int(py * 4) + 110


def get_bomb_points(quad: np.ndarray) -> List[Tuple[int, int]]:
    res = cv2.matchTemplate(quad, Img.bomb_template, cv2.TM_SQDIFF_NORMED)
    res[res > 0.15] = 1.0
    res = 1.0 - res

    label, count = ndimage.label(res)
    if count == 0:
        return []

    cords = ndimage.measurements.center_of_mass(res, label, range(1, count + 1))

    result = []
    for py, px in cords:
        result.append((int(px * 4), int(py * 4) + 133))

    return result
