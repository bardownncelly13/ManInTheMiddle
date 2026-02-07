#!/usr/bin/env python3

print("HONEYPOT FILE LOADED")

import socket
import logging
import os
import time
import json
from datetime import datetime
LOG_PATH = "/app/logs/honeypot.log"

def log_event(event_type, data):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event": event_type,
        **data
    }

    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
        


def run_honeypot():
    logger = logging.getLogger("Honeypot")

    HOST = "0.0.0.0"
    PORT = 22 

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    logger.info(f"Honeypot listening on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        start_time = time.time()

        src_ip, src_port = addr
        log_event("connection", {
            "src_ip": src_ip,
            "src_port": src_port
        })

        try:
            client.sendall(b"SSH-2.0-OpenSSH_8.4p1 Ubuntu-5ubuntu1\r\n")
            client.sendall(b"login as: ")
            username = client.recv(1024).strip().decode(errors="ignore")

            client.sendall(b"Password: ")
            password = client.recv(1024).strip().decode(errors="ignore")

            duration = time.time() - start_time

            log_event("login_attempt", {
                "src_ip": src_ip,
                "src_port": src_port,
                "username": username,
                "password": password,
                "duration": round(duration, 2)
            })


            client.sendall(b"Permission denied, please try again.\r\n")

        except Exception as e:
            logger.error(f"Error handling connection: {e}")

        finally:
            client.close()


if __name__ == "__main__":
   
    run_honeypot()
