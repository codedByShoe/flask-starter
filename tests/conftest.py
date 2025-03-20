import pytest
import os
import tempfile
from app import create_app, db
from app.auth.models import User
from config import TestingConfig

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()

    # Create the Flask application with test config
    app = create_app(TestingConfig)

    # Configure the app for testing
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
    })

    # Create the database and the database tables
    with app.app_context():
        db.create_all()
        yield app

        # Teardown - cleanup and close database
        db.session.remove()
        db.drop_all()

    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Test client for our Flask app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Test CLI runner for our Flask app"""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Create a test user in the database"""
    with app.app_context():
        user = User(
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        user.is_active = True
        db.session.add(user)
        db.session.commit()

        return user

@pytest.fixture
def auth_client(client, test_user):
    """Client with authenticated user session"""
    client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password123',
    })
    return client