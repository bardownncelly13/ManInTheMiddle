I changed to test on prot 9000 instead of 2222

make sure to docker compose up --build before testing

## to test just do ./demo.sh which will 
    1. test without knocking (server drops so it times out)
    2. test with wrong knocks (server drops so it times out)
    3. test with correct knocks (server responds with port open)

# Port Knocking Server

This server protects a TCP service (default: port 9000) using a UDP port knocking sequence.

## How It Works

- The protected port is blocked using iptables (DROP rule).
- The server listens for a specific UDP knock sequence.
- If the correct sequence is received within the time window:
  - An iptables ACCEPT rule is inserted for that client IP.
  - The port is opened temporarily (default: 30 seconds).
- After the timer expires, access is removed.

## Default Settings

- Knock sequence: 1234, 5678, 9012
- Protected port: 9000
- Sequence window: 10 seconds
- Open duration: 30 seconds

## Run

Inside the container: auto starts on lauch

```bash
python3 knock_server.py
##############################
# Port Knocking Client

This client sends a UDP knock sequence to unlock a protected TCP port.

## How It Works

- Sends UDP packets to each port in the specified sequence.
- Optionally checks if the protected port is open after knocking.

## Default Settings

- Knock sequence: 1234, 5678, 9012
- Delay between knocks: 0.3 seconds
- Protected port (for check): 9000

## Usage

Basic knock:

```bash
python3 knock_client.py --target 172.20.0.40