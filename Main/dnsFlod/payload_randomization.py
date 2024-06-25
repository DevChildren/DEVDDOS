# payload_randomization.py

import random

def randomize_dns_payload(domain):
    packet = bytearray()
    transaction_id = random.randint(0, 65535)
    flags = random.choice([0x0100, 0x8180])  # Query or Response
    
    packet.extend(transaction_id.to_bytes(2, 'big'))
    packet.extend(flags.to_bytes(2, 'big'))
    packet.extend((1).to_bytes(2, 'big'))  # Questions
    packet.extend((0).to_bytes(2, 'big'))  # Answer RRs
    packet.extend((0).to_bytes(2, 'big'))  # Authority RRs
    packet.extend((0).to_bytes(2, 'big'))  # Additional RRs

    for part in domain.split('.'):
        packet.append(len(part))
        packet.extend(part.encode())

    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x01)  # Type A
    packet.append(0x00)
    packet.append(0x01)  # Class IN

    return packet
