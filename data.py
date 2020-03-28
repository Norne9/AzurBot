from btn import Clickable
import cv2
import numpy as np


class Btn:
    question = Clickable([f"question{i}" for i in range(2)], offset_y=30, delay=0)
    switch = Clickable("switch", delay=5.0)
    mood = Clickable("mood")

    level_name = Clickable("level_name")
    event_name = Clickable("event_name")
    unable_info = Clickable("unable_info")

    close = Clickable("close", x=590, y=26)
    item = Clickable("item", x=273, y=107)
    menu_battle = Clickable("menu_battle", x=507, y=150)
    cmode = Clickable("cmode", x=518, y=294)
    go1 = Clickable("go1", x=459, y=247, delay=1.0)
    go2 = Clickable("go2", x=525, y=291, delay=6.0)
    evade = Clickable("evade", x=505, y=224)
    got_it = Clickable("got_it", delay=1.0)
    auto = Clickable("auto", x=376, y=56, delay=1.0)
    auto_sub = Clickable("auto_sub", x=377, y=84, delay=1.0)
    battle = Clickable("battle", x=529, y=306, delay=2.0)
    confirm = Clickable("confirm", x=511, y=321, delay=6.0)
    lock_confirm = Clickable("lock_confirm", x=360, y=252)
    lose_confirm = Clickable("lose_confirm", x=286, y=258)
    lose_close = Clickable("lose_close", x=298, y=305)
    commission = Clickable("commission", x=284, y=252)
    reconnect = Clickable("reconnect", x=360, y=252)
    download = Clickable("download", x=364, y=242)
    update = Clickable("update", x=284, y=251)
    retreat = Clickable("retreat", x=380, y=330)

    sort = Clickable("sort", x=555, y=7)
    sort_confirm = Clickable("sort_confirm", x=369, y=314)
    enhanceable = Clickable("enhanceable", x=380, y=270)
    enhance_confirm = Clickable("enhance_confirm", x=447, y=262)
    enhance_break = Clickable("enhance_break", x=367, y=277)
    enhance = Clickable(["enhance_button1", "enhance_button2"], delay=1.0)

    commission_completed = Clickable("commission_completed", x=192, y=136)
    commission_s = Clickable("commission_s")
    commission_go = Clickable("commission_go", x=213, y=134)
    commission_0 = Clickable("commission_0", x=541, y=10)
    commission_new = Clickable("commission_new")
    commission_recommend = Clickable("commission_recommend", delay=1.0)
    commission_ready = Clickable("commission_ready", delay=3.0)
    commission_confirm = Clickable("commission_confirm", x=360, y=256)
    commission_cost = Clickable("commission_cost", x=558, y=147)
    commission_oil = Clickable("commission_oil")
    commission_cancel = Clickable("commission_cancel", x=529, y=170)
    commission_select_cancel = Clickable("commission_select_cancel", x=216, y=256)
    commission_select_0 = Clickable("commission_select_0", x=297, y=333)

    menu_can = Clickable("menu_can", delay=1.0)
    menu_money = Clickable("menu_money", delay=6.0)
    menu_quit_cancel = Clickable("menu_quit_cancel", x=216, y=257, delay=1.0)

    zero_heals = Clickable("zero_heals", x=68, y=273, delay=2.0)
    use_heal = Clickable("use_heal", x=365, y=217, delay=3.0)
    cancel_heal = Clickable("cancel_heal", x=238, y=219, delay=3.0)


class Img:
    arrow = cv2.imread(f"images/arrow.png", cv2.IMREAD_GRAYSCALE)
    boss = cv2.imread(f"images/boss.png", cv2.IMREAD_GRAYSCALE)
    digits = [cv2.imread(f"images/digits/{i}.png", cv2.IMREAD_GRAYSCALE) for i in range(10)]
    commission = cv2.imread(f"images/commission_new.png", cv2.IMREAD_GRAYSCALE)

    # for frame recognition
    ally_color = np.array([[[57, 235, 156]]], dtype=np.uint8)
    enemy_color = np.full((2, 2, 3), np.array([57, 60, 247]), dtype=np.uint8)
    bomb_template = cv2.imread(f"images/game/bomb.png", cv2.IMREAD_COLOR)
    auto_template = cv2.imread(f"images/game/auto.png", cv2.IMREAD_GRAYSCALE)

    # for triangle finding
    triangle_template = cv2.imread("images/triangle.png", cv2.IMREAD_GRAYSCALE)
    triangle_big_template = cv2.imread("images/triangle_big.png", cv2.IMREAD_GRAYSCALE)
    deadzone_image = cv2.imread("images/deadzone.png", cv2.IMREAD_GRAYSCALE)
