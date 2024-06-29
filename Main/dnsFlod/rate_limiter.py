import time

class AdaptiveRateLimiter:
    def __init__(self, initial_rate):
        self.rate = initial_rate

    def sleep(self):
        time.sleep(self.rate)

    def adjust_rate(self, success):
        if success:
            self.rate = max(0.01, self.rate - 0.001)
        else:
            self.rate = min(0.1, self.rate + 0.001)
