#!/usr/bin/env python3
#
# Script to create a backup of a snapshot

import sys
import os
import shutil
import subprocess
import tempfile
import time

SNAPSHOT_SIZE="1024M"
SNAPSHOT_NAME="snap"
VOLUME_GROUP="/dev/pluto-vg"
LOGICAL_VOLUME="root"
MOUNT_POINT="/mnt/snap"

BACKUP_MOUNT_POINT="/mnt/backup"
BACKUP_SOURCE="/mnt/snap/home/marc"
BACKUP_DEST="/mnt/backup"
BACKUP_NAME="HomeBackup"

# Step 1 : Create the snapshot volume
args = ["lvcreate", "-L" + SNAPSHOT_SIZE, "-s", "-n", SNAPSHOT_NAME, VOLUME_GROUP + "/" + LOGICAL_VOLUME]
if subprocess.call(args) != 0:
    print("Snapshot creation failed.")
    sys.exit(1)

print("Created snapshot of " + VOLUME_GROUP + "/" + LOGICAL_VOLUME)

# Step 2 : Mount the snapshot
args = ["mount", VOLUME_GROUP + "/" + SNAPSHOT_NAME, MOUNT_POINT, "-o", "ro"]
if subprocess.call(args) != 0:
    print("Mounting the snapshot failed.")
    sys.exit(1)

print("Snapshot mounted at " + MOUNT_POINT)

# Step 3 : Mount backup location
if BACKUP_MOUNT_POINT:
    args = ["mount", BACKUP_MOUNT_POINT]
    if subprocess.call(args) != 0:
        print("Mounting the backup location failed.")
        sys.exit(1)

    print("Backup location mounted at " + BACKUP_MOUNT_POINT)
    
# Step 4 : Change to the backup source folder
cur_dir = os.path.abspath(os.path.curdir)
os.chdir(BACKUP_SOURCE)

# Step 5 : Create TAR
tarfile = os.path.join(BACKUP_DEST, BACKUP_NAME + ".tar.gz")
args = ["tar", "cfz", tarfile, BACKUP_SOURCE]
if subprocess.call(args) != 0:
    print("Create TAR file failed.")
    sys.exit(1)

print("TAR file created")

# Step x : Change back to current dir
os.chdir(cur_dir)

# Step x : Unmount the backup location
if BACKUP_MOUNT_POINT:
    args = ["umount", BACKUP_MOUNT_POINT]
    if subprocess.call(args) != 0:
        print("Unmounting the backup location failed.")
        sys.exit(1)

    print("Backup location unmounted")

# Step x : Wait until snapshot device is not busy anymore
time.sleep(60)

# Step x : Unmount the snapshot
args = ["umount", VOLUME_GROUP + "/" + SNAPSHOT_NAME]
if subprocess.call(args) != 0:
    print("Unmounting the snapshot failed.")
    sys.exit(1)

print("Snapshot unmounted")

# Step x : Remove the snapshot
args = ["lvremove", "-f", VOLUME_GROUP + "/" + SNAPSHOT_NAME]
if subprocess.call(args) != 0:
    print("Removing the snapshot failed.")
    sys.exit(1)

print("Snapshot removed")
