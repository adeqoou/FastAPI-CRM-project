import smtplib
from fastapi import HTTPException, status
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from src.celery import celery_app

load_dotenv()


@celery_app.task
def send_mail(email: str, subject: str, message: str):
    smtp_server: str = os.getenv('SMTP_SERVER')
    smtp_port: int = os.getenv('SMTP_PORT')
    smtp_user: str = os.getenv('SMTP_USER')
    smtp_password: str = os.getenv('SMTP_PASSWORD')

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server.sendmail(smtp_user, email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
