import adb
import utils
from data import Btn
from log import log
import random
import time


def enhance_ships():
    utils.click(87, 332, 74, 24, 3.0)  # open dock

    Btn.sort.click(utils.screenshot())
    if adb.screenshot(False)[820, 1144, 2] > 100:
        utils.click(384, 260, 57, 14, 1.0)
    Btn.sort_confirm.click(utils.screenshot())

    utils.click(49, 53, 63, 56, 3.0)  # click first ship
    Btn.enhance.click(utils.screenshot())

    no_enhance = 0
    while True:
        # click enhance
        if Btn.enhance.on_screen(utils.screenshot()):
            utils.click(483, 302, 58, 19, 0.5)  # press fill button
            utils.click(567, 302, 58, 19, 2.0)  # press enhance button

            if Btn.enhance_confirm.click(utils.screenshot()):  # press confirm
                no_enhance = 0
                if Btn.enhance_break.click(utils.screenshot()):  # press disassemble
                    utils.click(434, 244, 164, 97, 2.0)  # tap to continue
                else:  # something went wrong
                    log("No break button!")
            else:
                no_enhance += 1
        else:
            no_enhance += 10
            log("No enhance button!")

        if no_enhance >= 4:  # stop if we can't enhance 4 times
            break

        adb.swipe(  # swipe to next ship
            random.randint(900, 966), random.randint(501, 558), random.randint(210, 276), random.randint(501, 558)
        )
        time.sleep(1.0)


def retire_ships():
    def sort_rare():
        utils.click(556, 7, 32, 12, 2.0)  # click sort
        utils.click(318, 226, 31, 8, 1.0)  # click rare
        utils.click(372, 318, 55, 7, 2.0)  # click confirm

    utils.click(491, 336, 55, 16, 3.0)  # click build
    utils.click(10, 221, 30, 32, 3.0)  # click retire
    sort_rare()

    # no ships
    if Btn.retire_nothing.on_screen(utils.screenshot()):
        log("Nothing to retire")
        sort_rare()  # disable sorting
        return

    # select ships
    for x in range(7):
        utils.click(54 + x * 82, 56, 54, 50, 0.3)

    utils.click(556, 328, 58, 13, 2.0)  # click confirm

    if Btn.retire_confirm.click(utils.screenshot()):  # press confirm
        if Btn.enhance_confirm.click(utils.screenshot()):  # press confirm
            if Btn.enhance_break.click(utils.screenshot()):  # press disassemble
                utils.screenshot()

    sort_rare()
