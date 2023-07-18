from email.message import EmailMessage
import smtplib
import os
import ssl
# from dotenv import load_dotenv
# load_dotenv()

class Notify:
    # __serviceAccEmail = os.getenv('SERVICE_EMAIL')
    # __serviceAccPassword = os.getenv('SERVICE_PASSWORD')

    _subject = " Something went wrong !!"

    def email(errorMessage:str,to:list[str]):

        for dest in to:
            em = EmailMessage()
            em['From']=Notify.__serviceAccEmail
            em['Subject']= Notify._subject
            em.set_content(errorMessage)
            em['To']= dest
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465 , context=context) as s:    
               
                s.login(Notify.__serviceAccEmail, Notify.__serviceAccPassword)
                s.sendmail(Notify.__serviceAccEmail, dest, em.as_string())
                s.quit()

