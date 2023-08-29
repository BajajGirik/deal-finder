from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import os
import ssl

load_dotenv()


class EmailNotification:
    __service_account_email = os.environ.get("SERVICE_EMAIL")
    __service_account_password = os.environ.get("SERVICE_EMAIL_PASSWORD")
    DEFAULT_SUBJECT = " Something went wrong !!"

    @staticmethod
    def send_email(message: str, subject: str, to: list[str]) -> None:
        if (
            not EmailNotification.__service_account_email
            or not EmailNotification.__service_account_password
        ):
            raise Exception(
                "Please provide both service email and password to send email"
            )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as gmail:
            gmail.login(
                EmailNotification.__service_account_email,
                EmailNotification.__service_account_password,
            )
            for destination_mail in to:
                email_message = EmailMessage()
                email_message["From"] = EmailNotification.__service_account_email
                email_message["Subject"] = (
                    subject if subject else EmailNotification.DEFAULT_SUBJECT
                )
                email_message.set_content(message)
                email_message["To"] = destination_mail
                gmail.sendmail(
                    EmailNotification.__service_account_email,
                    destination_mail,
                    email_message.as_string(),
                )
            gmail.quit()
