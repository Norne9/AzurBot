import adb
import time
import utils
import random
from data import Btn, Img
from log import log
import img
import numpy as np


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


def parse_time(time_pic: np.ndarray) -> int:
    digit_mul = [10 * 60 * 60, 1 * 60 * 60, 10 * 60, 1 * 60, 10, 1]

    # digit separation table
    digit_sep: np.ndarray = np.sum(time_pic, axis=0) < 3500
    digit_sep[-1] = True

    # cut single digit & recognize
    last_sep, last_pos = True, 0
    digits = []
    for pos in range(digit_sep.shape[0]):
        if digit_sep[pos] and not last_sep and pos - last_pos > 6:
            digit = time_pic[:, last_pos : pos + 1]
            digit = np.concatenate([np.full_like(digit, 64), digit, np.full_like(digit, 64)], axis=1)
            digits.append(img.which(digit, Img.digits))
        if digit_sep[pos]:
            last_pos = pos
        last_sep = digit_sep[pos]

    # compute time in seconds
    time_num = 0
    for num, mul in zip(digits, digit_mul):
        time_num += num * mul

    return time_num


def send_best_commission(oil: bool, max_time: int) -> bool:
    if Btn.commission_0.on_screen(utils.screenshot()):  # check if we have fleets
        log("0 fleets")
        return False

    for _ in range(2):  # swipe to bottom
        adb.swipe(1100, 1030, 1100, 130)
    time.sleep(2.0)

    screen = utils.screenshot()  # make screenshots
    screen_hd = adb.screenshot_hd_gray()
    commission_buttons = img.find_zones(utils.screenshot(), Img.commission, 0.9)

    best_x, best_y, best_time = -1, -1, max_time
    for x, y, w, h in commission_buttons:
        # check oil
        has_oil = Btn.commission_oil.on_screen(screen[y - 30 : y + 20, x + 129 : x + 400])
        if oil != has_oil:
            continue

        # check time
        time_img = screen_hd[y * 3 + 2 * 3 : y * 3 + 13 * 3, x * 3 + 66 * 3 : x * 3 + 107 * 3]
        time_num = parse_time(time_img)
        if time_num > max_time:
            continue

        # remember best commission
        if time_num < best_time:
            best_time = time_num
            best_x, best_y = x, y

    if best_time >= max_time:
        return False

    # start commission
    utils.click(best_x, best_y, 45, 13, 3.0)
    Btn.commission_recommend.click(utils.screenshot())
    Btn.commission_ready.click(utils.screenshot())
    Btn.commission_confirm.click(utils.screenshot())
    # check if commission started
    time.sleep(3.0)
    has_cancel = Btn.commission_cancel.on_screen(utils.screenshot())
    # close commission window
    utils.click(63, 327, 18, 25, 1.0)
    return has_cancel


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
    while send_best_commission(True, 40000):
        pass

    log("Starting daily commissions oil")
    utils.click(12, 63, 30, 30, 3.0)
    while send_best_commission(True, 40000):
        pass

    log("Starting urgent commissions")
    utils.click(11, 114, 28, 25, 3.0)
    while send_best_commission(False, 15000):
        pass

    log("Starting daily commissions")
    utils.click(12, 63, 30, 30, 3.0)
    while send_best_commission(False, 15000):
        pass
