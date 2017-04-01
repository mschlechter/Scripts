""" Simple script which creates an incremental rsync backup tree using --link-dest. """

import os
import subprocess
import sys
import time

#
# Prepare logger
#

class Logger:
    """Logger class for logging messages"""
    log_entries = []

    def log(self, message):
        """Log message"""
        self.log_entries.append(message)
        print(message)

def main():
    """Main function when run directly"""

    #
    # Parse arguments
    #

    import argparse
    parser = argparse.ArgumentParser(
        description="keep a time machine like history of a source directory")
    parser.add_argument("source", help="source directory for backup")
    parser.add_argument("destination", help="destination directory for backup")
    parser.add_argument("-r", "--retention", help="number of backups to keep. Default is 7")
    parser.add_argument("-f", "--force",
                        help="overwrite today's backup if it exists", action="store_true")
    args = parser.parse_args()

    source = args.source
    destination = args.destination
    retention = 7
    force = args.force

    if args.retention is not None:
        retention = args.retention

    if not backup(source, destination, retention, force):
        sys.exit(1)

def backup(source, destination, retention, force):
    """Backup function which does the actual work"""

    logger = Logger()

    current_log = None

    try:

        #
        # Check if source and destination directory exist
        #

        if not os.path.isdir(source):
            logger.log("Source directory does not exist!")
            return False

        if not os.path.isdir(destination):
            logger.log("Destination directory does not exist!")
            return False

        #
        # Print summary
        #

        logger.log("Source      : " + source)
        logger.log("Destination : " + destination)
        logger.log("Retention   : " + str(retention))
        if force:
            logger.log("Overwriting today's backup if it exists!")

        #
        # Check and create destination directory for today
        #

        current_destination = os.path.join(destination, time.strftime("%Y%m%d"))

        if os.path.isdir(current_destination) and not force:
            logger.log("Backup for today already exists!")
            return False

        if not os.path.isdir(current_destination):
            logger.log("Creating directory " + current_destination)
            os.makedirs(current_destination)


        #
        # Prepare log directory and files
        #

        log_dir = os.path.join(destination, "Logs")
        if not os.path.isdir(log_dir):
            logger.log("Creating directory " + log_dir)
            os.makedirs(log_dir)

        current_log = os.path.join(log_dir, time.strftime("%Y%m%d") + "_keep.log")
        current_log_rsync = os.path.join(log_dir, time.strftime("%Y%m%d") + "_rsync.log")

        logger.log("Log file : " + current_log)
        logger.log("Log file (rsync) : " + current_log_rsync)

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
            logger.log("Previous backup found : " + last_backup_dir)
        else:
            logger.log("No previous backup found.")

        #
        # Compose rsync command
        #

        rsync_args = []

        if last_backup_found:

            # Incremental backup
            logger.log("Preparing incremental backup...")
            rsync_args = ["rsync", "-av", "--delete", "--link-dest",
                          last_backup_dir, source, current_destination]

        else:

            # Full backup
            logger.log("Preparing full backup...")
            rsync_args = ["rsync", "-av", "--delete", source, current_destination]

        #
        # Run rsync command and redirect output to rsync log file
        #

        logger.log("Backup started at " + time.strftime("%T"))

        rsync_result = 0

        with open(current_log_rsync, 'w') as clr:
            rsync_result = subprocess.call(rsync_args, stdout=clr, stderr=clr)

        if rsync_result > 0:
            logger.log("There were errors during the backup operation!")
            return False

        logger.log("Backup completed successfully at " + time.strftime("%T"))

        return True

    except Exception as exception:

        logger.log("An error has occurred : %s" % exception)
        return False

    finally:

        # Write log
        if current_log is not None:
            with open(current_log, 'w') as current_log_file:
                for log_item in logger.log_entries:
                    current_log_file.write("%s\n" % log_item)


#
# When being run directly, start main()
#

if __name__ == "__main__":
    main()
