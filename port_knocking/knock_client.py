#!/usr/bin/env python3
"""Port knocking client (UDP)."""

import argparse
import socket
import time

DEFAULT_KNOCK_SEQUENCE = [1234, 5678, 9012]
DEFAULT_PROTECTED_PORT = 9000
DEFAULT_DELAY = 0.3


def send_knock(target, port, delay):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"knock", (target, port))
        sock.close()
    except OSError:
        pass
    time.sleep(delay)


def perform_knock_sequence(target, sequence, delay):
    for port in sequence:
        print(f"[+] Knocking on {port}")
        send_knock(target, port, delay)


def check_protected_port(target, protected_port):
    try:
        with socket.create_connection((target, protected_port), timeout=2.0):
            print(f"[+] Connected to protected port {protected_port}")
    except OSError:
        print(f"[-] Could not connect to protected port {protected_port}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument(
        "--sequence",
        default=",".join(str(p) for p in DEFAULT_KNOCK_SEQUENCE),
    )
    parser.add_argument(
        "--protected-port",
        type=int,
        default=DEFAULT_PROTECTED_PORT,
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
    )
    parser.add_argument(
        "--check",
        action="store_true",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        sequence = [int(p) for p in args.sequence.split(",")]
    except ValueError:
        raise SystemExit("Invalid sequence format.")

    perform_knock_sequence(args.target, sequence, args.delay)

    if args.check:
        check_protected_port(args.target, args.protected_port)


if __name__ == "__main__":
    main()
