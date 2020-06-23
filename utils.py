import adb
import random
import time
import cv2
from data import Btn
from log import log, send_img

useless_buttons = [
    # Btn.item,
    Btn.close,
    Btn.menu_battle,
    # Btn.go1,
    Btn.go2,
    Btn.lose_close,
    Btn.evade,
    Btn.got_it,
    Btn.universal_confirm,
]


def screenshot():
    time.sleep(0.5)
    screen = adb.screenshot()

    if Btn.item.click(screen):  # send what we get to discord
        cv2.imwrite("test.png", screen[140:215, 160:480])
        send_img("test.png")
        return screenshot()

    if Btn.item2.click(screen):  # send what we get to discord
        cv2.imwrite("test.png", screen[110:250, 160:480])
        send_img("test.png")
        return screenshot()

    for btn in useless_buttons:
        if btn.click(screen):
            return screenshot()
    return screen


def screen_face():
    return adb.screenshot()[70:93, 11:51]


def do_nothing():
    x1, y1 = random.randint(174, 514) * 3, random.randint(57, 77) * 3
    adb.tap(x1, y1)
    time.sleep(1.0)

    # x2, y2 = random.randint(174, 514) * 3, random.randint(57, 77) * 3
    # adb.swipe(x1, y1, x2, y2)
    # time.sleep(1.0)


def click(x: int, y: int, w: int, h: int, delay: float):
    x, y = random.randint(x * 3, x * 3 + w * 3), random.randint(y * 3, y * 3 + h * 3)
    adb.tap(x, y)
    time.sleep(delay)


def click_home():
    log("Going home...")
    start_time = time.time()
    while True:
        adb.back()
        time.sleep(0.5)
        if Btn.menu_quit_cancel.click(adb.screenshot()):
            return
        if time.time() - start_time > 20.0:  # it's taking to long - restart game
            restart_game()
            return


def warn(name: str, screen):
    cv2.imwrite(f"warn_screens/{name}_{time.time()}.png", screen)


def restart_game():
    log("Closing game")
    adb.stop_game()
    time.sleep(2.0)
    log("Starting game")
    adb.start_game()
    time.sleep(8.0)

    start_time = time.time()
    while True:  # wait for game to start
        screen = screenshot()
        if Btn.archives.on_screen(screen):  # if daily on screen - done
            break
        if time.time() - start_time > 120.0:  # it's taking to long - try again
            restart_game()
            return
        do_nothing()
    click_home()  # go to main menu


def show(screen):
    cv2.imshow("screen", screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def scroll_down():
    adb.swipe(1100, 900, 1100, 130)
    time.sleep(1.0)
