from flask import current_app
from flask_mail import Message, Mail
import logging
from app import mail as app_mail

logger = logging.getLogger(__name__)

def send_email(recipient, subject, html_body, sender=None, text_body=None):
    """
    Send an email using the configured Flask-Mail instance.

    This function works both within and outside a Flask application context,
    making it suitable for use in background jobs.
    """
    try:
        # For logging purposes
        logger.info(f"Preparing to send email: Subject='{subject}' To='{recipient}'")

        # Use the sender if provided, otherwise try to get from config
        if sender is None:
            try:
                # Try to get from current_app if in application context
                sender = current_app.config['MAIL_DEFAULT_SENDER']
            except RuntimeError:
                # Outside application context, use a default
                sender = 'noreply@example.com'
                logger.info("Using default sender address as we're outside app context")

        # Create the message
        msg = Message(
            subject=subject,
            recipients=[recipient],
            html=html_body,
            sender=sender
        )

        if text_body:
            msg.body = text_body

        # Send the message
        # If we're outside the application context, we need to handle it differently
        try:
            # Try to use the already configured mail instance
            app_mail.send(msg)
            logger.info(f"Email sent successfully to {recipient}")
        except RuntimeError as e:
            # If that fails, log the error
            logger.error(f"Error using app_mail: {str(e)}")
            logger.info("Worker is outside application context - email cannot be sent")
            logger.info("Consider modifying worker.py to include application context")
            # Re-raise to ensure the job is marked as failed
            raise

        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        # Re-raise the exception to ensure the job fails properly
        raise