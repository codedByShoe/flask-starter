from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

from app.core import bp

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