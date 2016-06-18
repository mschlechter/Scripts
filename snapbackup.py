#!/usr/bin/env python3
#
# Script to create a backup of a snapshot

import sys
import os
import shutil
import subprocess
import datetime
import time

VOLUME_GROUP="/dev/pluto-vg"
LOGICAL_VOLUME="root"

SNAPSHOT_NAME="snap"
SNAPSHOT_MOUNT_POINT="/mnt/snap"
SNAPSHOT_SIZE="1024M"

BACKUP_MOUNT_POINT="/mnt/backup"
BACKUP_SOURCE="/mnt/snap/home/marc"
BACKUP_DEST="/mnt/backup"
BACKUP_ARCHIVE_NAME="HomeBackup"

LVCREATE = "/sbin/lvcreate"
LVREMOVE = "/sbin/lvremove"
MOUNT = "/bin/mount"
UMOUNT = "/bin/umount"
TAR = "/bin/tar"

# 1. Create the snapshot volume
args = [LVCREATE, "-L" + SNAPSHOT_SIZE, "-s", "-n", SNAPSHOT_NAME, VOLUME_GROUP + "/" + LOGICAL_VOLUME]
if subprocess.call(args) != 0:
    print("Snapshot creation failed.")
    sys.exit(1)

print("Created snapshot of " + VOLUME_GROUP + "/" + LOGICAL_VOLUME)

# 2. Mount the snapshot
args = [MOUNT, VOLUME_GROUP + "/" + SNAPSHOT_NAME, SNAPSHOT_MOUNT_POINT, "-o", "ro"]
if subprocess.call(args) != 0:
    print("Mounting the snapshot failed.")
    sys.exit(1)

print("Snapshot mounted at " + SNAPSHOT_MOUNT_POINT)

# 3. Mount backup location
if BACKUP_MOUNT_POINT:
    args = [MOUNT, BACKUP_MOUNT_POINT]
    if subprocess.call(args) != 0:
        print("Mounting the backup location failed.")
        sys.exit(1)

    print("Backup location mounted at " + BACKUP_MOUNT_POINT)
    
# 4. Change to the backup source folder
cur_dir = os.path.abspath(os.path.curdir)
os.chdir(BACKUP_SOURCE)

# 5. Create backup archive
today = datetime.date.today().strftime("%Y%m%d")
tarfile = os.path.join(BACKUP_DEST, BACKUP_ARCHIVE_NAME) + today + ".tar.gz"
args = [TAR, "cfz", tarfile, BACKUP_SOURCE]
if subprocess.call(args) != 0:
    print("Create backup archive failed.")
    sys.exit(1)

print("Backup archive " + tarfile + " created")

# 6. Change back to current dir to prevent keeping the snapshot busy
os.chdir(cur_dir)

# 7. Unmount the backup location
if BACKUP_MOUNT_POINT:
    args = [UMOUNT, BACKUP_MOUNT_POINT]
    if subprocess.call(args) != 0:
        print("Unmounting the backup location failed.")
        sys.exit(1)

    print("Backup location unmounted")

# 8. Unmount the snapshot
args = [UMOUNT, VOLUME_GROUP + "/" + SNAPSHOT_NAME]
if subprocess.call(args) != 0:
    print("Unmounting the snapshot failed.")
    sys.exit(1)

print("Snapshot unmounted")

# 9. Remove the snapshot
args = [LVREMOVE, "-f", VOLUME_GROUP + "/" + SNAPSHOT_NAME]
if subprocess.call(args) != 0:
    print("Removing the snapshot failed.")
    sys.exit(1)

print("Snapshot removed")
