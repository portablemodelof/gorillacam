import time
import pygame

from settings import FPS_OPTIONS, SHUTTER_OPTIONS, GAIN_OPTIONS, WB_OPTIONS


class Controls:
    def __init__(self, state, camera, recorder, screen_size):
        self.state = state
        self.camera = camera
        self.recorder = recorder
        self.w, self.h = screen_size

        self.ui_mode = "VIEWFINDER"
        self.picker_key = None

        self.last_tap_time = 0
        self.last_tap_pos = (0, 0)

    def options_for(self, key):
        return {
            "fps": FPS_OPTIONS,
            "shutter": SHUTTER_OPTIONS,
            "gain": GAIN_OPTIONS,
            "wb": WB_OPTIONS,
        }[key]

    def picker_position(self):
        positions = {
            "fps": (120, 118),
            "shutter": (120, 154),
            "gain": (120, 190),
            "wb": (120, 226),
        }
        return positions.get(self.picker_key, (120, 118))

    def show_controls(self):
        self.ui_mode = "CONTROL"
        self.picker_key = None

    def hide_controls(self):
        self.ui_mode = "VIEWFINDER"
        self.picker_key = None

    def open_picker(self, key):
        self.ui_mode = "PICKER"
        self.picker_key = key

    def close_picker(self):
        self.ui_mode = "CONTROL"
        self.picker_key = None

    def is_double_tap(self, x, y):
        now = time.time()
        double = (
            now - self.last_tap_time < 0.35
            and abs(x - self.last_tap_pos[0]) < 60
            and abs(y - self.last_tap_pos[1]) < 60
        )

        self.last_tap_time = now
        self.last_tap_pos = (x, y)
        return double

    def handle_picker_touch(self, x, y):
        if not self.picker_key:
            return

        options = self.options_for(self.picker_key)
        box_x, box_y = self.picker_position()
        row_h = 30
        box_w = 140

        for i, option in enumerate(options):
            row_y = box_y + 38 + i * row_h

            if box_x <= x <= box_x + box_w and row_y <= y <= row_y + row_h:
                self.state[self.picker_key] = option
                self.camera.apply_controls()
                return

        self.close_picker()

    def handle_touch(self, x, y):
        if self.is_double_tap(x, y):
            self.hide_controls()
            return

        if self.ui_mode == "PICKER":
            self.handle_picker_touch(x, y)
            return

        if x > self.w - 130 and y < 60:
            self.recorder.toggle()
            return

        if x > self.w - 130 and 60 <= y < 115:
            self.state["streaming"] = not self.state["streaming"]
            return

        if self.ui_mode == "VIEWFINDER":
            self.show_controls()
            return

        if self.ui_mode == "CONTROL":
            if 118 <= y < 154:
                self.open_picker("fps")
            elif 154 <= y < 190:
                self.open_picker("shutter")
            elif 190 <= y < 226:
                self.open_picker("gain")
            elif 226 <= y < 265:
                self.open_picker("wb")

    def handle_key(self, key):
        if key == pygame.K_r:
            self.recorder.toggle()
        elif key == pygame.K_e:
            self.state["streaming"] = not self.state["streaming"]
        elif key == pygame.K_h:
            if self.ui_mode == "VIEWFINDER":
                self.show_controls()
            else:
                self.hide_controls()
        elif key in (pygame.K_q, pygame.K_ESCAPE):
            return "QUIT"

        return None
