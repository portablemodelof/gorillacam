#!/usr/bin/env python3

import time
import pygame

from settings import DEFAULT_STATE
from camera import Camera
from storage import Storage
from recorder import Recorder
from ui import UI
from controls import Controls


def main():
    pygame.init()
    pygame.mouse.set_visible(False)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    w, h = screen.get_size()

    state = DEFAULT_STATE.copy()

    camera = Camera(state)
    storage = Storage()
    recorder = Recorder(state, camera, storage)
    ui = UI(screen, state, recorder, storage)
    controls = Controls(state, camera, recorder, (w, h))

    running = True

    ui.splash()
    time.sleep(1.2)

    camera.start()

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

    if state["recording"]:
        recorder.stop()

    camera.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
