import img
import adb
import time
import utils
import random
from data import Btn, Img
from typing import List, Tuple
from log import log

find_funs = [
    lambda s: img.find_zones_color(s, (156, 239, 255), (6, 6)),  # 1-2 triangles
    lambda s: img.find_zones_color(s, (140, 138, 255), (6, 6)),  # 3 triangles
]
swipes = [
    lambda: None,
    lambda: adb.swipe(400, 400, 1720, 880),
    lambda: adb.swipe(1720, 200, 200, 880),
    lambda: adb.swipe(1720, 880, 200, 200),
    lambda: adb.swipe(200, 880, 1720, 200),
]


def sort_near(ships: List[Tuple[int, int]], point: Tuple[int, int]):
    px, py = point

    def get_dist(pos: Tuple[int, int]) -> float:
        x, y = pos
        dx, dy = x - px, y - py
        return dx * dx + dy * dy

    ships.sort(key=get_dist)


def click_boss() -> str:
    log(f"Searching boss")
    for sw in swipes:
        sw()  # swipe in some direction
        time.sleep(1.0)
        click_question()
        screen = utils.screenshot()
        boss_point = img.find_best(screen, Img.boss, 0.94)

        if boss_point is not None:  # boss on screen
            x, y = boss_point
            if img.is_deadzone(x * 3, y * 3):
                continue

            for _ in range(2):  # 2 click try's
                log(f"Tap boss [{x}, {y}]")
                utils.click(x, y, 18, 18, 0)
                if detect_info():  # don't try second click
                    break
                if wait_for_battle(8.0):  # success if switch disappeared
                    return "boss"

            # failed
            log(f"Searching ships near boss")
            ships = []
            screen = adb.screenshot(False)
            for fun in find_funs:
                ships.extend(fun(screen))
            sort_near(ships, (x * 3, y * 3))  # ships near boss

            for sx, sy in ships:
                for _ in range(2):  # 2 click try's
                    log(f"Tap ship [{sx}, {sy}]")
                    adb.tap(sx + random.randint(0, 50), sy + random.randint(0, 50))
                    if detect_info():  # don't try second click
                        break
                    if wait_for_battle(8.0):  # success if switch disappeared
                        return "ship"

    return "none"


def click_enemy() -> bool:
    log("Searching ships")
    for fun in find_funs:
        for sw in swipes:
            sw()  # swipe in some direction
            time.sleep(1.0)
            click_question()
            screen = utils.screenshot()  # click buttons
            ships = fun(adb.screenshot(False))  # find triangles

            player_point = img.find_best(screen, Img.arrow, 0.95)  # if we find player go near player
            if player_point is not None:
                px, py = player_point
                sort_near(ships, (px * 3, (py + 70) * 3))  # player 70 pixels bellow arrow

            for x, y in ships:
                for _ in range(2):  # 2 click try's
                    log(f"Tap ship [{x}, {y}]")
                    adb.tap(x + random.randint(0, 50), y + random.randint(0, 50))
                    if detect_info():  # don't try second click
                        break
                    if wait_for_battle(8.0):  # success if switch disappeared
                        return True
    return False


def click_question():
    for _ in range(3):
        if not Btn.question.click(utils.screenshot()):
            break
        if detect_info():
            continue
        time.sleep(7.0)


def detect_info() -> bool:
    time.sleep(1.0)
    has_unable = False

    zone = utils.screenshot()[143 : 143 + 40, 192 : 192 + 60]
    while Btn.unable_info.on_screen(zone):
        time.sleep(0.5)
        zone = utils.screenshot()[143 : 143 + 40, 192 : 192 + 60]
        has_unable = True
    return has_unable


def wait_for_battle(seconds: float) -> bool:
    log(f"Waiting max {seconds}s")
    end_time = time.time() + seconds
    while end_time > time.time():
        time.sleep(0.5)
        if not Btn.switch.on_screen(utils.screenshot()):
            return True
    return False
