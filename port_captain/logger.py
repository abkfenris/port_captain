"""
Common logging configuration
"""
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

log_format = logging.Formatter("%(levelname)s - %(message)s")
stream_handler.setFormatter(log_format)

logger.addHandler(stream_handler)
