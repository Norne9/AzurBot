import adb
import random
import time
import cv2
from data import Btn
from log import log

useless_buttons = [
    Btn.item,
    Btn.reconnect,
    Btn.download,
    Btn.close,
    Btn.menu_battle,
    Btn.go1,
    Btn.go2,
    Btn.lock_confirm,
    Btn.lose_confirm,
    Btn.lose_close,
    Btn.evade,
    Btn.got_it,
]


def screenshot():
    screen = adb.screenshot()
    for btn in useless_buttons:
        if btn.click(screen):
            return screenshot()
    return screen


def do_nothing():
    x1, y1 = random.randint(174, 514) * 3, random.randint(57, 77) * 3
    x2, y2 = random.randint(174, 514) * 3, random.randint(57, 77) * 3
    adb.tap(x1, y1)
    time.sleep(1.0)
    adb.swipe(x1, y1, x2, y2)
    time.sleep(1.0)


def click(x: int, y: int, w: int, h: int, delay: float):
    x, y = random.randint(x * 3, x * 3 + w * 3), random.randint(y * 3, y * 3 + h * 3)
    adb.tap(x, y)
    time.sleep(delay)


def click_home():
    click(608, 9, 13, 15, 3.0)


def warn(name: str, screen):
    cv2.imwrite(f"warn_screens/{name}_{time.time()}.png", screen)


def restart_game():
    log("Closing game")
    adb.stop_game()
    time.sleep(10.0)
    log("Starting game")
    adb.start_game()
    time.sleep(20.0)