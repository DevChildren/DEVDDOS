# socket_manager.py

import socket

class SocketManager:
    def __init__(self):
        self.sock = None

    def connect(self, target_ip, target_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        self.sock.connect((target_ip, target_port))

    def send(self, data):
        if self.sock:
            self.sock.sendall(data.encode())

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except socket.error as e:
                logging.error(f"Error closing socket: {e}")
            finally:
                self.sock = None
