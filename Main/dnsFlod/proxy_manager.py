# proxy_manager.py

import random

def get_random_proxy():
    proxy_list = [
        "http://123.456.789.012:8080",
        "http://234.567.890.123:8080"
        # Tambahkan lebih banyak proxy sesuai kebutuhan
    ]
    proxy = random.choice(proxy_list)
    return {"http": proxy, "https": proxy}

def check_proxy(proxy):
    try:
        response = requests.get("http://www.google.com", proxies=proxy, timeout=5)
        if response.status_code == 200:
            return True
    except:
        return False
    return False
