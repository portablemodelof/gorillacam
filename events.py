import time


class Events:
    def __init__(self, logger=None):
        self.message = None
        self.until = 0
        self.logger = logger

    def post(self, message, seconds=2.0):
        self.message = message
        self.until = time.time() + seconds

        if self.logger:
            self.logger.write(message)

    def current(self):
        if self.message and time.time() < self.until:
            return self.message
        return None
