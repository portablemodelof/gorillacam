import pygame

from settings import WHITE, GRAY, RED, GREEN, BLACK
from version import NAME, VERSION, BUILD


class UI:
    def __init__(self, screen, state, recorder, storage, events, diagnostics=None):
        self.screen = screen
        self.state = state
        self.recorder = recorder
        self.storage = storage
        self.events = events
        self.diagnostics = diagnostics
        self.w, self.h = self.screen.get_size()

        self.font = pygame.font.SysFont("Inter", 18)
        self.font_small = pygame.font.SysFont("Inter", 14)
        self.font_boot = pygame.font.SysFont("Inter", 22)

    def text(self, value, x, y, font=None, color=WHITE):
        font = font or self.font
        surface = font.render(str(value), True, color)
        self.screen.blit(surface, (x, y))

    def splash(self, lines=None):
        lines = lines or []
        self.screen.fill(BLACK)

        title = self.font_boot.render(NAME, True, WHITE)
        version = self.font_small.render(f"v{VERSION}  build {BUILD}", True, GRAY)

        self.screen.blit(title, title.get_rect(center=(self.w // 2, 90)))
        self.screen.blit(version, version.get_rect(center=(self.w // 2, 120)))

        y = 170
        for line in lines:
            color = WHITE if line.startswith("✓") else GRAY
            item = self.font.render(line, True, color)
            self.screen.blit(item, item.get_rect(center=(self.w // 2, y)))
            y += 34

        pygame.display.flip()

    def draw_status(self):
        x = self.w - 95
        rec_color = RED if self.state["recording"] else GRAY
        net_color = GREEN if self.state["streaming"] else GRAY

        self.text("● REC" if self.state["recording"] else "○ REC", x, 16, self.font, rec_color)

        if self.state["recording"]:
            self.text(self.recorder.timer(), x, 40, self.font_small, RED)

        self.text("● NET" if self.state["streaming"] else "○ NET", x, 68, self.font, net_color)

    def draw_controls(self):
        self.text("GC", 20, 52, self.font_small, GRAY)

        self.text("MODE", 20, 82, self.font_small, GRAY)
        self.text(self.state["mode"], 20, 102)

        self.text("FPS", 20, 132, self.font_small, GRAY)
        self.text(f'{self.state["fps"]}', 20, 152)

        self.text("SHUTTER", 20, 182, self.font_small, GRAY)
        self.text(self.state["shutter"], 20, 202)

        self.text("GAIN", 20, 232, self.font_small, GRAY)
        self.text(self.state["gain"], 20, 252)

        self.text("WB", 20, 282, self.font_small, GRAY)
        self.text(self.state["wb"], 20, 302)

        self.text("MEDIA", 20, self.h - 58, self.font_small, GRAY)
        self.text(
            f"{self.storage.label()}  {self.storage.free_gb():.1f}GB",
            20,
            self.h - 38,
            self.font_small,
            WHITE,
        )

    def picker_position(self, key):
        positions = {
            "mode": (120, 92),
            "fps": (120, 142),
            "shutter": (120, 192),
            "gain": (120, 242),
            "wb": (120, 292),
        }
        return positions.get(key, (120, 142))

    def draw_picker(self, picker_key, options):
        if not picker_key:
            return

        current = self.state[picker_key]
        box_x, box_y = self.picker_position(picker_key)
        box_w = 160
        row_h = 30
        box_h = 40 + len(options) * row_h

        panel = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 185))
        self.screen.blit(panel, (box_x, box_y))

        self.text(picker_key.upper(), box_x + 14, box_y + 10, self.font_small, GRAY)

        for i, option in enumerate(options):
            y = box_y + 38 + i * row_h
            selected = option == current
            mark = "●" if selected else "○"
            color = WHITE if selected else GRAY
            self.text(f"{mark} {option}", box_x + 14, y, self.font, color)

    def draw_notice(self):
        message = self.events.current()
        if not message:
            return

        surface = self.font.render(message, True, WHITE)
        pad_x = 18
        pad_y = 10
        rect = surface.get_rect(center=(self.w // 2, self.h - 70))

        bg = pygame.Surface((rect.width + pad_x * 2, rect.height + pad_y * 2), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 190))

        self.screen.blit(bg, (rect.x - pad_x, rect.y - pad_y))
        self.screen.blit(surface, rect)

    def draw_diagnostics(self):
        if not self.diagnostics:
            return

        panel = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 220))
        self.screen.blit(panel, (0, 0))

        self.text("DIAGNOSTICS", 30, 28, self.font, WHITE)

        y = 68

        for title, lines in self.diagnostics.sections():
            self.text(title, 30, y, self.font_small, GRAY)
            y += 22

            for line in lines:
                color = WHITE

                if line.startswith("CPU"):
                    try:
                        temp = float(line.replace("CPU", "").replace("°C", "").strip())
                        if temp >= 75:
                            color = RED
                    except Exception:
                        pass

                self.text(line, 48, y, self.font_small, color)
                y += 22

            y += 14

        self.text("Tap anywhere to close", 30, self.h - 34, self.font_small, GRAY)

    def draw(self, ui_mode, picker_key, picker_options):
        if ui_mode == "DIAGNOSTICS":
            self.draw_diagnostics()
            return

        self.draw_status()

        if ui_mode in ("CONTROL", "PICKER") or self.state["recording"]:
            self.draw_controls()

        if ui_mode == "PICKER":
            self.draw_picker(picker_key, picker_options)

        self.draw_notice()
        self.text("Q", 8, self.h - 22, self.font_small, GRAY)
