import time
import random
import adb
from btn import Clickable
from log import log
from typing import List, Tuple
import argparse
import cv2
import img

MODE_EVENT = False
MODE_SWAP = 5
MODE_BOSS = 2

BTN_QUESTION = Clickable([f"question{i}" for i in range(2)], offset_y=30, delay=5.0)
BTN_SWITCH = Clickable("switch")
BTN_MOOD = Clickable("mood")

BTN_LEVEL_NAME = Clickable("level_name", delay=2.0)
BTN_EVENT_NAME = Clickable("event_name", delay=2.0)

BTN_CLOSE = Clickable("close", x=590, y=26)
BTN_ITEM = Clickable("item", x=273, y=107)
BTN_MENU_BATTLE = Clickable("menu_battle", x=507, y=150)
BTN_CMODE = Clickable("cmode", x=518, y=294)
BTN_GO1 = Clickable("go1", x=459, y=247, delay=1.0)
BTN_GO2 = Clickable("go2", x=525, y=291, delay=1.0)
BTN_EVADE = Clickable("evade", x=505, y=224)
BTN_GOT_IT = Clickable("got_it", delay=1.0)
BTN_AUTO = Clickable("auto", x=376, y=56, delay=1.0)
BTN_AUTO_SUB = Clickable("auto_sub", x=377, y=84, delay=1.0)
BTN_BATTLE = Clickable("battle", x=529, y=306, delay=40.0)
BTN_CONFIRM = Clickable("confirm", x=511, y=321, delay=6.0)
BTN_LOCK_CONFIRM = Clickable("lock_confirm", x=360, y=252)
BTN_LOSE_CONFIRM = Clickable("lose_confirm", x=286, y=258)
BTN_LOSE_CLOSE = Clickable("lose_close", x=298, y=305)
BTN_COMMISSION = Clickable("commission", x=284, y=252)
BTN_RECONNECT = Clickable("reconnect", x=360, y=252)
BTN_DOWNLOAD = Clickable("download", x=364, y=242)
BTN_UPDATE = Clickable("update", x=284, y=251)
BTN_RETREAT = Clickable("retreat", x=380, y=330)

BTN_SORT = Clickable("sort", x=555, y=7)
BTN_SORT_CONFIRM = Clickable("sort_confirm", x=369, y=314)
BTN_ENHANCEABLE = Clickable("enhanceable", x=380, y=270)
BTN_ENHANCE_CONFIRM = Clickable("enhance_confirm", x=447, y=262)
BTN_ENHANCE_BREAK = Clickable("enhance_break", x=367, y=277)
BTN_ENHANCE = Clickable(["enhance_button1", "enhance_button2"], delay=1.0)

BTN_COMMISSION_COMPLETED = Clickable("commission_completed", x=192, y=136, delay=3.0)
BTN_COMMISSION_S = Clickable("commission_s", delay=3.0)
BTN_COMMISSION_GO = Clickable("commission_go", x=213, y=134, delay=2.0)
BTN_COMMISSION_0 = Clickable("commission_0", x=541, y=10)
BTN_COMMISSION_NEW = Clickable("commission_new", delay=2.0)
BTN_COMMISSION_RECOMMEND = Clickable("commission_recommend", delay=2.0)
BTN_COMMISSION_READY = Clickable("commission_ready", delay=2.0)
BTN_COMMISSION_CONFIRM = Clickable("commission_confirm", x=361, y=257, delay=6.0)
BTN_COMMISSION_COST = Clickable("commission_cost", x=558, y=147)
BTN_COMMISSION_OIL = Clickable("commission_oil")

IMG_ARROW = cv2.imread(f"images/arrow.png", cv2.IMREAD_GRAYSCALE)
IMG_BOSS = cv2.imread(f"images/boss.png", cv2.IMREAD_GRAYSCALE)

useless_buttons = [
    BTN_ITEM,
    BTN_RECONNECT,
    BTN_DOWNLOAD,
    BTN_CLOSE,
    BTN_MENU_BATTLE,
    # BTN_CMODE,
    BTN_GO1,
    BTN_GO2,
    BTN_LOCK_CONFIRM,
    BTN_LOSE_CONFIRM,
    BTN_LOSE_CLOSE,
    BTN_EVADE,
    BTN_GOT_IT,
]


def screenshot():
    screen = adb.screenshot()
    for btn in useless_buttons:
        if btn.click(screen):
            return screenshot()
    return screen


swipes = [
    lambda: None,
    lambda: adb.swipe(400, 400, 1720, 880),
    lambda: adb.swipe(1720, 200, 200, 880),
    lambda: adb.swipe(1720, 880, 200, 200),
    lambda: adb.swipe(200, 880, 1720, 200),
]

find_funs = [
    lambda s: img.find_zones_color(s, (148, 235, 255), (2, 2)),  # 1-2 triangles
    lambda s: img.find_zones_color(s, (132, 134, 255), (2, 2)),  # 3 triangles
]


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


