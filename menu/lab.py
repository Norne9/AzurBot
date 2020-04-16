import utils
from data import Btn
from btn import Clickable


def start_lab():
    utils.click(3, 70, 11, 24, 2.0)  # open left panel
    while not Btn.technology.on_screen(utils.screenshot()):  # open lab
        utils.click(212, 277, 19, 11, 1.0)
    for btn in [Btn.lab_girl, Btn.tech_rigging, Btn.tech_donation, Btn.tech_basic]:
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
