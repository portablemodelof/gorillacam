import shutil
from pathlib import Path
from datetime import datetime

from settings import RECORDINGS


class Storage:
    def active_dir(self):
        media_root = Path("/media")

        if media_root.exists():
            for user_dir in media_root.iterdir():
                if user_dir.is_dir():
                    for mount in user_dir.iterdir():
                        if mount.is_dir():
                            out = mount / "gorillacam"
                            out.mkdir(parents=True, exist_ok=True)
                            return out, "USB"

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
        usage = shutil.disk_usage(folder)
        return usage.free / (1024 ** 3)
