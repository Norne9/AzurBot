import frame_recognition
import adb
import utils
import time
import numpy as np
from log import log
from data import Btn


def fight():
    start_time, last_enemy_time, sub_used = -1.0, -1.0, False
    last_player = None
    while True:
        screen = adb.screenshot(False)
        frame = frame_recognition.process_frame(screen)

        # start time counting
        if frame.auto_button and start_time < 0:
            start_time = time.time()
            last_enemy_time = start_time

        # level finished
        if not frame.auto_button and check_end():
            adb.release()
            log(f"Level finished in {time.time() - start_time:.2f}s")
            return

        # auto mode need?
        target_auto = True
        if frame.barrage_button:
            target_auto = False

        # change mode
        if frame.auto_button != target_auto:
            utils.click(3, 15, 73, 15, 0)
            adb.release()
            continue

        # no control in auto mode
        if not target_auto or (last_player is None and frame.player is None):
            continue

        # launch submarine 5 seconds after start
        # if time.time() - start_time > 5.0 and not sub_used:
        #    sub_used = True
        #    utils.click(354, 295, 27, 25, 0)
        #    adb.release()

        # pressing buttons
        # only if we have enemys or don't have them for 5 seconds
        if len(frame.enemys) > 0 or time.time() - last_enemy_time > 5.0:
            last_enemy_time = time.time()
            if frame.air_button:
                utils.click(428, 296, 25, 25, 0)
                adb.release()

        # player searching
        if frame.player is None:
            player_x, player_y = last_player
        else:
            player_x, player_y = frame.player
            last_player = frame.player
        enemy_y = -1

        # pressing torpedoes
        if frame.torp_button and player_x > 650:
            utils.click(500, 296, 25, 25, 0)
            adb.release()

        # finding best enemy
        best_x = 100000
        if len(frame.bombs) > 0:  # bombs always best
            best_dst = 100000
            for x, y in frame.bombs:
                dst = abs(player_y - y)
                if dst < best_dst:
                    best_dst = dst
                    enemy_y = y
        elif len(frame.enemys) > 0:  # normal enemys - second target
            for x, y in frame.enemys:
                if x < best_x:
                    best_x = x
                    enemy_y = y
        else:  # didn't found enemy, go to center
            enemy_y = 1080 // 2

        # move to enemy y
        move_y = (enemy_y - player_y) / 300.0
        move_x = 0.4 if player_x < 400 or frame.player is None else -0.2

        # move forward if no enemys
        if len(frame.enemys) == 0 or best_x > 1500:
            move_x = 0.4 if player_x < 850 or frame.player is None else -0.2

        # move faster if we have bomb ships or torpedoes ready
        if len(frame.bombs) > 0 or frame.torp_button:
            move_y = (enemy_y - player_y) / 100.0
            move_x = 0.6

        # make a move
        move_y = float(np.clip(move_y, -1.0, 1.0))
        move(move_x, move_y)


def move(x: float, y: float):
    x = 227 + x * 55
    y = 883 + y * 55
    adb.hold(x, y)


def check_end() -> bool:
    screen = utils.screenshot()
    return Btn.confirm.on_screen(screen)
