from flask import render_template, current_app
from app.email import send_mail


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print(token)
    send_mail('[Microblog] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token))
              # html_body=render_template('email/reset_password.html', 
                                         #user=user, token=token))
    #BCC = 'receiver2@test.net'
    #SUBJECT = 'GmailのSMTPサーバ経由'
    #BODY = 'pythonでメール送信'
    #msg = create_message(current_app.config['ADMINS'][0],[user.email], BCC, SUBJECT, BODY)
    #send_mail(current_app.config['ADMINS'][0], [user.email], msg)
    #send_mail()
