from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from app.utils.security import hash_password, check_password


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime, nullable=True)

    def __init__(
        self, email, password, first_name=None, last_name=None, is_admin=False
    ):
        self.email = email.lower()
        self.password_hash = hash_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = hash_password(password)

    def activate(self):
        self.is_active = True
        db.session.commit()

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email

    def __repr__(self):
        return f"<User {self.email}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

