class BootManager:
    def __init__(self, events):
        self.events = events
        self.steps = []

    def step(self, label, func=None):
        self.events.post(f"{label}...")

        try:
            result = func() if func else None
            self.steps.append((label, True))
            self.events.post(f"✓ {label}")
            return result

        except Exception as e:
            self.steps.append((label, False))
            self.events.post(f"✗ {label}")
            raise e
