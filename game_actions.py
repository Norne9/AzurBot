import img
import adb
import time
import utils
import enemy_finder
from data import Btn, Img
from typing import List, Tuple
from log import log

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
    for sw in swipes * 2:
        sw()  # swipe in some direction
        time.sleep(1.0)
        click_question()
        screen = utils.screenshot()
        boss_point = img.find_best(screen, Img.boss, 0.8)

        if boss_point is not None:  # boss on screen
            x, y = boss_point
            for _ in range(2):  # 2 click try's
                point = enemy_finder.get_safe_point((x + 20) * 3, (y + 7) * 3)
                if point is None:
                    continue
                bx, by = point

                log(f"Tap boss [{bx}, {by}]")
                adb.tap(bx, by)
                if detect_info():  # don't try second click
                    break
                if wait_for_battle(8.0):  # success if switch disappeared
                    return "boss"

            # failed
            log(f"Searching ships near boss")
            ships = []
            screen = adb.screenshot(False)
            for yellow in [True, False]:
                ships.extend(enemy_finder.find_triangles(screen, yellow))
            sort_near(ships, (x * 3, y * 3))  # ships near boss

            if tap_ships(ships):
                return "ship"

    return "none"


def click_enemy() -> bool:
    log("Searching ships")
    for yellow in [True, True, False, False]:
        for sw in swipes:
            sw()  # swipe in some direction
            time.sleep(1.0)
            click_question()
            screen = utils.screenshot()  # click buttons
            ships = enemy_finder.find_triangles(adb.screenshot(False), yellow)

            player_point = img.find_best(screen, Img.arrow, 0.95)  # if we find player go near player
            if player_point is not None:
                px, py = player_point
                sort_near(ships, (px * 3, (py + 70) * 3))  # player 70 pixels bellow arrow

            if tap_ships(ships):
                return True
    return False


def tap_ships(ships: List[Tuple[int, int]]) -> bool:
    for x, y in ships:
        for _ in range(2):  # 2 click try's
            # select random place to tap
            point = enemy_finder.get_safe_point(x, y)
            if point is None:
                break

            # tap
            x, y = point
            log(f"Tap ship [{x}, {y}]")
            adb.tap(x, y)

            # wait
            if detect_info():  # don't try second click
                break
            if wait_for_battle(8.0):  # success if switch disappeared
                return True


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
