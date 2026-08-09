import numpy as np
import time
import cv2


class TestCamera:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

        self.start_time = time.time()
        self.frames = 0
        self.fps = 30

    def start(self):
        pass

    def stop(self):
        pass

    def draw_centered_text(self, frame, text, y, scale=2):
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 4

        (text_width, text_height), _ = cv2.getTextSize(
            text,
            font,
            scale,
            thickness
        )

        x = (self.width - text_width) // 2

        # black background box
        cv2.rectangle(
            frame,
            (x - 40, y - text_height - 40),
            (x + text_width + 40, y + 40),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            text,
            (x, y),
            font,
            scale,
            (255, 255, 255),
            thickness
        )

    def capture_array(self):
        frame = np.zeros(
            (self.height, self.width, 3),
            dtype=np.uint8
        )

        # Test pattern color bars
        bars = [
            (255, 255, 255),
            (255, 255, 0),
            (0, 255, 255),
            (0, 255, 0),
            (255, 0, 255),
            (255, 0, 0),
            (0, 0, 255),
        ]

        bar_width = self.width // len(bars)

        for i, color in enumerate(bars):
            frame[:, i * bar_width:(i + 1) * bar_width] = color

        # Generate SMPTE-style timecode

        elapsed = int(time.time() - self.start_time)

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        frames = self.frames % self.fps

        tc = f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

        # Main status message
        self.draw_centered_text(
            frame,
            "NO SOURCE FOUND",
            (self.height // 2) - 40,
            scale=2
        )

        # Timecode
        self.draw_centered_text(
            frame,
            tc,
            (self.height // 2) + 120,
            scale=2
        )

        # Small bottom label
        self.draw_centered_text(
            frame,
            "GORILLA CONTROL",
            self.height - 50,
            scale=1
        )

        self.frames += 1

        return frame
