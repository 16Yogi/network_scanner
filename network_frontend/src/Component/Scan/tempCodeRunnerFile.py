import subprocess
import asyncio
import socket
import threading
from typing import List, Tuple
from bleak import BleakScanner

# === 1. Scan Available Wi-Fi Networks ===
def scan_wifi_networks() -> List[str]:
    try:
        output = subprocess.check_output(
            "netsh wlan show networks mode=bssid",
            shell=True,
            encoding="utf-8",
            errors="ignore"
        )
        ssids = []
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
                if ssid and ssid not in ssids:
                    ssids.append(ssid)
        return ssids
    except Exception as e:
        print(f"Error scanning Wi-Fi: {e}")
        return []

# === 2. Multithreaded Ping Sweep ===
def ping_host(ip: str, live_hosts: List[str], lock: threading.Lock):
    result = subprocess.run(
        ['ping', '-n', '1', '-w', '100', ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if "TTL=" in result.stdout:
        with lock:
            live_hosts.append(ip)

def ping_sweep(network_prefix: str = "192.168.1.") -> List[str]:
    live_hosts = []
    threads = []
    lock = threading.Lock()
    print(f"\n📡 Scanning network {network_prefix}0/24 for live hosts...")
    for i in range(1, 255):
        ip = f"{network_prefix}{i}"
        t = threading.Thread(target=ping_host, args=(ip, live_hosts, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return live_hosts

# === 3. Multithreaded Port Scanner ===
def scan_single_port(ip: str, port: int, open_ports: List[int], lock: threading.Lock):
    try:
        with socket.create_connection((ip, port), timeout=0.5):
            with lock:
                open_ports.append(port)
    except:
        pass

def scan_ports(ip: str, ports: List[int]) -> List[int]:
    open_ports = []
    threads = []
    lock = threading.Lock()
    for port in ports:
        t = threading.Thread(target=scan_single_port, args=(ip, port, open_ports, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return open_ports

# === 4. Bluetooth Scanner ===
async def scan_bluetooth_devices() -> List[Tuple[str, str]]:
    print("\n🔍 Scanning for Bluetooth devices nearby...")
    devices = await BleakScanner.discover(timeout=5.0)
    return [(d.name or "Unknown", d.address) for d in devices]

# === 5. Parse Pi-hole Log File ===
def parse_pihole_logs(log_file_path: str) -> dict:
    domain_map = {}
    try:
        with open(log_file_path, "r") as f:
            for line in f:
                if "query" in line and "A " in line:  # basic DNS query filtering
                    parts = line.strip().split()
                    if len(parts) >= 6:
                        client = parts[3]
                        domain = parts[5]
                        domain_map.setdefault(client, []).append(domain)
    except Exception as e:
        print(f"❌ Error reading Pi-hole log: {e}")
    return domain_map

# === MAIN ===
if __name__ == "__main__":
    # 1. Wi-Fi Networks
    print("📶 Scanning for available Wi-Fi networks...")
    wifi_networks = scan_wifi_networks()
    if wifi_networks:
        print("✅ Wi-Fi Networks Found:")
        for ssid in wifi_networks:
            print(f" - {ssid}")
    else:
        print("❌ No Wi-Fi networks found.")

    # 2. Live Hosts
    network_prefix = "192.168.1."  # Adjust if needed
    live_hosts = ping_sweep(network_prefix)
    if live_hosts:
        print("\n✅ Live hosts found:")
        for host in live_hosts:
            print(f" - {host}")
    else:
        print("❌ No live hosts found.")

    # 3. Port Scanning
    common_ports = [21, 22, 23, 80, 443, 8080]
    print("\n🔓 Scanning common ports on live hosts...")
    for host in live_hosts:
        open_ports = scan_ports(host, common_ports)
        if open_ports:
            print(f"📍 Open ports on {host}: {', '.join(map(str, open_ports))}")
        else:
            print(f"📍 No open ports found on {host}.")

    # 4. Bluetooth
    bt_devices = asyncio.run(scan_bluetooth_devices())
    if bt_devices:
        print("\n✅ Bluetooth devices found:")
        for name, mac in bt_devices:
            print(f" - Name: {name}, MAC: {mac}")
    else:
        print("❌ No Bluetooth devices found.")

    # 5. Website Access via Pi-hole Logs
    print("\n🌐 Checking what websites devices accessed (Pi-hole log)...")
    pihole_log_path = "C:/Users/yogendra_m.DEEPIJATEL/Desktop/Data/pihole.log"
    dns_map = parse_pihole_logs(pihole_log_path)
    if dns_map:
        for ip in live_hosts:
            domains = dns_map.get(ip, [])
            if domains:
                print(f"🔗 {ip} visited domains: {', '.join(set(domains))}")
            else:
                print(f"🔍 No domains logged for {ip}")
    else:
        print("❌ No DNS log data found.")
