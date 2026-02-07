#!/usr/bin/env bash

set -euo pipefail

TARGET_IP=${1:-172.20.0.40}
SEQUENCE=${2:-"1234,5677,9012"}
PROTECTED_PORT=${3:-9000}  # updated port

echo "[1/5] Attempting protected port before knocking"
nc -zv -n -w 2 "$TARGET_IP" "$PROTECTED_PORT" || true


echo "[2/5] Sending wrong knock sequence: $SEQUENCE"
python3 knock_client.py --target "$TARGET_IP" --sequence "$SEQUENCE" --check --protected-port "$PROTECTED_PORT"

echo "[3/5] Attempting protected port with bad knock"
nc -zv -n -w 2 "$TARGET_IP" "$PROTECTED_PORT" || true
SEQUENCE=${2:-"1234,5678,9012"}

echo "[4/5] Sending correct knock sequence: $SEQUENCE"
python3 knock_client.py --target "$TARGET_IP" --sequence "$SEQUENCE" --check --protected-port "$PROTECTED_PORT"

echo "[5/5] Attempting protected port after correct knocking"
nc -zv -n -w 2 "$TARGET_IP" "$PROTECTED_PORT" || true