# TODO: Refactor 'tap(randint, randint); sleep()' to 'click(x, y, w, h, delay)'
def after_level():
    log("Collecting oil")
    click_home()  # go to main menu
    click_home()

    screen = adb.screenshot()
    if not BTN_MENU_BATTLE.on_screen(screen):  # check if we in main menu
        cv2.imwrite(f"warn_screens/menu_{time.time()}.png", screen)
        log("Something went wrong")
        click_home()
        return

    adb.tap(random.randint(9, 29), random.randint(222, 242))  # open left panel
    time.sleep(3.0)
    adb.tap(random.randint(210, 300), random.randint(99, 117))  # tap can
    time.sleep(3.0)
    adb.tap(random.randint(582, 672), random.randint(99, 117))  # tap money
    time.sleep(3.0)

    send_commission()
    log("Commissions done")
    click_home()

    log("Removing trash")
    screen = adb.screenshot()
    if not BTN_MENU_BATTLE.on_screen(screen):  # check if we in main menu
        cv2.imwrite(f"warn_screens/menu_{time.time()}.png", screen)
        log("Something went wrong")
        click_home()
        return

    adb.tap(random.randint(303, 453), random.randint(1008, 1035))  # open dock
    time.sleep(3.0)

    BTN_SORT.click(screenshot())
    if screenshot()[275, 379] > 130:
        click(384, 260, 57, 14, 1.0)
    BTN_SORT_CONFIRM.click(screenshot())

    adb.tap(random.randint(189, 297), random.randint(195, 342))  # click first ship
    time.sleep(3.0)

    no_enhance = 0
    while no_enhance < 4:
        # click enhance
        if BTN_ENHANCE.click(screenshot()):
            adb.tap(random.randint(1470, 1602), random.randint(909, 933))  # press fill button
            time.sleep(0.5)
            adb.tap(random.randint(1725, 1857), random.randint(909, 933))  # press enhance button
            time.sleep(1.0)

            if BTN_ENHANCE_CONFIRM.click(screenshot()):  # press confirm
                no_enhance = 0
                if BTN_ENHANCE_BREAK.click(screenshot()):  # press disassemble
                    adb.tap(random.randint(1395, 1623), random.randint(807, 942))  # tap to continue
                    time.sleep(2.0)
                else:  # something went wrong
                    log("No break button!")
                    adb.back()
            else:
                no_enhance += 1
        else:
            no_enhance += 1
            log("No enhance button!")

        adb.swipe(
            random.randint(900, 966), random.randint(501, 558), random.randint(210, 276), random.randint(501, 558)
        )
        time.sleep(1.0)

    log("Done!")
    click_home()  # go to main menu


def send_one_commission(zero_cost: bool, oil_only: bool, total_try: int):
    try_count = 0
    while try_count < total_try and BTN_COMMISSION_NEW.click(screenshot()):
        if zero_cost and not BTN_COMMISSION_COST.on_screen(screenshot()):
            pass
        elif not oil_only or BTN_COMMISSION_OIL.on_screen(screenshot()):
            BTN_COMMISSION_RECOMMEND.click(screenshot())
            BTN_COMMISSION_READY.click(screenshot())
            BTN_COMMISSION_CONFIRM.click(screenshot())
        click(63, 327, 18, 25, 1.0)
        if BTN_COMMISSION_0.on_screen(screenshot()):
            log("0 fleets")
            return
        try_count += 1


def send_commission():
    if BTN_COMMISSION_COMPLETED.click(screenshot()):
        log("Completing commission")
        while BTN_COMMISSION_S.click(screenshot()):
            BTN_ITEM.click(screenshot())

    if BTN_COMMISSION_GO.click(screenshot()):
        if BTN_COMMISSION_0.on_screen(screenshot()):
            log("0 fleets")
            return
    else:
        return

    log("Starting urgent commissions oil")
    click(11, 114, 28, 25, 3.0)
    send_one_commission(False, True, 5)

    log("Starting daily commissions oil")
    click(12, 63, 30, 30, 3.0)
    send_one_commission(True, True, 5)

    log("Starting urgent commissions")
    click(11, 114, 28, 25, 3.0)
    send_one_commission(False, False, 5)

    log("Starting daily commissions")
    click(12, 63, 30, 30, 3.0)
    send_one_commission(True, False, 5)


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
        screen = screenshot()
        boss_point = img.find_best(screen, IMG_BOSS, 0.94)

        if boss_point is not None:  # boss on screen
            x, y = boss_point
            for _ in range(2):  # 2 click try's
                log(f"Tap boss [{x}, {y}]. Waiting 7.0s")
                click(x, y, 18, 18, 7.0)
                if not BTN_SWITCH.on_screen(screenshot()):  # success if switch disappeared
                    return "boss"

            # failed
            log(f"Searching ships near boss ")
            ships = []
            screen = adb.screenshot(False)
            for fun in find_funs:
                ships.extend(fun(screen))
            sort_near(ships, (x * 3, y * 3))  # ships near boss

            for sx, sy in ships:
                for _ in range(2):  # 2 click try's
                    log(f"Tap ship [{sx}, {sy}]. Waiting 7.0s")
                    adb.tap(sx + random.randint(0, 50), sy + random.randint(0, 50))
                    time.sleep(7.0)
                    if not BTN_SWITCH.on_screen(screenshot()):  # success if switch disappeared
                        return "ship"

    return "none"


