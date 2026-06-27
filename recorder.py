import os
import signal
import subprocess
import time


class Recorder:
    def __init__(self, state, camera, storage):
        self.state = state
        self.camera = camera
        self.storage = storage
        self.start_time = None
        self.process = None

    def toggle(self):
        if self.state["recording"]:
            self.stop()
        else:
            self.start()

    def start(self):
        if self.state["recording"]:
            return

        filepath = self.storage.new_recording_path()

        cmd = [
            "rpicam-vid",
            "-t", "0",
            "--width", "1920",
            "--height", "1080",
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

        self.process = None
        self.state["recording"] = False
        self.start_time = None

    def timer(self):
        if not self.start_time:
            return "00:00:00"

        seconds = int(time.time() - self.start_time)
        return f"{seconds // 3600:02d}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"
