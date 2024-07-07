import socket

def get_ip_addresses(domain):
    try:
        result = socket.getaddrinfo(domain, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        ip_addresses = set()
        for res in result:
            ip = res[4][0]
            ip_addresses.add(ip)
        return ip_addresses
    except socket.gaierror:
        return None

def main():
    domain = input("Masukkan nama domain untuk diperiksa IP address: ")
    ip_addresses = get_ip_addresses(domain)
    
    if ip_addresses:
        print(f"IP addresses dari {domain} adalah:")
        for ip in ip_addresses:
            print(ip)
    else:
        print(f"Tidak dapat menemukan IP addresses untuk {domain}")

if __name__ == "__main__":
    main()
