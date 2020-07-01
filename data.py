from btn import Clickable
import cv2
import numpy as np


class Btn:
    switch = Clickable("switch", delay=5.0)
    mood = Clickable("mood")

    level_name = Clickable("level_name")
    event_name = Clickable("event_name")
    unable_info = Clickable("unable_info")
    archives = Clickable("archives", x=95, y=335)
    no_oil = Clickable("no_oil", x=211, y=160)

    close = Clickable("close", x=590, y=26)
    item = Clickable("item", x=273, y=107)
    item2 = Clickable("item2", x=274, y=72)
    menu_battle = Clickable("menu_battle", x=507, y=150)
    cmode = Clickable("cmode", x=518, y=294)
    go1 = Clickable("go1", x=445, y=253, delay=1.0)
    go2 = Clickable("go2", x=514, y=295, delay=8.0)
    evade = Clickable("evade", x=505, y=224)
    got_it = Clickable("got_it", delay=1.0)
    auto = Clickable("auto", x=376, y=56, delay=1.0)
    auto_sub = Clickable("auto_sub", x=377, y=84, delay=1.0)
    battle = Clickable("battle", x=529, y=306, delay=5.0)
    lose_close = Clickable("lose_close", x=298, y=305)
    retreat = Clickable("retreat", x=380, y=330)

    sort = Clickable("sort", x=555, y=7)
    enhanceable = Clickable("enhanceable", x=380, y=270)
    enhance_break = Clickable("enhance_break", x=367, y=277)
    enhance = Clickable(["enhance_button1", "enhance_button2"], delay=1.0)
    retire_nothing = Clickable("retire_nothing", x=47, y=170)
    retire_button = Clickable("retire_button")

    commission_completed = Clickable("commission_completed", x=192, y=136)
    commission_s = Clickable("commission_s")
    commission_go = Clickable("commission_go", x=213, y=134)
    commission_0 = Clickable("commission_0", x=541, y=10)
    commission_new = Clickable("commission_new")
    commission_recommend = Clickable("commission_recommend", delay=1.0)
    commission_ready = Clickable("commission_ready", delay=3.0)
    commission_cost = Clickable("commission_cost", x=558, y=147)
    commission_oil = Clickable("commission_oil")
    commission_cancel = Clickable("commission_cancel", x=530, y=178)
    commission_select_cancel = Clickable("commission_select_cancel", x=216, y=256)
    commission_select_0 = Clickable("commission_select_0", x=354, y=333)

    menu_can = Clickable("menu_can", delay=1.0)
    menu_money = Clickable("menu_money", delay=1.0)
    menu_quit_cancel = Clickable("menu_quit_cancel", x=219, y=248, delay=1.0)

    zero_heals = Clickable("zero_heals", x=68, y=273, delay=2.0)
    use_heal = Clickable("use_heal", x=365, y=217, delay=3.0)
    cancel_heal = Clickable("cancel_heal", x=238, y=219, delay=3.0)

    technology = Clickable("technology", x=58, y=6)
    tech_rigging = Clickable("tech_rigging", x=275, y=48)
    tech_basic = Clickable("tech_basic", x=277, y=48)
    tech_donation = Clickable("tech_donation", x=277, y=48)
    commence = Clickable("commence", x=216, y=285)
    tech_terminate = Clickable("tech_terminate", x=220, y=285)
    lab_girl = Clickable("lab_girl", x=340, y=40)  # x:340 y:40 s:25x60

    universal_confirm = Clickable(
        [
            "universal_confirm",
            "universal_confirm_mini",
            "universal_confirm2",
            "universal_confirm3",
            "universal_confirm4",
            "universal_confirm5",
        ]
    )


class Img:
    arrow = cv2.imread(f"images/arrow.png", cv2.IMREAD_GRAYSCALE)
    boss = cv2.imread(f"images/boss.png", cv2.IMREAD_GRAYSCALE)
    boss_mini = cv2.imread(f"images/boss_mini.png", cv2.IMREAD_GRAYSCALE)
    digits = [cv2.imread(f"images/digits/{i}.png", cv2.IMREAD_GRAYSCALE) for i in range(10)]
    commission = cv2.imread(f"images/commission_new.png", cv2.IMREAD_GRAYSCALE)
    question0 = cv2.imread("images/question0.png", cv2.IMREAD_GRAYSCALE)
    question1 = cv2.imread("images/question1.png", cv2.IMREAD_GRAYSCALE)

    # for frame recognition
    ally_color = np.array([[[57, 235, 156]]], dtype=np.uint8)
    enemy_color = np.full((2, 2, 3), np.array([57, 60, 247]), dtype=np.uint8)
    bomb_template = cv2.imread(f"images/game/bomb.png", cv2.IMREAD_COLOR)
    auto_template = cv2.imread(f"images/game/auto.png", cv2.IMREAD_GRAYSCALE) / 255.0

    # for learning
    book_color = np.full((4, 4, 3), np.array([99, 255, 148]), dtype=np.uint8)

    # for triangle finding
    triangle_template = cv2.imread("images/triangle.png", cv2.IMREAD_GRAYSCALE)
    triangle_big_template = cv2.imread("images/triangle_big.png", cv2.IMREAD_GRAYSCALE)
    deadzone_image = cv2.imread("images/deadzone.png", cv2.IMREAD_GRAYSCALE)
