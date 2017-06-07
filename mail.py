""" Mail script which uses a config file for the mailsettings """

import configparser
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    parser.add_argument("--text", help="message text", required=True)
    parser.add_argument('--html', dest='html', action='store_true')
    parser.set_defaults(html=False)

    args = parser.parse_args()

    sendmail(args.config, args.to, args.subject, args.text, args.html)

def sendmail(config_file, recipient, subject, text, html):
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
        smtp_usetls = config.getboolean("smtp", "usetls")
        smtp_useauth = config.getboolean("smtp", "useauth")
        smtp_username = config.get("smtp", "username")
        smtp_password = config.get("smtp", "password")
        mail_from = config.get("profile", "from")

        logger.log("[SMTP configuration]")
        logger.log("SMTP Server      : " + smtp_server)
        logger.log("SMTP Server port : " + str(smtp_server_port))
        logger.log("SMTP Use TLS     : " + str(smtp_usetls))
        logger.log("SMTP Use auth    : " + str(smtp_useauth))
        logger.log("SMTP Username    : " + smtp_username)
        logger.log("SMTP Password    : " + "*" * len(smtp_password))
        logger.log("")
        logger.log("[Message configuration]")
        logger.log("Mail from        : " + mail_from)
        logger.log("Recipient        : " + recipient)
        logger.log("Subject          : " + subject)
        logger.log("Test is HTML     : " + str(html))

        message = MIMEMultipart()
        message['Subject'] = subject
        message['To'] = recipient
        message['From'] = mail_from

        message.attach(MIMEText(text, 'html' if html else 'plain'))

        smtp = smtplib.SMTP(smtp_server, smtp_server_port)
        if smtp_usetls:
            smtp.starttls()

        if smtp_useauth:
            smtp.login(smtp_username, smtp_password)

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
