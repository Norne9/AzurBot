import subprocess
import cv2
from typing import List


def shell(cmd: List[str]) -> str:
    args = ["adb", "shell"]
    args.extend(cmd)
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as proc:
        out, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB error: {err.decode()}")
        return out.replace(b"\r\n", b"\n").decode().strip()


def screenshot():
    # take screenshot
    shell(["screencap", "/mnt/sdcard/test.png"])
    # pull it to pc
    with subprocess.Popen(
        ["adb", "pull", "/mnt/sdcard/test.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    ) as proc:
        _, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB error: {err.decode()}")
    # load
    image = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)
    # resize
    print(image.shape)
    resized = cv2.resize(image, (image.shape[1] // 3, image.shape[0] // 3), interpolation=cv2.INTER_AREA)
    if image.shape[0] > image.shape[1]:
        resized = cv2.rotate(resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return resized


def tap(x: int, y: int):
    shell(["input", "tap", str(int(x) * 3), str(int(y) * 3)])
