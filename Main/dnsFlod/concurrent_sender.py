# concurrent_sender.py

import threading
import time

def start_concurrent_sending(target_function, args=(), num_threads=10):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=target_function, args=args)
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
