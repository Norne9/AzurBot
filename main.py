from adb import shell, screenshot, tap
import cv2
import time


def run():
    print(shell(["echo", '"Hello world!"']))
    while True:
        cmd = input("Press enter... ")
        if len(cmd) > 0:
            break
        screen = screenshot()
        cv2.imwrite(f"screenshots/{time.time()}.png", screen)


if __name__ == "__main__":
    run()
