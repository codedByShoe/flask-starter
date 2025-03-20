"""
Tasks to be executed by RQ workers
"""
import time
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def example_task(seconds):
    """
    Example task that sleeps for the specified number of seconds
    """
    logger.info(f"Starting example task, will sleep for {seconds} seconds")
    time.sleep(seconds)
    logger.info("Finished example task")
    return {"status": "success", "duration": seconds}

def process_data(data):
    """
    Example task that processes data
    """
    logger.info(f"Processing data: {data}")
    # Simulate processing
    time.sleep(2)
    result = {"processed": True, "input_length": len(data)}
    logger.info(f"Finished processing data, result: {result}")
    return result