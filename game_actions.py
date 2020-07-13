import img
import adb
import time
import utils
import enemy_finder
from data import Btn, Img
from typing import List, Tuple
from log import log


def double_swap():
    swap()
    swap()
    time.sleep(3.0)


swipes = [
    double_swap,
    lambda: adb.swipe(400, 400, 1720, 880),
    lambda: adb.swipe(1720, 200, 200, 880),
    lambda: adb.swipe(1720, 880, 200, 200),
    lambda: adb.swipe(200, 880, 1720, 200),
    lambda: adb.swipe(1720, 200, 1320, 600),
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

        boss_point = img.find_best(screen, Img.boss, 0.7)
        if boss_point is None:
            boss_point = img.find_best(screen, Img.boss_mini, 0.7)
            if boss_point is None:
                continue
            else:
                boss_point = boss_point[0] - 4, boss_point[1] - 6
        else:
            boss_point = boss_point[0] + 20, boss_point[1] + 7

        x, y = boss_point
        point = None
        for _ in range(2):  # 2 click try's
            point = enemy_finder.get_safe_point(x * 3, y * 3)
            if point is None:
                continue
            bx, by = point

            log(f"Tap boss [{bx}, {by}]")
            adb.tap(bx, by)
            if detect_info():  # don't try second click
                break
            if wait_for_battle(8.0):  # success if switch disappeared
                return "boss"

        if point is None:  # don't attack ships if boss not clickable
            continue

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
    for yellow in [True, False]:
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
            checked_tap(x, y)

            # wait
            if detect_info():  # don't try second click
                break
            if wait_for_battle(8.0):  # success if switch disappeared
                return True


def click_question(clicks_before: int = 0):
    screen = utils.screenshot()
    zones = img.find_zones(screen, Img.question0, 0.8)
    zones.extend(img.find_zones(screen, Img.question1, 0.8))
    for x, y, w, h in zones:
        x, y = x + w / 2, y + h / 2 + 30
        point = enemy_finder.get_safe_point(int(x) * 3, int(y) * 3)
        if point is None:
            continue
        x, y = point
        log(f"Click question [{x}, {y}]")
        adb.tap(x, y)
        if detect_info():
            continue

        time.sleep(7.0)
        if clicks_before < 4:
            click_question(clicks_before + 1)
        break


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


def swap():
    for _ in range(8):
        before = adb.screenshot()
        if not Btn.switch.on_screen(before):
            log("ERROR: Failed to switch, button not on screen")
            return
        before = utils.screen_face()  # get portrait
        utils.click(497, 334, 34, 7, 1.0)
        after = utils.screen_face()
        if img.mean_square(before, after) > 0.001:
            return
        time.sleep(1.5)
    log("ERROR: Failed to switch, more than 8 try's")


def swap_team(target_face, target_team):
    current_face = utils.screen_face()
    face_same = img.mean_square(target_face, current_face) < 0.001
    if target_team != face_same:
        swap()


def checked_tap(x, y):
    before = adb.screenshot()[58:101, 10:53]
    adb.tap(x, y)
    time.sleep(0.5)
    after = adb.screenshot()[58:101, 10:53]

    # if switch disappeared it's ok
    if not Btn.switch.on_screen(after):
        return
    # if ship icon changed -> change it back
    if img.mean_square(before, after) > 0.001:
        swap()
