"""
RQ Worker script to run background tasks
"""
import os
import redis
from rq import Worker, Queue
import logging
from dotenv import load_dotenv
import sys

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get Redis connection string from environment
redis_url = os.getenv('VALKEY_URL', 'redis://localhost:6379/0')
logger.info(f"Connecting to Redis at {redis_url}")

# Define the queues to listen to
queue_names = ['default', 'email', 'high', 'low']

# Create a Flask app context for the worker
def create_app_context():
    """Create and return a Flask app context for use in worker jobs"""
    from run import app
    return app.app_context()

class FlaskContextWorker(Worker):
    """Worker that sets up a Flask application context for each job"""

    def perform_job(self, job, queue):
        """Set up Flask app context before performing a job"""
        logger.info(f"Setting up Flask app context for job {job.id}")
        with create_app_context():
            return super().perform_job(job, queue)

if __name__ == '__main__':
    try:
        # Connect to Redis
        conn = redis.from_url(redis_url)
        logger.info(f"Successfully connected to Redis")

        # Create queue instances
        queues = [Queue(name, connection=conn) for name in queue_names]
        logger.info(f"Created queues: {', '.join(queue_names)}")

        # Create and start worker with Flask context
        worker = FlaskContextWorker(queues)
        logger.info(f"Worker created, listening to queues: {', '.join(queue_names)}")
        logger.info(f"Email tasks will be processed through the 'email' queue")

        # Start the worker
        logger.info("Starting worker...")
        worker.work(with_scheduler=True)
    except Exception as e:
        logger.error(f"Worker failed to start: {e}")
        sys.exit(1)