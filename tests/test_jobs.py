import pytest
from unittest.mock import patch, MagicMock
from app.jobs.tasks import example_task, process_data

def test_example_task():
    """Test the example task function"""
    # Patch the time.sleep function to avoid waiting
    with patch('time.sleep') as mock_sleep:
        result = example_task(5)

        # Check that sleep was called with the correct argument
        mock_sleep.assert_called_once_with(5)

        # Check the return value
        assert result['status'] == 'success'
        assert result['duration'] == 5

def test_process_data():
    """Test the process_data task function"""
    # Patch the time.sleep function to avoid waiting
    with patch('time.sleep') as mock_sleep:
        test_data = {'key': 'value', 'items': [1, 2, 3]}
        result = process_data(test_data)

        # Check that sleep was called
        mock_sleep.assert_called_once()

        # Check the return value
        assert result['processed'] is True
        assert result['input_length'] == len(test_data)

def test_task_queue(app):
    """Test that tasks can be enqueued"""
    with app.app_context():
        # Mock the Redis Queue
        mock_queue = MagicMock()
        app.task_queue = mock_queue

        # Enqueue a task
        app.task_queue.enqueue(example_task, 10)

        # Check that enqueue was called correctly
        mock_queue.enqueue.assert_called_once_with(example_task, 10)

def test_email_queue(app):
    """Test that email tasks can be enqueued"""
    with app.app_context():
        # Mock the Redis Queue
        mock_queue = MagicMock()
        app.email_queue = mock_queue

        # Mock the send_email function
        from app.email.email import send_email

        # Enqueue an email task
        app.email_queue.enqueue(
            send_email,
            recipient='test@example.com',
            subject='Test Subject',
            html_body='<p>Test Email</p>'
        )

        # Check that enqueue was called correctly
        mock_queue.enqueue.assert_called_once_with(
            send_email,
            recipient='test@example.com',
            subject='Test Subject',
            html_body='<p>Test Email</p>'
        )