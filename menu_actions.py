import adb
import time
import utils
import random
from data import Btn, Img
from log import log
from btn import Clickable
import img
import numpy as np


def after_level(use_lab: bool):
    utils.click_home()  # go to main menu
    log("Removing trash")
    enhance_ships()

    utils.click_home()  # go to main menu
    log("Retiring trash")
    retire_ships()

    log("Collecting oil")
    utils.click_home()  # go to main menu
    left_panel()

    if use_lab:
        log("Starting labs")
        utils.click_home()  # go to main menu
        start_lab()

    utils.click_home()  # go to main menu
    log("Done!")


def left_panel():
    utils.click(3, 70, 11, 24, 3.0)  # open left panel
    screen = adb.screenshot()
    Btn.menu_can.click(screen)  # tap can
    Btn.menu_money.click(screen)  # tap money

    send_commission()
    log("Commissions done")


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


def send_girl():
    utils.click(121, 159, 27, 24, 3.0)  # click first plus
    for _ in range(2):  # swipe to bottom
        utils.scroll_down()
    for x in range(7):
        for y in range(3):
            utils.click(60 + 84 * x, 60 + 114 * y, 40, 10, 2.0)
            Btn.commission_select_cancel.click(adb.screenshot())
            if not Btn.commission_select_0.on_screen(adb.screenshot()):
                utils.click(468, 321, 86, 27, 2.0)
                return
    adb.back()
    time.sleep(2.0)


def send_best_commission(oil: bool, max_time: int) -> bool:
    if Btn.commission_0.on_screen(utils.screenshot()):  # check if we have fleets
        return False

    for _ in range(2):  # swipe to bottom
        utils.scroll_down()
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
    send_girl()
    Btn.commission_recommend.click(adb.screenshot())
    Btn.commission_ready.click(adb.screenshot())
    Btn.commission_confirm.click(adb.screenshot())
    # check if commission started
    time.sleep(6.0)
    has_cancel = Btn.commission_cancel.on_screen(utils.screenshot())
    # close commission window
    utils.click(63, 327, 18, 25, 1.0)
    return has_cancel


def send_commission():
    clicked_complete = False
    utils.click(200, 135, 42, 12, 2.0)  # click commissions
    while Btn.commission_s.click(utils.screenshot()):
        clicked_complete = True
    if clicked_complete:
        utils.click(200, 135, 42, 12, 2.0)  # click go

    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return

    log("Starting urgent commissions oil")
    utils.click(11, 114, 28, 25, 3.0)
    while send_best_commission(True, 40000):
        pass
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return

    log("Starting daily commissions oil")
    utils.click(12, 63, 30, 30, 3.0)
    while send_best_commission(True, 40000):
        pass
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return

    log("Starting urgent commissions")
    utils.click(11, 114, 28, 25, 3.0)
    while send_best_commission(False, 15000):
        pass
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return

    log("Starting daily commissions")
    utils.click(12, 63, 30, 30, 3.0)
    while send_best_commission(False, 15000):
        pass
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return


def start_lab():
    utils.click(3, 70, 11, 24, 2.0)  # open left panel
    while not Btn.technology.on_screen(utils.screenshot()):  # open lab
        utils.click(212, 277, 19, 11, 1.0)
    for btn in [Btn.lab_girl, Btn.tech_rigging]:
        if start_lab_image(btn):
            break


def start_lab_image(btn: Clickable):
    for _ in range(5):
        if btn.on_screen(utils.screenshot()):
            utils.click(301, 92, 36, 34, 2.0)  # open project
            if Btn.commence.click(utils.screenshot()):
                Btn.tech_confirm.click(utils.screenshot())
                return True
            else:
                return False
        utils.click(445, 77, 38, 52, 0.5)  # open project
        utils.click(445, 77, 38, 52, 1.5)  # open project
    return False
