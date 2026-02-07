#!/usr/bin/env python3
"""Port knocking server."""

import argparse
import logging
import socket
import time
import subprocess
import threading

DEFAULT_KNOCK_SEQUENCE = [1234, 5678, 9012]
DEFAULT_PROTECTED_PORT = 9000
DEFAULT_SEQUENCE_WINDOW = 10.0
OPEN_DURATION = 30
def setup_firewall(protected_port):
    subprocess.run([
        "iptables", "-A", "INPUT",
        "-m", "conntrack",
        "--ctstate", "ESTABLISHED,RELATED",
        "-j", "ACCEPT"
    ], check=False)

    subprocess.run([
        "iptables", "-A", "INPUT",
        "-p", "tcp",
        "--dport", str(protected_port),
        "-j", "DROP"
    ], check=True)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def open_protected_port(ip, protected_port):
    try:
        subprocess.run(
            ["iptables", "-I", "INPUT", "-p", "tcp",
             "--dport", str(protected_port),
             "-s", ip, "-j", "ACCEPT"],
            check=True
        )
        logging.info(f"Opened port {protected_port} for {ip}")
    except Exception as e:
        logging.error(f"Failed to open port: {e}")


def close_protected_port(ip, protected_port):
    try:
        subprocess.run(
            ["iptables", "-D", "INPUT", "-p", "tcp",
             "--dport", str(protected_port),
             "-s", ip, "-j", "ACCEPT"],
            check=True
        )
        logging.info(f"Closed port {protected_port} for {ip}")
    except Exception as e:
        logging.error(f"Failed to close port: {e}")


def listen_for_knocks(sequence, window_seconds, protected_port):
    logger = logging.getLogger("KnockServer")
    logger.info(f"Listening for knocks: {sequence}")
    logger.info(f"Protected port: {protected_port}")

    sockets = []
    for port in set(sequence):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))
        sock.setblocking(False)
        sockets.append(sock)

    ip_states = {}  # ip -> (step, last_time)

    while True:
        now = time.time()

        for s in sockets:
            try:
                data, addr = s.recvfrom(1024)
                ip = addr[0]
                port = s.getsockname()[1]

                # Reset if timeout exceeded
                if ip in ip_states:
                    step, last_time = ip_states[ip]
                    if now - last_time > window_seconds:
                        ip_states.pop(ip)
                        step = 0
                else:
                    step = 0

                expected_port = sequence[step]

                if port == expected_port:
                    step += 1
                    ip_states[ip] = (step, now)

                    if step == len(sequence):
                        logger.info(f"Valid sequence from {ip}")
                        open_protected_port(ip, protected_port)
                        ip_states.pop(ip, None)

                        threading.Timer(
                            OPEN_DURATION,
                            close_protected_port,
                            args=(ip, protected_port)
                        ).start()
                else:
                    ip_states.pop(ip, None)

            except BlockingIOError:
                pass

        time.sleep(0.05)


def parse_args():
    parser = argparse.ArgumentParser()
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
        "--window",
        type=float,
        default=DEFAULT_SEQUENCE_WINDOW,
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging()

    try:
        sequence = [int(p) for p in args.sequence.split(",")]
    except ValueError:
        raise SystemExit("Invalid sequence format.")
    setup_firewall(args.protected_port)
    listen_for_knocks(sequence, args.window, args.protected_port)


if __name__ == "__main__":
    main()
