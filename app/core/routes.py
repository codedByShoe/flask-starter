from flask import render_template
from flask_login import login_required, current_user
from app.utils import send_email
from app.extensions import mail

from app.core import bp

@bp.route('/send-test')
def send_test():
    send_email(
        mail=mail,
        to='recipient@example.com',
        subject='Hello from Flask',
        html_body='<h1>This is a test</h1>',
        text_body='This is a test'
    )
    return "Email is being sent in the background!"

@bp.route('/')
def index():
    """Home page route"""
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page (requires authentication)"""
    return render_template('dashboard.html', title='Dashboard')

@bp.route('/profile')
@login_required
def profile():
    """User profile page (requires authentication)"""
    return render_template('profile.html', title='Profile', user=current_user)