from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

class AttackManager:
    def __init__(self):
        self.active_attacks = []
        self.executor = ThreadPoolExecutor()

    def run_attack(self, attack, thread_count):
        logging.info(f"Starting attack with {thread_count} threads")
        self.active_attacks.append(attack)
        attack_futures = [self.executor.submit(attack.attack) for _ in range(thread_count)]
        self._handle_futures(attack_futures)
        self.active_attacks.remove(attack)

    def run_all_attacks(self, attacks, thread_count):
        logging.info(f"Starting all attacks with {thread_count} threads each")
        self.active_attacks.extend(attacks)
        all_futures = []
        for attack in attacks:
            all_futures.extend(self.executor.submit(attack.attack) for _ in range(thread_count))
        self._handle_futures(all_futures)
        self.active_attacks.clear()

    def shutdown(self):
        logging.info("Shutting down all attacks")
        for attack in self.active_attacks:
            attack.stop_attack()
        self.executor.shutdown(wait=False)

    def get_status(self):
        status = {}
        for attack in self.active_attacks:
            status[id(attack)] = {
                "target_ip": attack.target_ip,
                "target_port": attack.target_port,
                "is_running": attack.is_running,
            }
        return status

    def _handle_futures(self, futures):
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Attack error: {e}")
