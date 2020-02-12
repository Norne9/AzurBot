import time
import random
import adb
from btn import Clickable
from log import log
import sys


BTN_LV = Clickable("lv", offset_y=-14, delay=10.0)
BTN_BOSS = Clickable("boss", delay=10.0)
BTN_SWITCH = Clickable("switch", x=481, y=327)

BTN_MENU_BATTLE = Clickable("menu_battle", x=507, y=150)
BTN_LEVEL_NAME = Clickable("level_name", delay=1.0)
BTN_GO1 = Clickable("go1", x=459, y=247, delay=1.0)
BTN_GO2 = Clickable("go2", x=525, y=291)
BTN_EVADE = Clickable("evade", x=505, y=224)
BTN_GOT_IT = Clickable("got_it", delay=1.0)
BTN_AUTO = Clickable("auto", x=376, y=56, delay=1.0)
BTN_BATTLE = Clickable("battle", x=529, y=306, delay=40.0)
BTN_CONFIRM = Clickable("confirm", x=511, y=321, delay=15.0)
BTN_COMMISSION = Clickable("commission", x=284, y=252)

useless_buttons = [
    BTN_MENU_BATTLE,
    BTN_GO1,
    BTN_GO2,
    BTN_EVADE,
    BTN_CONFIRM,
    BTN_COMMISSION,
    BTN_GOT_IT,
    BTN_LEVEL_NAME,
]


def do_nothing():
    x1, y1 = random.randint(174, 514) * 3, random.randint(57, 77) * 3
    x2, y2 = random.randint(174, 514) * 3, random.randint(57, 77) * 3
    adb.tap(x1, y1)
    time.sleep(1.0)
    adb.swipe(x1, y1, x2, y2)
    time.sleep(1.0)


def run():
    boss_clicks, ship_clicks = 0, 0
    is_nothing = False
    while True:
        screen = adb.screenshot()
        time.sleep(1.0)

        if BTN_BATTLE.on_screen(screen):
            is_nothing = False
            BTN_AUTO.click(screen)
            BTN_GOT_IT.click(screen)
            #  TODO: Check mood
            BTN_BATTLE.click(screen)
            continue

        for btn in useless_buttons:
            if btn.click(screen):
                boss_clicks, ship_clicks = 0, 0
                is_nothing = False
                break
        else:  # buttons not pressed
            if BTN_SWITCH.on_screen(screen):
                is_nothing = False
                if boss_clicks < 2 and BTN_BOSS.click(screen):
                    ship_clicks = 0
                    boss_clicks += 1
                elif ship_clicks < 4 and BTN_LV.click(screen):
                    ship_clicks += 1
                    boss_clicks = 0
                else:
                    ship_clicks = 0
                    do_nothing()
            else:  # nothing to do
                if not is_nothing:
                    log("Nothing to do")
                is_nothing = True
                do_nothing()


def shot():
    import cv2

    while True:
        cmd = input("Press enter... ")
        if len(cmd) > 0:
            break
        screen = adb.screenshot()
        cv2.imwrite(f"screenshots/{time.time()}.png", screen)


if __name__ == "__main__":
    log(adb.shell(["echo", '"Android connected!"']))
    if len(sys.argv) > 1:
        shot()
    else:
        run()
