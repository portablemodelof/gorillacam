import os
import signal
import subprocess
import time
from settings import MODE_CONFIGS

class Recorder:
    def __init__(self, state, camera, storage, events):
        self.state = state
        self.camera = camera
        self.storage = storage
        self.events = events
        self.start_time = None
        self.process = None
        self.current_file = None

    def toggle(self):
        if self.state["recording"]:
            self.stop()
        else:
            self.start()

    def start(self):
        if self.state["recording"]:
            return

        filepath = self.storage.new_recording_path()
        self.current_file = filepath

        cmd = [
            "rpicam-vid",
            "-t", "0",
            "--width", str(MODE_CONFIGS[self.state["mode"]]["width"]),
            "--height", str(MODE_CONFIGS[self.state["mode"]]["height"]),
            "--framerate", str(self.state["fps"]),
            "--codec", "libav",
            "--libav-format", "mp4",
            "--bitrate", "25000000",
            "--nopreview",
            "-o", str(filepath),
        ]

        self.process = subprocess.Popen(cmd, preexec_fn=os.setsid)
        self.state["recording"] = True
        self.start_time = time.time()
        self.events.post("Recording Started")

    def stop(self):
        if not self.state["recording"]:
            return

        try:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            time.sleep(0.5)

            if self.process.poll() is None:
                os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
        except Exception:
            pass

        saved_name = self.current_file.name if self.current_file else "Clip Saved"

        self.process = None
        self.state["recording"] = False
        self.start_time = None
        self.current_file = None

        self.events.post(f"Saved {saved_name}", seconds=2.5)

    def timer(self):
        if not self.start_time:
            return "00:00:00"

        seconds = int(time.time() - self.start_time)
        return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
