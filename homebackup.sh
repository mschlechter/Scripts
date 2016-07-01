#!/bin/bash
#
# Script which creates a LVM snapshot, mounts it, and then makes a
# backup of the configured directories.
#
# It is recommended to use a logical volume and filesystem dedicated to
# data. Removing a snapshot of a filesystem that is in use (for example
# the root filesystem), might cause errors with lvremove.
#
# If you have a separate logical volume with one filesystem in it, this
# script should work just fine.
#

#
# Begin of configuration section
#

VOLUME_GROUP="/dev/saturn-vg"
VOLUME_NAME="$VOLUME_GROUP/home"

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

#
# End of configuration section
#

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
		log "Removing snapshot volume $SNAPSHOT_VOLUME_NAME"
		$LVREMOVE -f $SNAPSHOT_VOLUME_NAME \
			|| log "Removing snapshot failed."
	fi
}

# Create snapshot volume
log "Creating snapshot for volume $VOLUME_NAME"
$LVCREATE -L $SNAPSHOT_SIZE -s -n $SNAPSHOT_NAME $VOLUME_NAME \
	&& log "Snapshot volume $SNAPSHOT_VOLUME_NAME created." \
	|| die "Snapshot creation failed."

# Mount snapshot filesystem
log "Mounting snapshot on $SNAPSHOT_MOUNT_POINT"
$MOUNT $SNAPSHOT_VOLUME_NAME $SNAPSHOT_MOUNT_POINT -o ro,nouuid \
	|| die "Mounting snapshot failed."

# Perform cleanup
cleanup

# Log backup succeeded
log "Backup succeeded!"
