from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

from settings import SHUTTER_US, WB_GAINS


class Camera:
    def __init__(self, state):
        self.state = state
        self.picam2 = Picamera2()

        config = self.picam2.create_video_configuration(
            main={"size": (1280, 720), "format": "RGB888"}
        )
        self.picam2.configure(config)

        self.encoder = None
        self.output = None

    def start(self):
        self.picam2.start()
        self.apply_controls()

    def stop(self):
        self.picam2.stop()

    def capture_frame(self):
        return self.picam2.capture_array()

    def apply_controls(self):
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

    def start_recording(self, filepath):
        self.encoder = H264Encoder(bitrate=25_000_000)
        self.output = FfmpegOutput(str(filepath))
        self.picam2.start_recording(self.encoder, self.output)

    def stop_recording(self):
        self.picam2.stop_recording()
