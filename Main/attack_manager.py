from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class AttackManager:
    def __init__(self):
        self.active_attacks = []

    def run_attack(self, attack, thread_count):
        logging.info(f"Starting attack with {thread_count} threads")
        self.active_attacks.append(attack)  # Add attack to active list
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(attack.attack) for _ in range(thread_count)]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Attack error: {e}")
        self.active_attacks.remove(attack)  # Remove attack from active list after completion

    def run_all_attacks(self, attacks, thread_count):
        logging.info(f"Starting all attacks with {thread_count} threads each")
        self.active_attacks.extend(attacks)  # Add all attacks to active list
        with ThreadPoolExecutor(max_workers=len(attacks) * thread_count) as executor:
            futures = []
            for attack in attacks:
                futures.extend(executor.submit(attack.attack) for _ in range(thread_count))
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Attack error: {e}")
        for attack in attacks:
            self.active_attacks.remove(attack)  # Remove attacks from active list after completion

    def shutdown(self):
        logging.info("Shutting down all attacks")
        for attack in self.active_attacks:
            attack.stop_attack()

    def get_status(self):
        status = {}
        for attack in self.active_attacks:
            status[id(attack)] = {
                "target_ip": attack.target_ip,
                "target_port": attack.target_port,
                "is_running": attack.is_running,
            }
        return status
