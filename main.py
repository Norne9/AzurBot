import time
import random
import adb
from btn import Clickable
from log import log
import sys


BTN_LV = Clickable("lv", offset_y=-14, delay=10.0)
BTN_BOSS = Clickable("boss", delay=10.0)
BTN_SWITCH = Clickable("switch", x=481, y=327)
BTN_MOOD = Clickable("mood")

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

BTN_ENHANCE_CONFIRM = Clickable("enhance_confirm", x=447, y=262)
BTN_ENHANCE_BREAK = Clickable("enhance_break", x=367, y=277)


useless_buttons = [
    BTN_MENU_BATTLE,
    BTN_GO1,
    BTN_GO2,
    BTN_EVADE,
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


# TODO: Refactor 'tap(randint, randint); sleep()' to 'click(x, y, w, h, delay)'
def after_level():
    log("Collecting oil")
    adb.back()  # go to main menu
    time.sleep(5.0)

    screen = adb.screenshot()
    if not BTN_MENU_BATTLE.on_screen(screen):  # check if we in main menu
        log("Something went wrong")
        return

    adb.tap(random.randint(9, 29), random.randint(222, 242))  # open left panel
    time.sleep(3.0)
    adb.tap(random.randint(210, 300), random.randint(99, 117))  # tap can
    time.sleep(3.0)
    adb.tap(random.randint(582, 672), random.randint(99, 117))  # tap money
    time.sleep(3.0)

    log("Removing trash")
    adb.back()  # close left panel
    time.sleep(3.0)

    screen = adb.screenshot()
    if not BTN_MENU_BATTLE.on_screen(screen):  # check if we in main menu
        log("Something went wrong")
        return

    adb.tap(random.randint(303, 453), random.randint(1008, 1035))  # open dock
    time.sleep(3.0)
    adb.tap(random.randint(189, 297), random.randint(195, 342))  # click first ship
    time.sleep(3.0)
    adb.tap(random.randint(32, 114), random.randint(195, 243))  # open enhance screen
    time.sleep(3.0)
    for _ in range(6):
        adb.tap(random.randint(1470, 1602), random.randint(909, 933))  # press fill button
        time.sleep(2.0)
        adb.tap(random.randint(1725, 1857), random.randint(909, 933))  # press enhance button
        time.sleep(2.0)

        screen = adb.screenshot()
        if BTN_ENHANCE_CONFIRM.click(screen):  # press confirm
            screen = adb.screenshot()
            if BTN_ENHANCE_BREAK.click(screen):  # press disassemble
                adb.tap(random.randint(1395, 1623), random.randint(807, 942))  # tap to continue
                time.sleep(4.0)

        adb.swipe(
            random.randint(900, 966), random.randint(501, 558), random.randint(210, 276), random.randint(501, 558)
        )
        time.sleep(2.0)

    log("Done!")
    time.sleep(6.0)
    adb.back()  # go back to menu
    time.sleep(2.0)
    adb.back()  # go back to menu
    time.sleep(6.0)


def begin_battle():
    screen = adb.screenshot()
    BTN_AUTO.click(screen)  # enable auto

    screen = adb.screenshot()
    BTN_GOT_IT.click(screen)  # got it after auto

    #  Check mood
    screen = adb.screenshot()
    if BTN_MOOD.on_screen(screen):
        log("Ships in bad mood. Wait 60min")
        for _ in range(3):
            adb.back()
            time.sleep(2.0)
        time.sleep(60 * 60)
        log("Continue")

    screen = adb.screenshot()
    BTN_BATTLE.click(screen)  # begin battle


def run():
    boss_clicks, ship_clicks, clear_count = 0, 0, 0
    is_nothing = False
    while True:
        screen = adb.screenshot()
        time.sleep(1.0)

        if BTN_BATTLE.on_screen(screen):
            is_nothing = False
            begin_battle()
            continue

        for btn in useless_buttons:
            if btn.click(screen):
                boss_clicks, ship_clicks = 0, 0
                is_nothing = False
                break
        else:  # buttons not pressed
            # on map
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
            elif BTN_CONFIRM.click(screen):  # after fight
                screen = adb.screenshot()
                BTN_COMMISSION.click(screen)
                screen = adb.screenshot()
                if BTN_LEVEL_NAME.on_screen(screen):  # level finished
                    clear_count += 1
                    if clear_count % 3 == 0:
                        after_level()
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
