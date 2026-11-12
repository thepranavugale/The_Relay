
import logging
from pathlib import Path
from datetime import datetime

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Logs directory
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file name
LOG_FILE = LOG_DIR / "the_relay.log"


def setup_logger(name="TheRelay", level=logging.INFO):
    """
    Configure and return a logger.

    Logs are saved to a file and displayed
    in the terminal.
    """

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(level)
    logger.propagate = False

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Terminal handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create default project logger
logger = setup_logger()


# ---------------------------------------
# TEST FUNCTION
# ---------------------------------------

def main():

    print("=" * 45)
    print("THE RELAY - LOGGER TEST")
    print("=" * 45)

    test_logger = setup_logger("TheRelayTest")

    test_logger.info("The Relay application started.")
    test_logger.warning("This is a warning message.")
    test_logger.error("This is an error message.")

    try:
        result = 10 / 0

    except ZeroDivisionError:
        test_logger.exception(
            "An exception occurred during testing."
        )

    print("\nLogger test completed.")
    print(f"Log file location: {LOG_FILE}")


if __name__ == "__main__":
    main()
