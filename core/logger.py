import json
import logging
import sys
from datetime import datetime, timezone
from core.config import settings


class JsonFormatter(logging.Formatter):
    """Custom formatter to output system logs in a structured JSON format."""

    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "environment": settings.ENVIRONMENT,
        }

        # Include exception details if present
        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_object)


def setup_logging():
    """Initializes and overrides the root logger to use structured JSON."""
    root_logger = logging.getLogger()

    # Clear existing handlers to prevent duplicate lines in Uvicorn
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Set threshold level from config
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    # Stream to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JsonFormatter())
    root_logger.addHandler(console_handler)

    # Suppress verbose external libraries if necessary
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


# Execute setup during initialization
setup_logging()
logger = logging.getLogger(settings.APP_NAME)