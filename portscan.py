# A simple port scan build with Python
# The syntax of the script consists in command "python",
# the name of script "portscan.py" and the target, IP or Hostname
# Example of use: python portscan 127.0.0.1
import sys
import socket
for ports in range(1,65535):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((sys.argv[1], ports)) == 0:
        print("PORT", ports, "OPEN")
        s.close()
