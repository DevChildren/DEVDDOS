import socket
import logging

class SocketManager:
    def __init__(self):
        self.sock = None

    def connect(self, target_ip, target_port):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((target_ip, target_port))
            logging.info(f"Connected to {target_ip}:{target_port}")
        except socket.error as e:
            logging.error(f"Socket error during connection: {e}")
            self.sock = None

    def send(self, data):
        if self.sock:
            try:
                self.sock.sendall(data.encode())
                logging.info("Data sent successfully")
            except socket.error as e:
                logging.error(f"Socket error during sending: {e}")
                self.close()

    def close(self):
        if self.sock:
            try:
                self.sock.close()
                logging.info("Socket closed successfully")
            except socket.error as e:
                logging.error(f"Error closing socket: {e}")
            finally:
                self.sock = None
