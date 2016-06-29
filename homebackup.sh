#!/bin/bash

VOLUME_GROUP="/dev/main-vg"
LOGICAL_VOLUME="root"
VOLUME_NAME="$VOLUME_GROUP/$LOGICAL_VOLUME"

SNAPSHOT_NAME="snap"
SNAPSHOT_MOUNT_POINT="/mnt/snap"
SNAPSHOT_SIZE="1024M"

LVCREATE=$(which lvcreate)
LVREMOVE=$(which lvremove)
MOUNT=$(which mount)
UMOUNT=$(which umount)
TAR=$(which tar)

function log
{
	echo "$(date +"%Y%m%d %H:%M:%S") $1"
}

function die
{
	log "$1"
	exit 1
}

# Create the snapshot volume
log "Creating snapshot for volume $VOLUME_NAME"
$LVCREATE -L $SNAPSHOT_SIZE -s -n $SNAPSHOT_NAME $VOLUME_NAME &> /dev/null
if [ $? -ne 0 ]; then die "Snapshot creation failed."; fi



# Remove the snapshot
log "Removing snapshot for volume $VOLUME_NAME"
$LVREMOVE -f $VOLUME_NAME &> /dev/null
if [ $? -ne 0 ]; then die "Removing snapshot failed."; fi

