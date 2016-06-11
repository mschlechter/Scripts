#!/usr/bin/env python3
#
# Script to create a backup of a snapshot

import sys
import os
import shutil
import subprocess
import tempfile

SNAPSHOT_SIZE="1024M"
SNAPSHOT_NAME="snap"
VOLUME_GROUP="/dev/pluto-vg"
LOGICAL_VOLUME="root"
MOUNT_POINT="/mnt/snap"

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
