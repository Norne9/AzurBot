import frame_recognition
import adb
import utils
import time
import numpy as np
import cv2
from data import Btn


def fight():
    l_input = adb.LongInput()
    last_player = None
    while True:
        screen = adb.screenshot(False)
        frame = frame_recognition.process_frame(screen)

        if len(frame.enemys) > 0:  # only if we have enemys
            if frame.air_button:
                utils.click(428, 296, 25, 25, 0)
            if frame.torp_button:
                utils.click(500, 296, 25, 25, 0)

        if not frame.auto_button and check_end():
            l_input.stop()
            return

        target_auto = True  # auto mode need?
        if frame.barrage_button:
            target_auto = False

        if frame.auto_button != target_auto:  # change mode
            utils.click(3, 15, 73, 15, 0)
            continue

        if not target_auto or (last_player is None and frame.player is None):  # no control in auto mode
            continue

        if frame.player is None:
            player_x, player_y = last_player
        else:
            player_x, player_y = frame.player
            last_player = frame.player
        enemy_y = -1

        # finding best enemy
        if len(frame.bombs) > 0:  # bombs always best
            best_dst = 100000
            for x, y in frame.bombs:
                dst = abs(player_y - y)
                if dst < best_dst:
                    best_dst = dst
                    enemy_y = y
        elif len(frame.enemys) > 0:  # normal enemys - second target
            best_x = 100000
            for x, y in frame.enemys:
                if x < best_x:
                    best_x = x
                    enemy_y = y
        else:  # didn't found enemy, go to center
            enemy_y = 1080 // 2

        # move to enemy y
        move_y = (enemy_y - player_y) / 300.0
        move_y = np.clip(move_y, -1.0, 1.0)
        move_x = 0.25 if player_x < 450 or frame.player is None else -0.1

        if len(frame.bombs) > 0:
            move_y = (enemy_y - player_y) / 100.0
            move_x = 0.4

        move(l_input, move_x, move_y)


def move(l_input: adb.LongInput, x: float, y: float):
    x = 227 + x * 55
    y = 883 + y * 55
    l_input.tap(int(x), int(y))


def check_end() -> bool:
    screen = utils.screenshot()
    return Btn.confirm.on_screen(screen)