import utils
from log import log
import adb
from data import Btn
from .commission import send_commission
from .lab import start_lab
from .remove import enhance_ships, retire_ships
from .book import learn_book

__all__ = ["after_level", "left_panel", "send_commission", "start_lab", "enhance_ships", "retire_ships", "learn_book"]


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
    learn_book()

    utils.click_home()  # go to main menu
    log("Done!")


def left_panel():
    utils.click(3, 70, 11, 24, 3.0)  # open left panel
    screen = adb.screenshot()
    Btn.menu_can.click(screen)  # tap can
    Btn.menu_money.click(screen)  # tap money

    send_commission()
    log("Commissions done")
