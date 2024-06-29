# http_request.py

import random
import logging

class HttpRequestGenerator:
    def __init__(self, target_ip, header):
        self.target_ip = target_ip
        self.headers = header
        self.user_agents = self.load_user_agents()

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

    def get_random_headers(self):
        return "\r\n".join(self.headers)

    def create_http_request(self):
        user_agent = self.get_random_user_agent()
        headers = self.get_random_headers()
       # path = random.choice(["/", "/index.html", "/home", "/login", "/dashboard", "/register", "/account", "/profile"])
        path = random.choice(["/mobile/index.php"])
        http_request = f"GET {path} HTTP/1.1\r\nHost: {self.target_ip}\r\nUser-Agent: {user_agent}\r\n{headers}\r\n\r\n"
        return http_request
