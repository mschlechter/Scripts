#!/bin/bash

VOLUME_GROUP="/dev/main-vg"
VOLUME_NAME="$VOLUME_GROUP/root"

SNAPSHOT_NAME="snap"
SNAPSHOT_VOLUME_NAME="$VOLUME_GROUP/$SNAPSHOT_NAME"
SNAPSHOT_MOUNT_POINT="/mnt/snap"
SNAPSHOT_SIZE="1024M"

LVCREATE=$(which lvcreate)
LVREMOVE=$(which lvremove)
LVDISPLAY=$(which lvdisplay)
MOUNT=$(which mount)
UMOUNT=$(which umount)
TAR=$(which tar)
MOUNTPOINT=$(which mountpoint)

function log
{
	echo "$(date +"%Y%m%d %H:%M:%S") $1"
}

function die
{
	log "$1"
	cleanup
	exit 1
}

function cleanup
{
	# Unmount snapshot filesystem (when mounted)
	if $MOUNTPOINT -q $SNAPSHOT_MOUNT_POINT; then
		log "Unmounting the snapshot"
		$UMOUNT $SNAPSHOT_VOLUME_NAME \
			|| log "Unmounting snapshot failed."
	fi

	# Remove snapshot volume (when it exists)
	if $LVDISPLAY | grep -q $SNAPSHOT_VOLUME_NAME; then
		log "Removing snapshot for volume $VOLUME_NAME"
		$LVREMOVE -f $VOLUME_NAME \
			|| log "Removing snapshot failed."
	fi
}

# Create the snapshot volume
log "Creating snapshot for volume $VOLUME_NAME"
$LVCREATE -L $SNAPSHOT_SIZE -s -n $SNAPSHOT_NAME $VOLUME_NAME \
	|| die "Snapshot creation failed."

# Mount the snapshot
log "Mounting snapshot on $SNAPSHOT_MOUNT_POINT"
$MOUNT $SNAPSHOT_VOLUME_NAME $SNAPSHOT_MOUNT_POINT -o ro \
	|| die "Mounting snapshot failed."

# Perform cleanup
cleanup




