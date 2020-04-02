import time
import requests
import os
import json
import threading


send_thread = None


def log(text: str):
    global send_thread
    print(f"[{time.strftime('%X')}] {text}")

    if send_thread:
        send_thread.join()

    send_thread = threading.Thread(target=send_msg, args=(text,))
    send_thread.start()


def send_msg(msg: str):
    if "al_log" not in os.environ:
        return
    hook_url = os.environ["al_log"]

    try:
        result = requests.post(
            hook_url, timeout=1, data=json.dumps({"content": msg}), headers={"Content-Type": "application/json"}
        )
        result.raise_for_status()
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.HTTPError as err:
        log(f"Discord error: {err}")


def send_img(name: str):
    if "al_loot" not in os.environ:
        return
    hook_url = os.environ["al_loot"]

    with open(name, mode="rb") as f:
        file = f.read()

    try:
        result = requests.post(hook_url, timeout=5, files={"file": ("screen.png", file)})
        result.raise_for_status()
    except requests.exceptions.Timeout:
        pass
    except requests.exceptions.HTTPError as err:
        log(f"Discord error: {err}")
