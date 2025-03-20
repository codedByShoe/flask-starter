import pytest
from flask import url_for
from app import db
from app.auth.models import User

def test_register_page(client):
    """Test that register page loads correctly"""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Create Account' in response.data

def test_login_page(client):
    """Test that login page loads correctly"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_user(client, app):
    """Test user registration process"""
    response = client.post('/auth/register', data={
        'email': 'newuser@example.com',
        'password': 'password123',
        'password_confirm': 'password123',
        'first_name': 'New',
        'last_name': 'User'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Registration successful' in response.data

    # Check that user was created in the database
    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.first_name == 'New'
        assert user.last_name == 'User'
        assert user.is_active is False  # User should be inactive until email verification

def test_register_validation(client):
    """Test validation during registration"""
    # Test with mismatched passwords
    response = client.post('/auth/register', data={
        'email': 'invalid@example.com',
        'password': 'password123',
        'password_confirm': 'different',
        'first_name': 'Test',
        'last_name': 'User'
    })

    assert response.status_code == 200
    assert b'Passwords must match' in response.data

    # Test with invalid email
    response = client.post('/auth/register', data={
        'email': 'not-an-email',
        'password': 'password123',
        'password_confirm': 'password123',
        'first_name': 'Test',
        'last_name': 'User'
    })

    assert response.status_code == 200
    assert b'Invalid email address' in response.data

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'You have been logged in successfully' in response.data

def test_login_invalid_credentials(client, test_user):
    """Test login with invalid credentials"""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_logout(auth_client):
    """Test logout functionality"""
    response = auth_client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out successfully' in response.data

def test_protected_route(client, auth_client):
    """Test that protected routes require authentication"""
    # Unauthenticated user should be redirected
    # response = client.get('/dashboard', follow_redirects=False)
    # assert response.status_code == 302  # Redirect status code

    # With follow_redirects, we should end up at the login page
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

    # Authenticated user should be able to access
    response = auth_client.get('/dashboard')
    assert response.status_code == 200
    assert b'Dashboard' in response.data
def test_confirm_email(client, app, test_user):
    """Test email confirmation process"""
    with app.app_context():
        from app.utils.security import generate_confirmation_token

        # Create inactive user
        inactive_user = User(
            email='inactive@example.com',
            password='password123'
        )
        db.session.add(inactive_user)
        db.session.commit()

        # Generate confirmation token
        token = generate_confirmation_token(inactive_user.email)

        # Try to confirm email
        response = client.get(f'/auth/confirm/{token}', follow_redirects=True)
        assert response.status_code == 200
        assert b'Your account has been confirmed' in response.data

        # Check that user is now active
        user = User.query.filter_by(email='inactive@example.com').first()
        assert user.is_active is True

def test_reset_password_request(client, test_user):
    """Test password reset request functionality"""
    response = client.post('/auth/reset-password-request', data={
        'email': 'test@example.com'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Check your email for instructions' in response.data