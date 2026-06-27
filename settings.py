from pathlib import Path

PROJECT = Path.home() / "gorillacam"
RECORDINGS = PROJECT / "recordings"
RECORDINGS.mkdir(parents=True, exist_ok=True)

WHITE = (245, 245, 245)
GRAY = (150, 150, 150)
RED = (220, 40, 40)
GREEN = (70, 200, 110)
BLACK = (0, 0, 0)

FPS_OPTIONS = [24, 25, 30, 60]
SHUTTER_OPTIONS = ["1/48", "1/50", "1/60", "1/120"]
GAIN_OPTIONS = ["1.0", "2.0", "4.0", "8.0"]
WB_OPTIONS = ["AUTO", "3200K", "5600K", "6500K"]

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
    "resolution": "1080P",
    "fps": 24,
    "shutter": "1/48",
    "gain": "1.0",
    "wb": "AUTO",
    "recording": False,
    "streaming": False,
}
