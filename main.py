import time
import adb
from log import log
import argparse
import utils
from data import Btn
from game_actions import click_boss, click_enemy
from menu_actions import after_level


MODE_EVENT = False
MODE_SWAP = 5
MODE_BOSS = 5


def begin_battle():
    for auto in [Btn.auto, Btn.auto_sub]:
        auto.click(utils.screenshot())  # enable auto

    #  Check mood
    screen = utils.screenshot()
    if Btn.mood.on_screen(screen):
        log("Ships in bad mood. Wait 60 min")
        utils.warn("mood", screen)
        utils.click_home()  # go to main menu
        time.sleep(60 * 60)
        log("Continue")
        return

    Btn.battle.click(utils.screenshot())  # begin battle


def run():
    after_level()  # free space & collect oil first

    clear_count, battle_count, battle_clicks, go_clicks = 0, 0, 0, 0
    nothing_start = 0.0
    is_nothing, clicked_boss = False, False
    while True:
        screen = utils.screenshot()

        if Btn.battle.on_screen(screen):
            is_nothing = False
            battle_clicks += 1
            if battle_clicks > 3:  # battle don't work, collect oil
                battle_clicks = 0
                after_level()
                continue
            begin_battle()
            continue

        # click go
        if Btn.go1.click(screen):
            go_clicks += 1
            if go_clicks > 2:
                go_clicks = 0
                adb.back()
                after_level()
            continue

        # level selection
        if Btn.level_name.on_screen(screen):
            if MODE_EVENT:
                utils.click(587, 80, 31, 29, 5.0)
            else:
                Btn.level_name.click(screen)
            continue
        elif MODE_EVENT and Btn.event_name.click(screen):
            continue

        # on map
        if Btn.switch.on_screen(screen):
            go_clicks = 0
            is_nothing, clicked_boss = False, False
            state = "none"

            if battle_count >= MODE_BOSS:
                state = click_boss()
                if state == "boss":
                    clicked_boss = True

            if state == "none":
                if not click_enemy():  # try click ships
                    log("Ships not found")
                    Btn.retreat.click(utils.screenshot())
                    battle_count, battle_clicks = 0, 0

        elif Btn.confirm.click(screen):  # after fight
            battle_clicks = 0
            is_nothing = False
            Btn.commission.click(utils.screenshot())
            screen = utils.screenshot()
            if Btn.switch.on_screen(screen):  # fight finished
                battle_count += 1
                if battle_count % MODE_SWAP == 0:
                    Btn.switch.click(screen)
            elif clicked_boss:  # level finished
                log("Boss killed")
                clear_count += 1
                battle_count = 0
                if clear_count % 2 == 0:
                    after_level()
        elif Btn.update.on_screen(screen):  # game requested update
            is_nothing = False
            utils.restart_game()
        else:  # nothing to do
            if not is_nothing:
                nothing_start = time.time()
                is_nothing = True
                log("Nothing to do")
            elif time.time() - nothing_start > 60 * 5:
                utils.warn("nothing", screen)
                log("Nothing to do for 5 minutes")
                is_nothing = False
                utils.restart_game()
            utils.do_nothing()


def shot():
    import cv2

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

    log(adb.prepare())
    if args.s:
        shot()
    else:
        run()
