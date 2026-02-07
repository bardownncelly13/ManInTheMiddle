# Honeypot Analysis
    makes a fake ssh port that asks for username and passowrd it logs
        Source IP address
        Source port
        Timestamp (UTC)
        Event type (connection, login_attempt, etc.)
        Username entered
        Password entered
        Connection duration
## Summary of Observed Attacks
Attacker sees 
nc localhost 2222    

SSH-2.0-OpenSSH_8.4p1 Ubuntu-5ubuntu1
login as: root
Password: root
Permission denied, please try again.

and it returns in logs  

{"timestamp": "2026-02-07T05:01:00.102665Z", "event": "login_attempt", "src_ip": "172.20.0.1", "src_port": 53612, "username": "root", "password": "root", "duration": 8.5}



## Recommendations

implement real SSH encryption
complete full SSH handshake
emulate full shell environment
implement IP blacklisting
