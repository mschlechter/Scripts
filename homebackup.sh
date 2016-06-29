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

# Create the snapshot volume
echo "Creating snapshot for volume $VOLUME_NAME"
$LVCREATE -L $SNAPSHOT_SIZE -s -n $SNAPSHOT_NAME $VOLUME_NAME &> /dev/null
if [ $? -ne 0 ];
then
	echo "Snapshot creation failed."
	exit 1
fi

# Remove the snapshot
echo "Removing snapshot for volume $VOLUME_NAME"
$LVREMOVE -f $VOLUME_NAME &> /dev/null
if [ $? -ne 0 ];
then
	echo "Removing snapshot failed."
	exit 1
fi

