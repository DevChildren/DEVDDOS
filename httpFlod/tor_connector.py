#tor_connector.py
import requests
import socket

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

def new_tor_identity():
    with socket.create_connection(('localhost', 9051)) as s:
        s.sendall(b'AUTHENTICATE "your_password"\r\n')
        response = s.recv(1024)
        if b'250 OK' not in response:
            raise Exception("Tor authentication failed")
        
        s.sendall(b'SIGNAL NEWNYM\r\n')
        response = s.recv(1024)
        if b'250 OK' not in response:
            raise Exception("Failed to obtain new Tor identity")
