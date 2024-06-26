#tor_integartion.py

import requests

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

def check_tor_connection():
    session = get_tor_session()
    try:
        response = session.get("http://httpbin.org/ip")
        if response.status_code == 200:
            print("Tor connection established. Your IP is:", response.json())
            return True
        else:
            print(f"Failed to establish Tor connection. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return False