def click_enemy() -> bool:
    log("Searching ships")
    for fun in find_funs:
        for sw in swipes:
            sw()  # swipe in some direction
            time.sleep(1.0)
            click_question()
            screen = screenshot()  # click buttons
            ships = fun(adb.screenshot(False))  # find triangles

            player_point = img.find_best(screen, IMG_ARROW, 0.95)  # if we find player go near player
            if player_point is not None:
                px, py = player_point
                sort_near(ships, (px * 3, (py + 70) * 3))  # player 70 pixels bellow arrow

            for x, y in ships:
                for _ in range(2):  # 2 click try's
                    log(f"Tap ship [{x}, {y}]. Waiting 7.0s")
                    adb.tap(x + random.randint(0, 50), y + random.randint(0, 50))
                    time.sleep(7.0)
                    if not BTN_SWITCH.on_screen(screenshot()):  # success if switch disappeared
                        return True
    return False


def click_question():
    for _ in range(3):
        if not BTN_QUESTION.click(screenshot()):
            break


def begin_battle():
    for auto in [BTN_AUTO, BTN_AUTO_SUB]:
        auto.click(screenshot())  # enable auto

    #  Check mood
    screen = screenshot()
    if BTN_MOOD.on_screen(screen):
        log("Ships in bad mood. Wait 60 min")
        cv2.imwrite(f"warn_screens/mood_{time.time()}.png", screen)
        click_home()  # go to main menu
        time.sleep(60 * 60)
        log("Continue")
        return

    BTN_BATTLE.click(screenshot())  # begin battle


def restart_game():
    log("Closing game")
    adb.stop_game()
    time.sleep(10.0)
    log("Starting game")
    adb.start_game()
    time.sleep(20.0)


def run():
    after_level()  # free space & collect oil first

    clear_count, battle_count, battle_clicks, = 0, 0, 0
    nothing_start = 0.0
    is_nothing, clicked_boss = False, False
    while True:
        screen = screenshot()
        time.sleep(1.0)

        if BTN_BATTLE.on_screen(screen):
            is_nothing = False
            battle_clicks += 1
            if battle_clicks > 3:  # battle don't work, collect oil
                battle_clicks = 0
                after_level()
                continue
            begin_battle()
            continue

        # level selection
        if BTN_LEVEL_NAME.on_screen(screen):
            if MODE_EVENT:
                click(587, 80, 31, 29, 5.0)
            else:
                BTN_LEVEL_NAME.click(screen)
            continue
        elif MODE_EVENT and BTN_EVENT_NAME.click(screen):
            continue

        # on map
        if BTN_SWITCH.on_screen(screen):
            is_nothing, clicked_boss = False, False
            state = "none"

            if battle_count >= MODE_BOSS:
                state = click_boss()
                if state == "boss":
                    clicked_boss = True

            if state == "none":
                if not click_enemy():  # try click ships
                    log("Ships not found")
                    BTN_RETREAT.click(screenshot())
                    battle_count, battle_clicks = 0, 0

        elif BTN_CONFIRM.click(screen):  # after fight
            battle_clicks = 0
            is_nothing = False
            BTN_COMMISSION.click(screenshot())
            screen = screenshot()
            if BTN_SWITCH.on_screen(screen):  # fight finished
                battle_count += 1
                if battle_count % MODE_SWAP == 0:
                    BTN_SWITCH.click(screen)
            elif clicked_boss:  # level finished
                log("Boss killed")
                clear_count += 1
                battle_count = 0
                if clear_count % 2 == 0:
                    after_level()
        elif BTN_UPDATE.on_screen(screen):  # game requested update
            is_nothing = False
            restart_game()
        else:  # nothing to do
            if not is_nothing:
                nothing_start = time.time()
                is_nothing = True
                log("Nothing to do")
            elif time.time() - nothing_start > 60 * 5:
                cv2.imwrite(f"warn_screens/nothing_{time.time()}.png", screen)
                log("Nothing to do for 5 minutes")
                is_nothing = False
                restart_game()
            do_nothing()


def shot():
    while True:
        cmd = input("Press enter... ")
        if cmd == "c":
            screen = adb.screenshot(False)
        elif len(cmd) > 0:
            break
        else:
            screen = adb.screenshot()
        cv2.imwrite(f"screenshots/{time.time()}.png", screen)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bot for farming in Azur Lane")
    parser.add_argument("--event", action="store_true", help="Farm event")
    parser.add_argument("-s", action="store_true", help="Make screenshots")
    parser.add_argument("--swap", action="store", type=int, default=MODE_SWAP, help="Battle count before swap")
    parser.add_argument("--boss", action="store", type=int, default=MODE_BOSS, help="Battle count before boss checking")
    args = parser.parse_args()
    MODE_EVENT, MODE_SWAP, MODE_BOSS = args.event, args.swap, args.boss

    log(adb.shell(["echo", '"Android connected!"']))
    if args.s:
        shot()
    else:
        run()
