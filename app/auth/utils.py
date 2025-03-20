from flask import current_app
from app import db
from app.auth.models import User
from app.email.email import send_email
from app.utils.security import generate_confirmation_token, generate_reset_token
from flask import render_template, url_for

def send_confirmation_email(user):
    """Send confirmation email to a new user"""
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    subject = "Please confirm your email"
    template = render_template('email/verify.html', confirm_url=confirm_url, user=user)

    # Use the email queue for sending emails asynchronously
    current_app.email_queue.enqueue(
        send_email,
        recipient=user.email,
        subject=subject,
        html_body=template
    )

def send_password_reset_email(user):
    """Send password reset email to user"""
    token = generate_reset_token(user.id)
    reset_url = url_for('auth.reset_password', token=token, _external=True)

    subject = "Password Reset Request"
    template = render_template('email/reset_password.html', reset_url=reset_url, user=user)

    # Use the email queue for sending emails asynchronously
    current_app.email_queue.enqueue(
        send_email,
        recipient=user.email,
        subject=subject,
        html_body=template
    )

def create_user(email, password, first_name=None, last_name=None):
    """Create a new user and return the user object"""
    user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    db.session.add(user)
    db.session.commit()
    return user