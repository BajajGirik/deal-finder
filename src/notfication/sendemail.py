from email.message import EmailMessage
from dotenv import load_dotenv
import smtplib
import os
import ssl

load_dotenv()

class EmailNotification:
    __serviceAccEmail = os.environ.get('SERVICE_EMAIL')
    __serviceAccPassword = os.environ.get('SERVICE_EMAIL_PASSWORD')
    _Default_subject = " Something went wrong !!"
   
    @staticmethod
    def sendEmail(message:str,subject:str,to:list[str]):
        if not EmailNotification.__serviceAccEmail or not EmailNotification.__serviceAccPassword:
            raise Exception("Please provide both service email and password to send email")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as gmail:    
            gmail.login(EmailNotification.__serviceAccEmail, EmailNotification.__serviceAccPassword)
            for dest in to:
                newEmail = EmailMessage()
                newEmail['From']=EmailNotification.__serviceAccEmail
                newEmail['Subject']= subject if subject else EmailNotification._Default_subject
                newEmail.set_content(message)
                newEmail['To']= dest
                gmail.sendmail(EmailNotification.__serviceAccEmail, dest, newEmail.as_string())
            gmail.quit()

