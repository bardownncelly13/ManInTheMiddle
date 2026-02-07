the scanner is run with ptyhon3 main.py
it has --target to specify the ip
-- ports 1-10000 or any range to specify the range of ports to scan
--timeout to specify the timeout on each port scanned 
--threads to specify the max number of threads 
I ran python3 main.py --target 172.20.0.0/27 to get the results shown below it uses default ports 1-1000 100 threads and .2 second timout 
results 

============================================================
      FINAL CONDENSED SUMMARY OF ALL OPEN PORTS
============================================================
172.20.0.1       Port  5001  Banner: b''
172.20.0.10      Port  5000  Banner: b''
172.20.0.11      Port  3306  Banner: J
z)+c6�����IL}i  ]]      zs)`mysql_native_password
172.20.0.20      Port  2222  Banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.13
Invalid SSH identification string.
172.20.0.21      Port  8888  Banner: b''
172.20.0.22      Port  6379  Banner: None
============================================================
I tried to ssh into the SSH port and found
FLAG{h1dd3n_s3rv1c3s_n33d_pr0t3ct10n} got by doing  ssh -p 2222 sshuser@172.20.0.20
then on http://172.20.0.21:8888
I tried to curl into it and got a auth error that I needed an api key 
when I did the man in the middle attack I found it and found the second flag 
FLAG{p0rt_kn0ck1ng_4nd_h0n3yp0ts_s4v3_th3_d4y}"


