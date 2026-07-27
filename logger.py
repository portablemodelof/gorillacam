from datetime import datetime
from settings import PROJECT

LOG_DIR = PROJECT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)


class Logger:
    def __init__(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = LOG_DIR / f"{today}.log"

    def write(self, message):
        stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.log_file.open("a") as f:
            f.write(f"[{stamp}] {message}\n")
