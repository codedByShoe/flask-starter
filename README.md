# Flask Starter

A production-ready monolithic Flask application starter with authentication, background jobs, and more.

## Features

- User authentication with email verification
- Password reset functionality
- Background job processing with RQ and Valkey (Redis-compatible)
- SQLite for development (easily configurable for other databases)
- MailPit for testing emails
- Docker Compose setup for development dependencies
- Production-ready configurations

## Prerequisites

- Python 3.10+
- Docker and Docker Compose (optional, for running Valkey and MailPit)

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/codedbyshoe/flask-starter.git
cd flask-starter
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start required services (Valkey and MailPit)

```bash
docker-compose up -d
```

### 5. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your preferred settings
```

### 6. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Start the worker for background jobs

```bash
python -m app.jobs.worker
```

### 8. Run the application

```bash
flask run
```

## Running Tests

```bash
pytest
```

## Project Structure

```
flask-monolith-starter/
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore file
├── config.py              # Application configuration
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker build file (TODO)
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
├── start_worker.py        # Helper to start worker
├── app/                   # Application code
│   ├── __init__.py        # Application factory
│   ├── auth/              # Authentication module
│   ├── core/              # Core application module
│   ├── email/             # Email handling module
│   ├── jobs/              # Background jobs module
│   ├── static/            # Static files
│   ├── templates/         # HTML templates
│   └── utils/             # Utility functions
├── migrations/            # Database migrations
└── tests/                 # Test suite
```

## Development Workflow

### Adding New Models

1. Create new model classes in appropriate modules
2. Generate migrations: `flask db migrate -m "Add new model"`
3. Apply migrations: `flask db upgrade`

### Adding New Routes

1. Create new route functions in blueprint modules
2. Register routes with appropriate blueprint

### Adding Background Jobs

1. Define new task functions in `app/jobs/tasks.py`
2. Enqueue tasks using `current_app.task_queue.enqueue()`

## Production Deployment

For production deployment, consider the following:

1. Sqlite needs directory read and write access which needs to be taken into consideration based on deployment methods. If file system writing is not available for some reason consider services like Turso or PostgreSQL
2. Configure a proper SMTP server such as MailTrap, Sendgrid, SES, 00.
3. Use Gunicorn with something like Caddy for serving the application if on VPS or similar
4. Ensure `FLASK_ENV=production` is set in your environment
5. Generate a strong SECRET_KEY (TODO: create a script that does this automatically)
6. Enable HTTPS with proper certificates if using NGINX or similar

## Troubleshooting

### Email Issues

If you're having trouble with emails:

1. Check that MailPit is running: `http://localhost:8025`
2. Verify the worker is running: `python -m app.jobs.worker`

### Database Issues

For database issues:

1. Check that migrations are applied: `flask db current`
2. Verify database connection: `flask shell` and try `from app import db; db.engine.connect()`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
