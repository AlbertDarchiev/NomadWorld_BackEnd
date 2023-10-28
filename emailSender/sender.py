from email.message import EmailMessage
import ssl
import smtplib
import re

sender = 'nomadworld.itb@gmail.com'
password = 'bajx esvc tjbw vkvn'
class ESender:
    def check(s):
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.match(pat,s):
            print("Valid Email")
            return True
        else:
            print("Invalid Email")
            return False
 

    @staticmethod
    def send_email(receiver, subject, body):
        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.send_message(em)
