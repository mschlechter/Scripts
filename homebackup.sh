#!/bin/bash

VOLUME_GROUP="/dev/main-vg"
LOGICAL_VOLUME="root"

SNAPSHOT_NAME="snap"
SNAPSHOT_MOUNT_POINT="/mnt/snap"
SNAPSHOT_SIZE="1024M"

LVCREATE=$(which lvcreate)
LVREMOVE=$(which lvremove)
MOUNT=$(which mount)
UMOUNT=$(which umount)
TAR=$(which tar)

# Create the snapshot volume
VOLUME_NAME="$VOLUME_GROUP/$LOGICAL_VOLUME"
echo $VOLUME_NAME
$LVCREATE -L $SNAPSHOT_SIZE -s -n $SNAPSHOT_NAME $VOLUME_NAME

