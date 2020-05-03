import utils
from data import Btn
from btn import Clickable
import adb


def start_lab():
    utils.click(3, 70, 11, 24, 2.0)  # open left panel
    while not Btn.technology.on_screen(adb.screenshot()):  # open lab
        utils.click(212, 277, 19, 11, 1.0)

    utils.click(301, 92, 36, 34, 2.0)  # click center
    if Btn.tech_terminate.on_screen(adb.screenshot()):
        return
    utils.click(445, 77, 38, 52, 0.5)  # close project

    for btn in [Btn.lab_girl, Btn.tech_rigging, Btn.tech_donation, Btn.tech_basic]:
        if start_lab_image(btn):
            break


def start_lab_image(btn: Clickable):
    for _ in range(5):
        if btn.on_screen(adb.screenshot()):
            utils.click(301, 92, 36, 34, 2.0)  # open project
            if Btn.tech_terminate.on_screen(adb.screenshot()):
                return True
            if Btn.commence.click(adb.screenshot()):
                if Btn.tech_confirm.click(adb.screenshot()):
                    if Btn.tech_terminate.on_screen(adb.screenshot()):
                        return True
                else:
                    utils.click(445, 77, 38, 52, 0.5)  # close project
            else:
                utils.click(445, 77, 38, 52, 0.5)  # close project
                return False
        utils.click(445, 77, 38, 52, 0.5)  # next project
        utils.click(445, 77, 38, 52, 1.5)  # close project
    return False
