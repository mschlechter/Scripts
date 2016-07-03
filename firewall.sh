#!/bin/bash -

#
# Simple firewall script
#

IPT=$(which iptables)


function reset()
{
	echo "Clearing firewall..."

	$IPT -F
	$IPT -X
	$IPT -t nat -F
	$IPT -t nat -X
	$IPT -t mangle -F
	$IPT -t mangle -X
	



}

function start()
{
	reset
	echo "Starting firewall..."
}

function status()
{
	$IPT -L -n -v
}

# Check arguments
if [ $# -ne 1 ]; then
	echo "Please specify action. Possible options are start and reset."
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

