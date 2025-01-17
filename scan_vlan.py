import subprocess
import concurrent.futures

def ping_ip(ip):
    """Pings an IP address and checks if it's online"""
    try:
        output = subprocess.run(["ping", "-c", "1", "-W", "1", ip], stdout=subprocess.DEVNULL)
        if output.returncode == 0:
            return ip
    except Exception:
        pass
    return None

def scan_subnet(subnet):
    """Scans all IPs in a /24 subnet"""
    network_prefix = ".".join(subnet.split(".")[:3])  # Extracts `10.8.11`
    active_hosts = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_ip, f"{network_prefix}.{i}"): i for i in range(1, 255)}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                active_hosts.append(result)
    
    return active_hosts

if __name__ == "__main__":
    subnet = "10.8.11.0/24"  # Subnetul mașinii tale
    print(f"Scanning subnet: {subnet}")
    active_ips = scan_subnet(subnet)
    
    print("Active hosts in VLAN:")
    for ip in active_ips:
        print(ip)
