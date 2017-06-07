""" Mail script which uses a config file for the mailsettings """

import configparser
import os
import smtplib

from email.mime.multipart import MIMEMultipart

class Logger:
    """Logger class for logging messages"""
    log_entries = []

    def log(self, message):
        """Log message"""
        self.log_entries.append(message)
        print(message)

def main():
    """Main function when run directly. Parses arguments and runs the backup routine."""

    import argparse
    parser = argparse.ArgumentParser(
        description="mail with external configuration")
    parser.add_argument("-c", "--config", help="configuration file", required=True)
    parser.add_argument("-to", "--to", help="recipient", required=True)
    parser.add_argument("-s", "--subject", help="subject", required=True)
    parser.add_argument("-b", "--body", help="message body", required=True)

    args = parser.parse_args()

    sendmail(args.config, args.to, args.subject, args.body)

def sendmail(config_file, recipient, subject, body):
    """Send mail function"""

    logger = Logger()
    current_log = None

    try:

        # If config file does not exist, abort
        if not os.path.isfile(config_file):
            logger.log("Configuration file does not exist!")
            return False

        config = configparser.RawConfigParser()
        config.read(config_file)

        smtp_server = config.get("smtp", "server")
        smtp_server_port = config.getint("smtp", "server_port")
        smtp_usessl = config.getboolean("smtp", "usessl")
        smtp_useauth = config.getboolean("smtp", "useauth")
        smtp_username = config.get("smtp", "username")
        smtp_password = config.get("smtp", "password")
        mail_from = config.get("profile", "from")

        logger.log("SMTP Server      : " + smtp_server)
        logger.log("SMTP Server port : " + str(smtp_server_port))
        logger.log("SMTP Use SSL     : " + str(smtp_usessl))
        logger.log("SMTP Use auth    : " + str(smtp_useauth))
        logger.log("SMTP Username    : " + smtp_username)
        logger.log("SMTP Password    : " + smtp_password)
        logger.log("Mail from        : " + mail_from)

        message = MIMEMultipart()
        message['Subject'] = subject
        message['To'] = recipient
        message['From'] = mail_from

        smtp = smtplib.SMTP(smtp_server, smtp_server_port)
        smtp.sendmail(mail_from, [recipient], message.as_string())
        smtp.quit()

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
