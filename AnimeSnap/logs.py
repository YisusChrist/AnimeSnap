"""Logging configuration."""
import logging

from .consts import DEBUG, LOG_FILE, NAME

# Create a logger instance
logger = logging.getLogger(NAME)

# Define log handlers
log_handlers = [logging.FileHandler(LOG_FILE)]

# Set the log level and message format
log_level = logging.DEBUG if DEBUG else logging.INFO
log_format = "[%(asctime)s] %(levelname)s: %(message)s"

# If in debug mode, include additional information
if DEBUG:
    log_format += ": %(pathname)s:%(lineno)d in %(funcName)s"

# Configure the logging system
logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=log_handlers,
)
