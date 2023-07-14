import smtplib
from email.mime.text import MIMEText
    
class EmailSender:
    def __init__(self,sender_email,recipient_email,subject):
        self.sender_email=sender_email
        self.recipient_email=recipient_email
        self.subject=subject

    def send_email(self,message):
        try:
            message=MIMEText(message)
            message['From']=self.sender_email
            message['To']=self.recipient_email
            message['Subject']=self.subject    
        except Exception as e:
            print(f"Error: {e}")

