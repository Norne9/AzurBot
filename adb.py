import subprocess
import cv2
import numpy as np
import socket
import random
import os
import struct
from typing import List

MY_IP: str = "127.0.0.1"
MY_PORT: int = 10000


def shell(cmd: List[str]) -> str:
    args = ["shell"]
    args.extend(cmd)
    return adb_basic(args).replace(b"\r\n", b"\n").decode().strip()


def adb_basic(cmd: List[str]) -> bytes:
    args = ["adb"]
    args.extend(cmd)
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,) as proc:
        data, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB {err.decode()}")
        return data


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def prepare() -> str:
    global MY_IP, MY_PORT
    MY_IP = get_ip()
    MY_PORT = random.randint(58000, 59000)

    # prepare sh script
    with open("android-data/touch.sh", mode="rb") as f:
        touch_sh = f.read()
    with open("android-data/touch.sh", mode="wb") as f:
        f.write(touch_sh.replace(b"\r", b""))

    with open("android-data/ss.sh", mode="w") as f:
        f.write(f"/data/local/tmp/ascreencap --stdout | /data/local/tmp/nc {get_ip()} {MY_PORT}")
    adb_basic(["push", "android-data/ss.sh", "/data/local/tmp/"])
    os.remove("android-data/ss.sh")

    adb_basic(["push", "android-data/ascreencap", "/data/local/tmp/"])
    adb_basic(["push", "android-data/nc", "/data/local/tmp/"])
    adb_basic(["push", "android-data/touch.sh", "/data/local/tmp/"])

    shell(["chmod", "0777", "/data/local/tmp/ss.sh"])
    shell(["chmod", "0777", "/data/local/tmp/ascreencap"])
    shell(["chmod", "0777", "/data/local/tmp/nc"])
    shell(["chmod", "0777", "/data/local/tmp/touch.sh"])

    return shell(["echo", '"Android connected!"'])


def screenshot_data() -> bytes:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((MY_IP, MY_PORT))
    s.listen(1)

    with subprocess.Popen(
        ["adb", "exec-out", "/data/local/tmp/ss.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ) as proc:
        conn, addr = s.accept()

        chunks = []
        while True:
            data = conn.recv(2048)
            if not data:
                break
            chunks.append(data)
        conn.close()
        s.close()

        _, err = proc.communicate()
        if len(err) > 0:
            raise Exception(f"ADB {err.decode()}")
    return b"".join(chunks)


def screenshot_hd_gray():
    data = screenshot_data()
    resized = cv2.imdecode(np.frombuffer(data, np.int8), cv2.IMREAD_GRAYSCALE)
    if resized.shape[0] > resized.shape[1]:
        resized = cv2.rotate(resized, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return resized


def screenshot(low_quality: bool = True):
    data = screenshot_data()

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


def append_command(data: bytearray, cmd_type: int, code: int, value: int):
    data.extend(struct.pack("<llHHi", 0, 0, cmd_type, code, int(value)))


def hold(x, y):
    data = bytearray()
    append_command(data, 1, 330, 1)
    append_command(data, 3, 53, x)
    append_command(data, 3, 54, y)
    append_command(data, 0, 2, 0)
    append_command(data, 0, 0, 0)
    command = "echo -n -e '" + "".join([f"\\x{b:02x}" for b in data]) + "' > /dev/input/event4"
    shell(command.split())


def release():
    data = bytearray()
    append_command(data, 1, 330, 0)
    append_command(data, 3, 53, 0)
    append_command(data, 3, 54, 0)
    append_command(data, 0, 2, 0)
    append_command(data, 0, 0, 0)
    command = "echo -n -e '" + "".join([f"\\x{b:02x}" for b in data]) + "' > /dev/input/event4"
    shell(command.split())
