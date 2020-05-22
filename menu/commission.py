import adb
import time
import utils
from data import Btn, Img
import numpy as np
import img
from log import log


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
    for _ in range(3):  # swipe to bottom
        utils.scroll_down()
    for y in range(3):
        for x in range(7):
            utils.click(60 + 84 * x, 60 + 114 * y, 40, 10, 2.0)
            Btn.commission_select_cancel.click(adb.screenshot())
            if not Btn.commission_select_0.on_screen(adb.screenshot()):
                utils.click(535, 328, 60, 14, 2.0)
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
    while send_best_commission(False, 29000):
        pass
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return

    log("Starting daily commissions")
    utils.click(12, 63, 30, 30, 3.0)
    while send_best_commission(False, 22000):
        pass
    if Btn.commission_0.on_screen(utils.screenshot()):
        log("0 fleets")
        return
