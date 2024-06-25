# interval_timing.py

import random

def get_dynamic_interval(min_interval=0.01, max_interval=0.1):
    return random.uniform(min_interval, max_interval)
