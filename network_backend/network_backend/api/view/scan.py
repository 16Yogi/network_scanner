import subprocess
import asyncio
import socket
import threading
from typing import List, Tuple
from bleak import BleakScanner
from rest_framework.decorators import api_view
from rest_framework.response import Response

# === 1. Wi-Fi Scanner ===
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
        return [f"Error scanning Wi-Fi: {e}"]

# === 2. Ping Sweep ===
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
    for i in range(1, 255):
        ip = f"{network_prefix}{i}"
        t = threading.Thread(target=ping_host, args=(ip, live_hosts, lock))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return live_hosts

# === 3. Port Scanner ===
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
    try:
        devices = await BleakScanner.discover(timeout=5.0)
        return [(d.name or "Unknown", d.address) for d in devices]
    except Exception as e:
        return [("Bluetooth error", str(e))]

# === 5. Saved Wi-Fi Passwords ===
def get_saved_wifi_passwords() -> List[Tuple[str, str]]:
    wifi_list = []
    try:
        profiles_output = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'],
            encoding='utf-8'
        )
        profiles = []
        for line in profiles_output.splitlines():
            if "All User Profile" in line:
                profile_name = line.split(":", 1)[1].strip()
                profiles.append(profile_name)

        for profile in profiles:
            try:
                details_output = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                    encoding='utf-8',
                    stderr=subprocess.DEVNULL
                )
                password = None
                for detail_line in details_output.splitlines():
                    if "Key Content" in detail_line:
                        password = detail_line.split(":", 1)[1].strip()
                        break
                wifi_list.append((profile, password if password else "(No password found)"))
            except subprocess.CalledProcessError:
                wifi_list.append((profile, "(Access denied)"))

    except Exception as e:
        return [(f"Error: {str(e)}", "")]
    return wifi_list

# === Django API View ===
@api_view(['GET'])
def network_scan(request):
    result = {}
    threads = []
    lock = threading.Lock()

    # Tasks for major scans
    def wifi_task():
        result['wifi_networks'] = scan_wifi_networks()

    def hosts_task():
        result['live_hosts'] = ping_sweep()

    def bluetooth_task():
        result['bluetooth_devices'] = asyncio.run(scan_bluetooth_devices())

    def wifi_passwords_task():
        result['saved_wifi_passwords'] = get_saved_wifi_passwords()

    # Launch parallel tasks
    threads.append(threading.Thread(target=wifi_task))
    threads.append(threading.Thread(target=hosts_task))
    threads.append(threading.Thread(target=bluetooth_task))
    threads.append(threading.Thread(target=wifi_passwords_task))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Port scan per live host (also in parallel)
    open_ports = {}

    def port_scan_task(ip):
        ports = scan_ports(ip, [21, 22, 23, 80, 443, 8080])
        with lock:
            open_ports[ip] = ports

    port_threads = []
    for ip in result.get("live_hosts", []):
        pt = threading.Thread(target=port_scan_task, args=(ip,))
        pt.start()
        port_threads.append(pt)

    for pt in port_threads:
        pt.join()

    result["open_ports"] = open_ports

    return Response(result)
