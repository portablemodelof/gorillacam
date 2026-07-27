#!/usr/bin/env python3

import time
import pygame

from settings import load_state
from camera import Camera
from storage import Storage
from recorder import Recorder
from ui import UI
from controls import Controls
from events import Events
from logger import Logger
from boot import BootManager
from diagnostics import Diagnostics

def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    w, h = screen.get_size()

    logger = Logger()
    events = Events(logger)
    boot = BootManager(events)

    boot_lines = []

    def boot_step(label, func):
        boot_lines.append(f"{label}...")
        placeholder_state = {"recording": False, "streaming": False}
        placeholder_recorder = type("RecorderPlaceholder", (), {"timer": lambda self: "00:00:00"})()
        placeholder_storage = type(
            "StoragePlaceholder",
            (),
            {"label": lambda self: "-", "free_gb": lambda self: 0.0},
        )()
        temp_ui = UI(screen, placeholder_state, placeholder_recorder, placeholder_storage, events)
        temp_ui.splash(boot_lines)

        result = boot.step(label, func)

        boot_lines[-1] = f"✓ {label}"
        temp_ui.splash(boot_lines)
        time.sleep(0.25)
        return result

    state = boot_step("Loading Settings", load_state)

    camera = Camera(state)
    storage = Storage()
    diagnostics = Diagnostics(state, storage)
    recorder = Recorder(state, camera, storage, events)
    ui = UI(screen, state, recorder, storage, events, diagnostics)
    controls = Controls(state, camera, recorder, (w, h), events)

    boot_step("Detecting Storage", storage.active_dir)
    boot_step("Starting Camera", camera.start)

    boot_lines.append("Ready")
    ui.splash(boot_lines)
    time.sleep(0.6)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                result = controls.handle_key(event.key)
                if result == "QUIT":
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                controls.handle_touch(*event.pos)

        frame = camera.capture_frame()
        surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        surface = pygame.transform.scale(surface, (w, h))

        screen.blit(surface, (0, 0))

        picker_options = (
            controls.options_for(controls.picker_key)
            if controls.picker_key
            else []
        )

        ui.draw(controls.ui_mode, controls.picker_key, picker_options)
        pygame.display.flip()

    events.post("Shutting Down")

    if state["recording"]:
        recorder.stop()

    camera.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
