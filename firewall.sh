#!/bin/bash -

#
# Simple firewall script
#

# NOTE: Make sure you disable your Linux distribution's firewall first, before using this one.

IPT=$(which iptables)
LOCAL_SUBNET="192.168.2.0/24"

function reset()
{
	echo "Clearing firewall..."

	# Flush all rules
	$IPT -F
	$IPT -X
	$IPT -t nat -F
	$IPT -t nat -X
	$IPT -t mangle -F
	$IPT -t mangle -X
	
	# Allow everything
	$IPT -P INPUT ACCEPT
	$IPT -P OUTPUT ACCEPT
	$IPT -P FORWARD ACCEPT
}

function start()
{
	reset
	echo "Starting firewall..."

	# Set default policies
	$IPT -P INPUT DROP
	$IPT -P FORWARD DROP
	$IPT -P OUTPUT ACCEPT

	# Accept incoming packets for existing connections
	$IPT -A INPUT -m state --state ESTABLISHED -j ACCEPT

	# Allow SSH from local subnet
	$IPT -A INPUT -s $LOCAL_SUBNET -m state --state NEW -p tcp --dport 22 -j ACCEPT

	# Allow Cockpit from local subnet
	$IPT -A INPUT -s $LOCAL_SUBNET -m state --state NEW -p tcp --dport 9090 -j ACCEPT

	# Allow GO Git Service from local subnet
	$IPT -A INPUT -s $LOCAL_SUBNET -m state --state NEW -p tcp --dport 3000 -j ACCEPT

}

function status()
{
	# Display status
	$IPT -L -n -v
}

# Check arguments
if [ $# -ne 1 ]; then
	echo "Please specify action. Possible options are start, reset and status."
	exit 0
fi

if [ "$1" == "start" ]; then
	start
	exit 0
fi

if [ "$1" == "reset" ]; then
	reset
	exit 0
fi

if [ "$1" == "status" ]; then
	status
	exit 0
fi

