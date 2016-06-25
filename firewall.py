#!/usr/bin/env python3

import socket


allowed_hostnames = ["autotaal.mooo.com"]
allowed_ipaddresses = ["192.168.3.0/24"]


all_ips = []

for hostname in allowed_hostnames:
    ips = socket.gethostbyname_ex(hostname)[2]
    for ip in ips:
        all_ips.append(ip)

for ip in allowed_ipaddresses:
    all_ips.append(ip)

print (all_ips)


# todo : build firewall rules
