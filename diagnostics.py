import socket
import subprocess
import time
from pathlib import Path

import psutil

from version import NAME, VERSION, BUILD


class Diagnostics:
    def __init__(self, state, storage):
        self.state = state
        self.storage = storage
        self.boot_time = time.time()

    def ip_address(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "No network"

    def cpu_temp_value(self):
        path = Path("/sys/class/thermal/thermal_zone0/temp")
        try:
            return int(path.read_text()) / 1000
        except Exception:
            return None

    def cpu_temp(self):
        temp = self.cpu_temp_value()
        if temp is None:
            return "Unknown"
        return f"{temp:.1f}°C"

    def ram_usage(self):
        return f"{psutil.virtual_memory().percent:.0f}%"

    def uptime(self):
        seconds = int(time.time() - self.boot_time)
        return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"

    def camera_name(self):
        try:
            result = subprocess.run(
                ["rpicam-hello", "--list-cameras"],
                capture_output=True,
                text=True,
                timeout=3,
            )
            output = result.stdout.lower()
            if "imx296" in output:
                return "IMX296 Global Shutter"
            if "imx477" in output:
                return "IMX477 HQ Camera"
            return "Detected"
        except Exception:
            return "Unknown"

    def sections(self):
        return [
            ("ABOUT", [
                NAME,
                f"Version {VERSION}",
                f"Build {BUILD}",
            ]),
            ("CAMERA", [
                self.camera_name(),
            ]),
            ("MEDIA", [
                self.storage.label(),
                f"{self.storage.free_gb():.1f} GB free",
            ]),
            ("SYSTEM", [
                f"CPU {self.cpu_temp()}",
                f"RAM {self.ram_usage()}",
                f"Uptime {self.uptime()}",
            ]),
            ("NETWORK", [
                self.ip_address(),
            ]),
        ]
