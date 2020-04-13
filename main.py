import time
import adb
from log import log
import utils
from data import Btn
from game_actions import click_boss, click_enemy
from menu_actions import after_level, left_panel, start_lab
from game_fight import fight
from settings import Settings


MODE_STARTSWAP = False
MODE_EVENT = False
MODE_FIGHT = False
MODE_LAB = False
MODE_SWAP = 5
MODE_BOSS = 5


def begin_battle() -> bool:
    if not MODE_FIGHT:  # enable auto in auto mode
        for auto in [Btn.auto, Btn.auto_sub]:
            auto.click(utils.screenshot())  # enable auto

    # use heals
    if not Btn.zero_heals.on_screen(utils.screenshot()):
        utils.click(47, 255, 25, 25, 2.0)
        Btn.use_heal.click(utils.screenshot())
        Btn.cancel_heal.click(utils.screenshot())

    # Check mood
    screen = utils.screenshot()
    if Btn.mood.on_screen(screen):
        log("Ships in bad mood. Wait 60 min")
        utils.warn("mood", screen)
        time.sleep(60 * 60)
        log("Continue")
        return False

    Btn.battle.click(utils.screenshot())  # begin battle
    if Btn.battle.on_screen(utils.screenshot()):  # check if battle started
        return False

    if MODE_FIGHT:
        fight()
    else:
        log("Waiting 30s")
        time.sleep(30.0)
    return True


def run():
    after_level(MODE_LAB)  # free space & collect oil first

    clear_count, battle_count, go_clicks = 0, 0, 0
    nothing_start = 0.0
    is_nothing, clicked_boss = False, False
    while True:
        screen = utils.screenshot()

        if Btn.battle.on_screen(screen):
            is_nothing = False
            if not begin_battle():
                after_level(MODE_LAB)
            continue

        # click go
        if Btn.go1.click(screen):
            go_clicks += 1
            if go_clicks > 2:
                go_clicks = 0
                adb.back()
                after_level(MODE_LAB)
                continue
            utils.screenshot()
            if MODE_STARTSWAP:
                utils.click(495, 358, 40, 2, 1.0)
                utils.click(497, 334, 34, 7, 5.0)
            continue

        # level selection
        if Btn.daily.on_screen(screen):
            if MODE_EVENT:
                utils.click(587, 80, 31, 29, 5.0)
            else:
                if Btn.level_name.click(screen):  # level on screen, no need to search
                    continue
                for _ in range(15):  # go to right world
                    utils.click(605, 181, 9, 13, 0.25)
                time.sleep(6.0)  # wait for warnings disappear
                for _ in range(14):  # go back until level found
                    if Btn.level_name.click(utils.screenshot()):
                        break
                    utils.click(25, 178, 6, 17, 3.0)
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
                    battle_count = 0

        elif Btn.confirm.click(screen):  # after fight
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
                    after_level(MODE_LAB)
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


def collect():
    while True:
        utils.click_home()
        left_panel()
        utils.click_home()
        if MODE_LAB:
            start_lab()
            utils.click_home()
        log("Waiting 5 min...")
        time.sleep(5 * 60)


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
    settings = Settings()
    MODE_EVENT = settings.mode == "e"
    MODE_FIGHT, MODE_LAB = settings.fight, settings.start_lab
    MODE_SWAP, MODE_BOSS = settings.swap, settings.boss
    MODE_STARTSWAP = settings.start_swap

    log(adb.prepare())
    if settings.mode == "c":
        collect()
    elif settings.mode == "s":
        shot()
    else:
        run()
