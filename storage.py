import shutil
from pathlib import Path
from datetime import datetime

from settings import RECORDINGS

GORILLA_SSD = Path("/media/gorilla/GorillaSSD")


class Storage:
    def active_dir(self):
        if GORILLA_SSD.exists() and GORILLA_SSD.is_mount():
            folder = GORILLA_SSD / "recordings"
            folder.mkdir(parents=True, exist_ok=True)
            return folder, "SSD"

        RECORDINGS.mkdir(parents=True, exist_ok=True)
        return RECORDINGS, "SD"

    def new_recording_path(self):
        folder, _ = self.active_dir()
        day_folder = folder / datetime.now().strftime("%Y-%m-%d")
        day_folder.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%H-%M-%S")
        return day_folder / f"gorillacam_{stamp}.mp4"

    def label(self):
        _, label = self.active_dir()
        return label

    def free_gb(self):
        folder, _ = self.active_dir()
        try:
            usage = shutil.disk_usage(folder)
            return usage.free / (1024 ** 3)
        except Exception:
            return 0.0



