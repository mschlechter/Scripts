#!/usr/bin/env python3
#
# Really simple firewall script with support for dynamic ip's
#
# Schedule this to run every night

import socket

# Configuration

ALLOWED_HOSTNAMES = ["autotaal.mooo.com"]
ALLOWED_ADDRESSES = ["192.168.2.0/24"]
OPEN_PORTS = [22,80,3000]

# End of configuration

all_ips = []

for hostname in ALLOWED_HOSTNAMES:
    ips = socket.gethostbyname_ex(hostname)[2]
    for ip in ips:
        all_ips.append(ip)

for ip in ALLOWED_ADDRESSES:
    all_ips.append(ip)

print (all_ips)

# todo : build firewall rules
# http://rdstash.blogspot.nl/2013/09/allow-host-with-dynamic-ip-through.html
# create chain and add it to the input filter