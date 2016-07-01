#!/bin/bash
#
# Script which creates a LVM snapshot, mounts it, and then makes a
# backup of the configured directories.
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

TARGET_MOUNT_POINT="/mnt/backup"
TARGET_ARCHIVE="$TARGET_MOUNT_POINT/SaturnHomes-$(date +"%Y%m%d").tar.gz"

SOURCE_DIR="/mnt/snap"

LVCREATE=$(which lvcreate)
LVREMOVE=$(which lvremove)
LVDISPLAY=$(which lvdisplay)
MOUNT=$(which mount)
UMOUNT=$(which umount)
TAR=$(which tar)
MOUNTPOINT=$(which mountpoint)

CURRENT_DIR=$(pwd)

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
	log "There were errors during the backup!"
	exit 1
}

function cleanup
{
	# Change back to current dir
	log "Changing back to $CURRENT_DIR"
	cd $CURRENT_DIR

	# Unmount target filesystem (when mounted)
	if $MOUNTPOINT -q $TARGET_MOUNT_POINT; then
		log "Unmounting target file system"
		$UMOUNT $TARGET_MOUNT_POINT \
			|| log "Unmounting target file system failed."
	fi

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

# Mount target filesystem
log "Mounting target filesystem $TARGET_MOUNT_POINT"
$MOUNT $TARGET_MOUNT_POINT \
	|| die "Mounting target filesystem failed."

# Change to the backup source directory
cd $SOURCE_DIR \
	|| die "Could not change to $SOURCE_DIR"

# Create tar archive
$TAR cfz $TARGET_ARCHIVE $SOURCE_DIR \
	&& log "Archive $TARGET_ARCHIVE created." \
	|| die "Failed to create archive $TARGET_ARCHIVE"

# Perform cleanup
cleanup

# Log backup succeeded
log "Backup succeeded!"
