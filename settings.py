import json
from pathlib import Path

PROJECT = Path.home() / "gorillacam"
RECORDINGS = PROJECT / "recordings"
CONFIG_DIR = PROJECT / "config"
CONFIG_FILE = CONFIG_DIR / "settings.json"

RECORDINGS.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

WHITE = (245, 245, 245)
GRAY = (150, 150, 150)
RED = (220, 40, 40)
GREEN = (70, 200, 110)
BLACK = (0, 0, 0)

MODE_OPTIONS = ["1080P", "720P", "420P"]
FPS_OPTIONS = [24, 25, 30, 60]
SHUTTER_OPTIONS = ["1/48", "1/50", "1/60", "1/120"]
GAIN_OPTIONS = ["1.0", "2.0", "4.0", "8.0"]
WB_OPTIONS = ["AUTO", "3200K", "5600K", "6500K"]

MODE_CONFIGS = {
    "1080P": {"width": 1920, "height": 1080},
    "720P": {"width": 1280, "height": 720},
    "420P": {"width": 640, "height": 420},
}

SHUTTER_US = {
    "1/48": 20833,
    "1/50": 20000,
    "1/60": 16666,
    "1/120": 8333,
}

WB_GAINS = {
    "3200K": (1.7, 1.1),
    "5600K": (1.4, 1.5),
    "6500K": (1.3, 1.7),
}

DEFAULT_STATE = {
    "mode": "1080P",
    "fps": 24,
    "shutter": "1/48",
    "gain": "1.0",
    "wb": "AUTO",
    "recording": False,
    "streaming": False,
}


def load_state():
    state = DEFAULT_STATE.copy()

    if CONFIG_FILE.exists():
        try:
            saved = json.loads(CONFIG_FILE.read_text())
            for key in ("mode", "fps", "shutter", "gain", "wb"):
                if key in saved:
                    state[key] = saved[key]
        except Exception:
            pass

    if state["mode"] not in MODE_OPTIONS:
        state["mode"] = DEFAULT_STATE["mode"]

    state["recording"] = False
    state["streaming"] = False
    return state


def save_state(state):
    saved = {
        "mode": state["mode"],
        "fps": state["fps"],
        "shutter": state["shutter"],
        "gain": state["gain"],
        "wb": state["wb"],
    }

    CONFIG_FILE.write_text(json.dumps(saved, indent=2))
