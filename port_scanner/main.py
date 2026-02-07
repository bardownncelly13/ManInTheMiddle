#!/usr/bin/env python3
"""
Port Scanner - Starter Template for Students
Assignment 2: Network Security

This is a STARTER TEMPLATE to help you get started.
You should expand and improve upon this basic implementation.

TODO for students:
1. Implement multi-threading for faster scans
2. Add banner grabbing to detect services
3. Add support for CIDR notation (e.g., 192.168.1.0/24)
4. Add different scan types (SYN scan, UDP scan, etc.)
5. Add output formatting (JSON, CSV, etc.)
6. Implement timeout and error handling
7. Add progress indicators
8. Add service fingerprinting
"""
import socket
import argparse
import time
from datetime import datetime
import concurrent.futures
import ipaddress

def scan_port(target, port, timeout=1.0):
    """
    Scan a single port on the target host
    Returns: (state, banner, elapsed)
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    banner = None
    start = time.time()
    try:
        s.connect((target, port))
        state = 'open'
        try:
            s.sendall(b'\r\n')
            banner = s.recv(128)
            if banner:
                banner = banner.decode(errors='replace').strip()
        except Exception:
            banner = None
    except (ConnectionRefusedError, OSError):
        state = 'closed'
    except socket.timeout:
        state = 'filtered'
    finally:
        s.close()
    elapsed = time.time() - start
    return state, banner, elapsed

def parse_ports(port_str):
    """Parse port arguments like '80,443,1000-1010' into list of ints"""
    result = set()
    for part in port_str.split(','):
        if '-' in part:
            a, b = part.split('-')
            for p in range(int(a), int(b)+1):
                result.add(p)
        else:
            result.add(int(part))
    return sorted(list(result))

def scan_range(target, ports, timeout=1.0, max_workers=100):
    results = []
    print(f"[*] Scanning {target} from port {ports[0]} to {ports[-1]} using {max_workers} threads")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, target, port, timeout): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                state, banner, elapsed = future.result()
            except Exception as exc:
                state, banner, elapsed = 'error', None, 0
            results.append({'port': port, 'state': state, 'banner': banner, 'time': elapsed})
    return results

def main():
    parser = argparse.ArgumentParser(description="Basic Port Scanner")
    parser.add_argument("--target", required=True, help="Target IP address, hostname, or subnet")
    parser.add_argument("--ports", default="1-10000", help="Port(s) to scan, e.g., 1-1000 or 22,80,443")
    parser.add_argument("--timeout", type=float, default=.2, help="Connection timeout (sec)")
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent scan threads")
    args = parser.parse_args()

    targets = []
    if "/" in args.target:
        try:
            net = ipaddress.ip_network(args.target, strict=False)
            targets = [str(h) for h in net.hosts()]
        except Exception as e:
            print(f"[-] Invalid subnet: {args.target} ({e})")
            return
    else:
        try:
            socket.gethostbyname(args.target)
            targets = [args.target]
        except socket.gaierror:
            print(f"[-] Invalid target: {args.target}")
            return

    ports = parse_ports(args.ports)
    all_open = []

    for tgt in targets:
        print(f"[*] Starting scan of {tgt} at {datetime.now()}")
        results = scan_range(tgt, ports, timeout=args.timeout, max_workers=args.threads)
        print(f"\n[+] SUMMARY for {tgt}:")
        for r in results:
            if r['state'] == 'open':
                print(f"Port {r['port']:5} OPEN   Banner: {r['banner']}")
                all_open.append({'host': tgt, 'port': r['port'], 'banner': r['banner']})
        print(f"Done at {datetime.now()}")

    print("\n" + "="*60)
    print("      FINAL CONDENSED SUMMARY OF ALL OPEN PORTS")
    print("="*60)
    if all_open:
        for entry in all_open:
            print(f"{entry['host']:15}  Port {entry['port']:5}  Banner: {entry['banner']}")
    else:
        print("No open ports found on any scanned hosts.")
    print("="*60)

if __name__ == "__main__":
    main()