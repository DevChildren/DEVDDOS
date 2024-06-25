# ip_rotation.py

import random

def generate_multiple_ips(count=10):
    ips = []
    for _ in range(count):
        ip_parts = [random.randint(0, 255) for _ in range(4)]
        ip_address = ".".join(map(str, ip_parts))
        if validate_ip(ip_address):
            ips.append(ip_address)
    return ips

def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True
