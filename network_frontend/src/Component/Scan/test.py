import subprocess
import asyncio
import socket
from typing import List, Tuple
from bleak import BleakScanner


# --- 1. Scan Available Wi-Fi Networks ---
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


# --- 2. Ping Sweep for Live Hosts ---
def ping_sweep(network_prefix: str = "192.168.1.") -> List[str]:
    live_hosts = []
    print(f"\nScanning network {network_prefix}0/24 for live hosts...")
    for i in range(1, 255):
        ip = f"{network_prefix}{i}"
        result = subprocess.run(
            ['ping', '-n', '1', '-w', '100', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if "TTL=" in result.stdout:
            live_hosts.append(ip)
    return live_hosts


# --- 3. Port Scanner ---
def scan_ports(ip: str, ports: List[int]) -> List[int]:
    open_ports = []
    for port in ports:
        try:
            with socket.create_connection((ip, port), timeout=0.5):
                open_ports.append(port)
        except:
            pass
    return open_ports


# --- 4. Bluetooth Scanner ---
async def scan_bluetooth_devices() -> List[Tuple[str, str]]:
    print("\nScanning for Bluetooth devices nearby...")
    devices = await BleakScanner.discover(timeout=5.0)
    return [(d.name or "Unknown", d.address) for d in devices]


# --- MAIN ---
if __name__ == "__main__":
    # Wi-Fi Networks
    print("Scanning for available Wi-Fi networks...")
    wifi_networks = scan_wifi_networks()
    if wifi_networks:
        print("Wi-Fi Networks Found:")
        for ssid in wifi_networks:
            print(f" - {ssid}")
    else:
        print("No Wi-Fi networks found.")

    # Ping Sweep
    network_prefix = "192.168.1."  # Update based on your network
    live_hosts = ping_sweep(network_prefix)
    if live_hosts:
        print("\nLive hosts found:")
        for host in live_hosts:
            print(f" - {host}")
    else:
        print("No live hosts found.")

    # Port Scanning on live hosts
    common_ports = [21, 22, 23, 80, 443, 8080]
    for host in live_hosts:
        open_ports = scan_ports(host, common_ports)
        if open_ports:
            print(f"Open ports on {host}: {', '.join(map(str, open_ports))}")
        else:
            print(f"No open common ports found on {host}.")

    # Bluetooth
    bt_devices = asyncio.run(scan_bluetooth_devices())
    if bt_devices:
        print("\nBluetooth devices found:")
        for name, mac in bt_devices:
            print(f" - Name: {name}, MAC: {mac}")
    else:
        print("No Bluetooth devices found.")
