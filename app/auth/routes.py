from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlparse

from app import db
from app.auth import bp
from app.auth.models import User
from app.auth.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
)
from app.auth.utils import (
    send_confirmation_email,
    send_password_reset_email,
    create_user,
)
from app.utils.security import confirm_token, verify_reset_token


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data or ""
        user = User.query.filter_by(email=email.lower()).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("Please confirm your email before logging in.", "warning")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        user.update_last_login()

        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("core.index")

        flash("You have been logged in successfully!", "success")
        return redirect(next_page)

    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("core.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = create_user(
            email=form.email.data,
            password=form.password.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )

        send_confirmation_email(user)

        flash(
            "Registration successful! Please check your email to confirm your account.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", title="Register", form=form)


@bp.route("/confirm/<token>")
def confirm_email(token):
    if current_user.is_authenticated and current_user.is_active:
        return redirect(url_for("core.index"))

    email = confirm_token(token)
    if not email:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.filter_by(email=email.lower()).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    if user.is_active:
        flash("Account already confirmed. Please login.", "info")
    else:
        user.activate()
        flash("Your account has been confirmed! You can now login.", "success")

    return redirect(url_for("auth.login"))


@bp.route("/reset-password-request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            send_password_reset_email(user)

        # Always show the same message to prevent user enumeration
        flash("Check your email for instructions to reset your password.", "info")
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password.html", title="Reset Password", form=form
    )


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    user_id = verify_reset_token(token)
    if not user_id:
        flash("The reset link is invalid or has expired.", "danger")
        return redirect(url_for("auth.login"))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("auth.login"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(
            "Your password has been reset. You can now log in with your new password.",
            "success",
        )
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password.html", title="Reset Password", form=form
    )

