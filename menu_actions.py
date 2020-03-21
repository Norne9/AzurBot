import adb
import time
import utils
import random
from data import Btn
from log import log


def after_level():
    log("Collecting oil")
    utils.click_home()  # go to main menu
    utils.click_home()

    screen = adb.screenshot()
    if not Btn.menu_battle.on_screen(screen):  # check if we in main menu
        utils.warn("menu", screen)
        log("Something went wrong")
        utils.click_home()
        return

    utils.click(3, 70, 11, 24, 3.0)  # open left panel
    screen = adb.screenshot()
    Btn.menu_can.click(screen)  # tap can
    Btn.menu_money.click(screen)  # tap money

    send_commission()
    log("Commissions done")
    utils.click_home()

    log("Removing trash")
    screen = adb.screenshot()
    if not Btn.menu_battle.on_screen(screen):  # check if we in main menu
        utils.warn("menu", screen)
        log("Something went wrong")
        utils.click_home()
        return

    utils.click(87, 332, 74, 24, 3.0)  # open dock

    Btn.sort.click(utils.screenshot())
    if utils.screenshot()[275, 379] > 130:
        utils.click(384, 260, 57, 14, 1.0)
    Btn.sort_confirm.click(utils.screenshot())

    utils.click(49, 53, 63, 56, 3.0)  # click first ship

    no_enhance = 0
    while no_enhance < 4:
        # click enhance
        if Btn.enhance.click(utils.screenshot()):
            utils.click(483, 302, 58, 19, 0.5)  # press fill button
            utils.click(567, 302, 58, 19, 2.0)  # press enhance button

            if Btn.enhance_confirm.click(utils.screenshot()):  # press confirm
                no_enhance = 0
                if Btn.enhance_break.click(utils.screenshot()):  # press disassemble
                    utils.click(434, 244, 164, 97, 2.0)  # tap to continue
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
    utils.click_home()  # go to main menu


def send_one_commission(zero_cost: bool, oil_only: bool, total_try: int):
    try_count = 0
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return
    while try_count < total_try and Btn.commission_new.click(utils.screenshot()):
        if zero_cost and not Btn.commission_cost.on_screen(utils.screenshot()):
            pass
        elif not oil_only or Btn.commission_oil.on_screen(utils.screenshot()):
            Btn.commission_recommend.click(utils.screenshot())
            Btn.commission_ready.click(utils.screenshot())
            Btn.commission_confirm.click(utils.screenshot())
        utils.click(63, 327, 18, 25, 1.0)
        if Btn.commission_0.on_screen(utils.screenshot()):
            log("0 fleets")
            return
        try_count += 1


def send_commission():
    if Btn.commission_completed.click(utils.screenshot()):
        log("Completing commission")
        while Btn.commission_s.click(utils.screenshot()):
            Btn.item.click(utils.screenshot())

    if Btn.commission_go.click(utils.screenshot()):
        if Btn.commission_0.on_screen(utils.screenshot()):
            log("0 fleets")
            return
    else:
        return

    log("Starting urgent commissions oil")
    utils.click(11, 114, 28, 25, 3.0)
    send_one_commission(False, True, 5)

    log("Starting daily commissions oil")
    utils.click(12, 63, 30, 30, 3.0)
    send_one_commission(True, True, 5)

    log("Starting urgent commissions")
    utils.click(11, 114, 28, 25, 3.0)
    send_one_commission(False, False, 5)

    log("Starting daily commissions")
    utils.click(12, 63, 30, 30, 3.0)
    send_one_commission(True, False, 5)
