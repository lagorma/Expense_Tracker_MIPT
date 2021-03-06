from flask import render_template, current_app
from app.email import send_mail


def send_password_reset_email(user):
    """ Function send an email with a URL with token"""
    token = user.get_reset_password_token()
    send_mail('[Microblog] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token))
