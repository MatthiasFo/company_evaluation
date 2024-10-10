import logging
import os
import sys


# Redirect print() to logging
class LoggerWriter:
    def __init__(self, level):
        # Set the log level (INFO, ERROR, etc.)
        self.level = level

    def write(self, message):
        # Only log if there's actually something to log
        if message.strip():  # Ignore empty lines
            self.level(message.strip())

    def flush(self):
        # This method is required for Python's output stream API
        pass


def setup_logging_for_cloud_and_local():
    # Logging configuration (place this at the top of your app.py)
    if os.getenv("ENVIRONMENT") == "production":
        # If on Google Cloud, use Cloud Logging
        import google.cloud.logging
        from google.cloud.logging.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        cloud_handler = CloudLoggingHandler(client)

        # Set up the root logger to use Cloud Logging
        logging.basicConfig(level=logging.INFO)
        root_logger = logging.getLogger()
        root_logger.addHandler(cloud_handler)
    else:
        # If running locally, print to console
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    sys.stdout = LoggerWriter(logging.info)
    sys.stderr = LoggerWriter(logging.error)

    logging.info("Application is starting...")
