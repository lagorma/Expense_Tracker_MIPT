from flask_mail import Message
from app import mail
from flask import current_app
from app import mail
from threading import Thread


def send_async_email(app, msg):
    """Sending by email is performed in a separate thread"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """auxiliary function that sends an email"""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
