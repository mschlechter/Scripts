#!/usr/bin/env python3
# 
# keep.py
#
# Simple script which creates an incremental rsync backup tree using --link-dest.
#

import os
import subprocess
import sys
import time

#
# Prepare logger
#

current_log = None
log_entries = []

def log(message):
    log_entries.append(message)
    print(message)

try:

    #
    # Parse arguments
    #

    import argparse
    parser = argparse.ArgumentParser(description="keep a time machine like history of a source directory")
    parser.add_argument("source", help="source directory for backup")
    parser.add_argument("destination", help="destination directory for backup")
    parser.add_argument("-r", "--retention", help="number of backups to keep. Default is 7")
    parser.add_argument("-f", "--force", help="overwrite today's backup if it exists", action="store_true")
    args = parser.parse_args()

    source = args.source
    destination = args.destination
    retention = 7
    force = args.force

    if args.retention is not None:
        retention = args.retention

    #
    # Check if source and destination directory exist
    #

    if not os.path.isdir(source):
        log("Source directory does not exist!")
        sys.exit(1)

    if not os.path.isdir(destination):
        log("Destination directory does not exist!")
        sys.exit(1)

    #
    # Print summary
    #

    log("Source      : " + source)
    log("Destination : " + destination)
    log("Retention   : " + str(retention))
    if force:
        log("Overwriting today's backup if it exists!")

    #
    # Check and create destination directory for today
    #

    current_destination = os.path.join(destination, time.strftime("%Y%m%d"))

    if os.path.isdir(current_destination) and not force:
        log("Backup for today already exists!")
        sys.exit(1)

    if not os.path.isdir(current_destination):
        log("Creating directory " + current_destination)
        os.makedirs(current_destination)


    #
    # Prepare log directory and files
    #

    log_dir = os.path.join(destination, "Logs")
    if not os.path.isdir(log_dir):
        log("Creating directory " + log_dir)
        os.makedirs(log_dir)

    current_log = os.path.join(log_dir, time.strftime("%Y%m%d") + "_keep.log")
    current_log_rsync = os.path.join(log_dir, time.strftime("%Y%m%d") + "_rsync.log")

    log("Log file : " + current_log)
    log("Log file (rsync) : " + current_log_rsync)

    #
    # Find previous backup
    #

    backup_dirs = [s for s in os.listdir(destination) 
        if not os.path.isfile(os.path.join(destination, s)) 
        and os.path.join(destination, s) != current_destination 
        and os.path.join(destination, s) != log_dir]
    backup_dirs.sort(key=lambda s: os.path.getmtime(os.path.join(destination, s)), reverse=True)

    last_backup_found = False
    last_backup_dir = None

    if len(backup_dirs) > 0:
        last_backup_found = True
        last_backup_dir = os.path.join(destination, backup_dirs[0])

    if last_backup_found:
        log("Previous backup found : " + last_backup_dir)
    else:
        log("No previous backup found.")

    #
    # Compose rsync command
    #

    rsync_args = []

    if last_backup_found:

        # Incremental backup
        log("Preparing incremental backup...")
        rsync_args = ["rsync", "-av", "--delete", "--link-dest", last_backup_dir, source, current_destination]

    else:

        # Full backup
        log("Preparing full backup...")
        rsync_args = ["rsync", "-av", "--delete", source, current_destination]

    #
    # Run rsync command and redirect output to rsync log file
    #

    log("Backup started at " + time.strftime("%T"))

    rsync_result = 0

    with open(current_log_rsync, 'w') as clr:
        rsync_result = subprocess.call(rsync_args, stdout=clr, stderr=clr)

    if rsync_result > 0:
        log("There were errors during the backup operation!")
        sys.exit(1)

    log("Backup completed successfully at " + time.strftime("%T"))

except SystemExit as e:

    log("")

except Exception as e:

    log("An error has occurred : %s" % e)

finally:

    # Write log
    if current_log is not None:
        with open(current_log, 'w') as cl:
            for log_item in log_entries:
                cl.write("%s\n" % log_item)
