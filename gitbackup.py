#!/usr/bin/env python3
#
# Script to backup all git repositories in a given source directory.

import sys
import os
import shutil
import subprocess
import tempfile

from typing import Iterable

#
# Configuration section
#

SOURCE_DIR = "/home/marc/Temp/src"
DESTINATION_DIR = "/home/marc/Temp/dest"
MOUNT_POINT = None # "/mnt/backup"

#
# End of configuration section
#

cur_dir = os.path.abspath(os.path.curdir)

def do_mount(dir: str) -> bool:
    result = subprocess.call(["mount", dir])
    return result == 0

def do_unmount(dir: str) -> bool:
    result = subprocess.call(["umount", dir])
    return result == 0

def create_git_clone(parent_dir: str, git_dir: str) -> bool:
    args = ["git", "clone", "--bare", os.path.join(parent_dir, git_dir)]
    return subprocess.call(args) == 0

def get_git_directories(dir: str) -> Iterable[str]:
    return sorted([
        name for name in os.listdir(dir)
        if os.path.isdir(os.path.join(dir, name))
        and name.endswith(".git")
    ])


# Step 1 : Try to mount the mount point
if MOUNT_POINT and not do_mount(MOUNT_POINT):
    print("Failed to mount " + MOUNT_POINT)
    sys.exit(1)

# Step 2 : Check if directories exist
if not os.path.exists(SOURCE_DIR):
    print ("\nERROR : Source directory does not exist!")
    sys.exit(1)

if not os.path.exists(DESTINATION_DIR):
    print ("\nERROR : Destination directory does not exist!")
    sys.exit(1)

# Step 3 : Create temp dir and change to it
temp_dir = tempfile.mkdtemp()
os.chdir(temp_dir)

# Step 4 : Get immediate subdirectories which name ends with .git
git_directories = get_git_directories(SOURCE_DIR)

# Step 5 : Backup git repositories
for git_dir in git_directories:
    temp_git_dir = os.path.join(temp_dir, git_dir)
    dest_git_dir = os.path.join(DESTINATION_DIR, git_dir)

    # Step 5.1 : Clone git repository
    print("Cloning into " + temp_git_dir)

    if not create_git_clone(SOURCE_DIR, git_dir):
        sys.exit(1) # Cloning failed
    
    # Step 5.2 : Create tar archive
    tarfile = dest_git_dir + ".tar.gz"
    tarargs = ["tar", "cfz", tarfile, temp_git_dir]
    if subprocess.call(tarargs) != 0:
        sys.exit(1) # Tar failed

# Step 6 : Change back to current dir
os.chdir(cur_dir)

# Step 7 : Remove temp dir
print ("Removing " + temp_dir)
shutil.rmtree(temp_dir)

# Step 8 : Unmount the mount point
if MOUNT_POINT and not do_unmount(MOUNT_POINT):
    print("Failed to unmount " + MOUNT_POINT)
    sys.exit(1)
