# decoy_traffic.py

import socket

def send_decoy_traffic(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    decoy_message = b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n"
    sock.sendto(decoy_message, (target_ip, target_port))
    sock.close()
