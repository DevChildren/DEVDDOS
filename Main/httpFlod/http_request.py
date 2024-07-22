import random
import logging
import requests
from bs4 import BeautifulSoup

class HttpRequestGenerator:
    def __init__(self, target_ip, headers):
        self.target_ip = target_ip
        self.user_agents = self.load_user_agents()
        self.paths = set()  # Untuk menyimpan path yang ditemukan

    def load_user_agents(self):
        try:
            with open('user-agents.txt', 'r') as f:
                user_agents = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) seperti Gecko",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, seperti Gecko) Version/9.1.2 Safari/601.7.7",
            ]
            logging.info("File user-agents.txt not found. Using default user agents.")
        return user_agents

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def crawl_paths(self, start_url):
        try:
            response = requests.get(start_url, headers={'User-Agent': self.get_random_user_agent()})
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for link in soup.find_all('a', href=True):
                    path = link['href']
                    if path.startswith('/') and path not in self.paths:
                        self.paths.add(path)
                        full_url = f"http://{self.target_ip}{path}"
                        # Rekursi untuk menemukan lebih banyak path
                        self.crawl_paths(full_url)
        except Exception as e:
            logging.error(f"Failed to crawl {start_url}: {e}")

    def create_http_request(self):
        if not self.paths:
            # Jika belum ada path, mulai dengan crawling
            self.crawl_paths(f"http://{self.target_ip}")
        # Pilih path secara acak dari yang ditemukan
        path = random.choice(list(self.paths)) if self.paths else "/"
        user_agent = self.get_random_user_agent()
        http_request = f"GET {path} HTTP/1.1\r\nHost: {self.target_ip}\r\nUser-Agent: {user_agent}\r\n\r\n"
        return http_request

# Contoh penggunaan
# if __name__ == "__main__":
#     target_ip = "example.com"  # Ganti dengan IP target atau domain
#     generator = HttpRequestGenerator(target_ip)
#     request = generator.create_http_request()
#     print(request)
# 