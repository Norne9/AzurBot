import time
import requests
import os
import json


def log(text: str):
    print(f"[{time.strftime('%X')}] {text}")
    send_msg(text)


def send_msg(msg: str):
    if "al_log" not in os.environ:
        return
    hook_url = os.environ["al_log"]

    result = requests.post(hook_url, data=json.dumps({"content": msg}), headers={"Content-Type": "application/json"})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        log(f"Discord error: {err}")


def send_img(name: str):
    if "al_loot" not in os.environ:
        return
    hook_url = os.environ["al_loot"]

    with open(name, mode="rb") as f:
        file = f.read()
    result = requests.post(hook_url, files={"file": ("screen.png", file)})

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        log(f"Discord error: {err}")
