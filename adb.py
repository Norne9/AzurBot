import subprocess
import cv2
import numpy as np
from typing import List


def shell(cmd: List[str]) -> str:
    args = ["adb", "shell"]
    args.extend(cmd)
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as proc:
        out, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB {err.decode()}")
        return out.replace(b"\r\n", b"\n").decode().strip()


def screenshot_hd_gray():
    with subprocess.Popen(
        ["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as proc:
        data, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB {err.decode()}")
    resized = cv2.imdecode(np.frombuffer(data, np.int8), cv2.IMREAD_GRAYSCALE)
    if resized.shape[0] > resized.shape[1]:
        resized = cv2.rotate(resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return resized


def screenshot(low_quality: bool = True):
    with subprocess.Popen(
        ["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as proc:
        data, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB {err.decode()}")
    # load
    if low_quality:
        image = cv2.imdecode(np.frombuffer(data, np.int8), cv2.IMREAD_GRAYSCALE)
        resized = cv2.resize(image, (image.shape[1] // 3, image.shape[0] // 3), interpolation=cv2.INTER_AREA)
    else:
        resized = cv2.imdecode(np.frombuffer(data, np.int8), cv2.IMREAD_COLOR)

    if resized.shape[0] > resized.shape[1]:
        resized = cv2.rotate(resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return resized


def tap(x: int, y: int):
    x, y = min(1919, max(0, x)), min(1079, max(0, y))
    shell(["input", "tap", str(int(x)), str(int(y))])


def swipe(x1: int, y1: int, x2: int, y2: int):
    shell(["input", "swipe", str(int(x1)), str(int(y1)), str(int(x2)), str(int(y2))])


def back():
    shell(["input", "keyevent", "4"])


def stop_game():
    shell(["am", "force-stop", "com.YoStarEN.AzurLane"])


def start_game():
    shell(["monkey", "-p", "com.YoStarEN.AzurLane", "1"])
