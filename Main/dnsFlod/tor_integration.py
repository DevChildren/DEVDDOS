import requests
import logging
import random
from .user_agents import get_random_user_agent

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

user_agent = get_random_user_agent
if user_agent:
  USER_AGENTS = user_agent
else:
    USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
    # Add more user agents if needed
   ]

def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    session.headers.update({'User-Agent': random.choice(USER_AGENTS)})
    return session

def check_tor_connection():
    session = get_tor_session()
    try:
        response = session.get("http://httpbin.org/ip", timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        ip_info = response.json()
        
        if 'ip' in ip_info:
            logging.info("Tor connection established. Your IP is: %s", ip_info['ip'])
            return True
        else:
            logging.error("Unexpected response format: %s", ip_info)
    except requests.exceptions.RequestException as e:
        logging.error("An error occurred: %s", e)
    return False

if __name__ == "__main__":
    if check_tor_connection():
        logging.info("Connection check completed successfully.")
    else:
        logging.warning("Connection check failed.")
