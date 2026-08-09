try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None

from camera_sources import TestCamera
from settings import SHUTTER_US, WB_GAINS, MODE_CONFIGS


class Camera:
    def __init__(self, state):
        self.state = state

        if Picamera2:
            self.picam2 = Picamera2()
            self.is_pi_camera = True
        else:
            mode = MODE_CONFIGS[self.state["mode"]]
            self.picam2 = TestCamera(
                mode["width"],
                mode["height"]
            )
            self.is_pi_camera = False

        self.configure()

    def configure(self):
        if not self.is_pi_camera:
            return

        mode = MODE_CONFIGS[self.state["mode"]]

        config = self.picam2.create_video_configuration(
            main={
                "size": (mode["width"], mode["height"]),
                "format": "RGB888",
            }
        )

        self.picam2.configure(config)

    def restart_with_new_mode(self):
        if not self.is_pi_camera:
            return

        self.picam2.stop()
        self.configure()
        self.picam2.start()
        self.apply_controls()

    def start(self):
        self.picam2.start()

        if self.is_pi_camera:
            self.apply_controls()

    def stop(self):
        self.picam2.stop()

    def capture_frame(self):
        return self.picam2.capture_array()

    def apply_controls(self):
        if not self.is_pi_camera:
            return

        fps = self.state["fps"]
        frame_time = int(1_000_000 / fps)

        controls = {
            "FrameDurationLimits": (frame_time, frame_time),
            "ExposureTime": SHUTTER_US[self.state["shutter"]],
            "AnalogueGain": float(self.state["gain"]),
        }

        if self.state["wb"] == "AUTO":
            controls["AwbEnable"] = True
        else:
            controls["AwbEnable"] = False
            controls["ColourGains"] = WB_GAINS[self.state["wb"]]

        self.picam2.set_controls(controls)
