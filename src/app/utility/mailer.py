"""
Utility functions to send mail
"""
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import settings


def send_message(to_emails, subject, html=None, sender="PO-Administrator@cdac.ca"):
    if not isinstance(to_emails, list):
        to_emails = [to_emails]

    logging.info("Sending emails to %s with content %s", to_emails, html)

    for email in to_emails:
        if email.find("@") == -1:
            email = email + "@cdac.ca"
            logging.info("Sending mail to %s", email)

        message = Mail(
            from_email=sender, subject=subject, to_emails=[email], html_content=html
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_KEY)
            sg.send(message)
        except Exception as e:
            logging.warn(str(e))
