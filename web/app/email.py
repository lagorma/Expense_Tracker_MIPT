from flask_mail import Message
from app import mail
from flask import current_app
from app import mail
from threading import Thread
import smtplib


#def send_async_email(app, msg):
#    with app.app_context():
#            mail.send(msg)

#def send_email(subject, sender, recipients, text_body, html_body):
   # to_name = 'TO_NAME';
   # to_email = 'TO_EMAIL_ADDRESS';
   # data = array('name'=>"Sam Jose", "body" => "Test mail");
   # Mail::send('emails', $data, function($message) use ($to_name, $to_email) {
   #     $message->to($to_email, $to_name)->subject('Artisans Web Testing Mail');
    #    $message->from('FROM_EMAIL_ADDRESS','Artisans Web');
    #connect()
    #with app.app_context():
        #with mail.connect() as conn:
            #subject='subject'
            #message='message'
            #msg=Message(
        #server = smtplib.SMTP(smtp.gmail.com)
        #server.starttls()
            #server.login(
    #msg = Message(subject, sender=sender, recipients=recipients)
    #msg.body = text_body
    #msg.html = html_body
    #Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
            #mail.send(msg)
#def send_email(host, subject, to_addr, from_addr, body_text):
    #msg = MIMEText ('%s - %s' % (msg.text, msg.channel))
    #msg = Message(subject, sender=sender, recipients=recipients)
    #server = smtplib.SMTP('smtp.gmail.com')
    #server.starttls()
    #server.login(current_app.config['MAIL_USERNAME'],current_app.config['MAIL_PASSWORD'])
    #msg.body = text_body
    #msg.html = html_body
    #msg['From'] = ('from')
    #msg['To'] = ('to')
    #server.sendmail(msg)
    #iserver.quit()

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate

#FROM_ADDRESS = 'sender@gmail.com'
#MY_PASSWORD = 'password'
#TO_ADDRESS = 'receiver@test.co.jp'
#BCC = 'receiver2@test.net'
#SUBJECT = 'GmailのSMTPサーバ経由'
#BODY = 'pythonでメール送信'


#def create_message(from_addr, to_addr, bcc_addrs, subject, body):
#    msg = MIMEText(body)
#    msg['Subject'] = subject
#    msg['From'] = from_addr
#    msg['To'] = to_addr
#    msg['Bcc'] = bcc_addrs
#    msg['Date'] = formatdate()
#    return msg


def send_mail(subject, sender, recipients, text_body):
    """ Function allows to send email if a user forgot the paswword """
    SERVER_NAME='smtp.gmail.com'
    SERVER_PORT=587
    #USER_NAME='pdara6116@gmail.com'
    PASSWORD='linux56test'
    print('connecting')
    server = smtplib.SMTP(SERVER_NAME,SERVER_PORT)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, PASSWORD)
    #msg.body = text_body
    #msg = Message(subject, sender=sender, recipients=recipients)
    msg = text_body
    #msg.html = html_body
    #text = text_body
    #html = html_body
    #server.sendmail('pdara6116@gmail.com', 'petrova.dv@phystech.edu', text_)
    server.sendmail(sender, recipients, msg)
    server.quit()


#if __name__ == '__main__':

#    to_addr = TO_ADDRESS
#    subject = SUBJECT
#    body = BODY

#    msg = create_message(FROM_ADDRESS, to_addr, BCC, subject, body)
#    send(FROM_ADDRESS, to_addr, msg)
