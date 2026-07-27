import time
import pygame

from settings import (
    MODE_OPTIONS,
    MODE_CONFIGS,
    FPS_OPTIONS,
    SHUTTER_OPTIONS,
    GAIN_OPTIONS,
    WB_OPTIONS,
    save_state,
)


class Controls:
    def __init__(self, state, camera, recorder, screen_size, events):
        self.state = state
        self.camera = camera
        self.recorder = recorder
        self.events = events
        self.w, self.h = screen_size

        self.ui_mode = "VIEWFINDER"  # VIEWFINDER, CONTROL, PICKER, DIAGNOSTICS
        self.picker_key = None

        self.last_tap_time = 0
        self.last_tap_pos = (0, 0)

    def options_for(self, key):
        return {
            "mode": MODE_OPTIONS,
            "fps": FPS_OPTIONS,
            "shutter": SHUTTER_OPTIONS,
            "gain": GAIN_OPTIONS,
            "wb": WB_OPTIONS,
        }[key]

    def picker_position(self):
        positions = {
            "mode": (120, 92),
            "fps": (120, 142),
            "shutter": (120, 192),
            "gain": (120, 242),
            "wb": (120, 292),
        }
        return positions.get(self.picker_key, (120, 142))

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

    def toggle_diagnostics(self):
        if self.ui_mode == "DIAGNOSTICS":
            self.ui_mode = "VIEWFINDER"
        else:
            self.ui_mode = "DIAGNOSTICS"
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
        box_w = 160

        for i, option in enumerate(options):
            row_y = box_y + 38 + i * row_h

            if box_x <= x <= box_x + box_w and row_y <= y <= row_y + row_h:
                self.state[self.picker_key] = option

                if self.picker_key == "mode":
                    self.events.post(f"Mode {option}")
                    save_state(self.state)
                    self.camera.restart_with_new_mode()
                else:
                    self.camera.apply_controls()
                    save_state(self.state)
                    self.events.post(f"{self.picker_key.upper()} {option}")

                return

        self.close_picker()

    def handle_touch(self, x, y):
        if self.ui_mode == "DIAGNOSTICS":
            self.ui_mode = "VIEWFINDER"
            return

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
            self.events.post("NET On" if self.state["streaming"] else "NET Off")
            return

        if self.ui_mode == "VIEWFINDER":
            self.show_controls()
            return

        if self.ui_mode == "CONTROL":
            if 90 <= y < 125:
                self.open_picker("mode")
            elif 140 <= y < 175:
                self.open_picker("fps")
            elif 190 <= y < 225:
                self.open_picker("shutter")
            elif 240 <= y < 275:
                self.open_picker("gain")
            elif 290 <= y < 325:
                self.open_picker("wb")

    def handle_key(self, key):
        if key == pygame.K_d:
            self.toggle_diagnostics()
            return None

        if key == pygame.K_r:
            self.recorder.toggle()
        elif key == pygame.K_e:
            self.state["streaming"] = not self.state["streaming"]
            self.events.post("NET On" if self.state["streaming"] else "NET Off")
        elif key == pygame.K_h:
            if self.ui_mode == "VIEWFINDER":
                self.show_controls()
            else:
                self.hide_controls()
        elif key in (pygame.K_q, pygame.K_ESCAPE):
            return "QUIT"

        return None
