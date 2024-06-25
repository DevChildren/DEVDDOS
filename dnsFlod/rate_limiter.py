# rate_limiter.py

import time

class AdaptiveRateLimiter:
    def __init__(self, initial_rate=0.1, min_rate=0.01, max_rate=1.0):
        self.current_rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
    
    def adjust_rate(self, success=True):
        if success:
            self.current_rate = max(self.min_rate, self.current_rate * 0.9)
        else:
            self.current_rate = min(self.max_rate, self.current_rate * 1.1)
    
    def sleep(self):
        time.sleep(self.current_rate)
