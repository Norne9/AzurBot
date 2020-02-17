import cv2
import img
import adb
import random
import time
import numpy as np
from log import log
from typing import Union, List


class Clickable:
    def __init__(
        self,
        image_names: Union[str, List[str]],
        x: int = -1,
        y: int = -1,
        offset_x: int = 0,
        offset_y: int = 0,
        delay: float = 3.0,
    ):
        if type(image_names) == str:  # if single string -> convert to array
            image_names = [image_names]
        self.image_names = image_names
        self.images = [cv2.imread(f"images/{name}.png", cv2.IMREAD_GRAYSCALE) for name in image_names]
        self.x = x
        self.y = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.delay = delay

    def on_screen(self, screen: np.ndarray) -> bool:
        for image in self.images:
            if self.__on_screen(screen, image):
                return True
        return False

    def click(self, screen: np.ndarray) -> bool:
        for name, image in zip(self.image_names, self.images):
            if self.__click(screen, image):
                log(f"Pressed {name}. Waiting {self.delay}s")
                time.sleep(self.delay)
                return True
        return False

    def __on_screen(self, screen: np.ndarray, image: np.ndarray) -> bool:
        if self.x < 0:  # find mode
            return len(img.find_zones(screen, image, 0.7)) > 0
        # check mode
        return img.check_zone(screen, image, self.x, self.y) > 0.9

    def __click(self, screen: np.ndarray, image: np.ndarray) -> bool:
        if self.x < 0:  # find mode
            zones = img.find_zones(screen, image, 0.7)
            if len(zones) == 0:
                return False
            x, y, w, h = random.choice(zones)
            x, y = x + self.offset_x, y + self.offset_y
            x, y = x * 3 + random.randint(0, w * 3), y * 3 + random.randint(0, h * 3)
        else:
            if img.check_zone(screen, image, self.x, self.y) < 0.9:
                return False
            x, y = self.x + self.offset_x, self.y + self.offset_y
            x, y = (
                x * 3 + random.randint(0, image.shape[1] * 3),
                y * 3 + random.randint(0, image.shape[0] * 3),
            )
        adb.tap(x, y)
        return True
