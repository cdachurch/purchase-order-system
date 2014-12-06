"""
Utility functions to send mail
"""
from google.appengine.api import mail

import logging

def send_message(to_emails, subject, html=None, sender="administrator@cdac.ca"):
    if not isinstance(to_emails, list):
        to_emails = [to_emails]
    
    logging.info("Sending emails to %s with content %s", to_emails, html)

    for email in to_emails:
        if not mail.is_email_valid(email):
            # Don't send the message
            logging.error("Declined sending an email to an invalid address: %s", email)
            return
        if email.find("@") == -1:
            email = email + "@cdac.ca"
            logging.info("Sending mail to %s", email)

        message = mail.EmailMessage(sender=sender,
                                    subject=subject,
                                    to=email,
                                    html=html)

        message.send()
