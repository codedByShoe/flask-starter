from flask_mail import Message
from flask import current_app
from threading import Thread

def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)

def send_email(mail, to, subject, html_body, text_body=None, sender=None):
    app = current_app._get_current_object()

    if sender is None:
        sender = app.config.get("MAIL_DEFAULT_SENDER", "noreply@example.com")

    msg = Message(subject=subject,
                  sender=sender,
                  recipients=[to],
                  html=html_body,
                  body=text_body)

    Thread(target=send_async_email, args=(app, mail, msg)).start()
