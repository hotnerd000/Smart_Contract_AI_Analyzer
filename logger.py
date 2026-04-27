import logging
import sys

def setup_logger():
    logger = logging.getLogger("agent")
    logger.setLevel(logging.INFO)

    # ✅ Force UTF-8 console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )

    # ✅ File handler with UTF-8
    file_handler = logging.FileHandler("agent.log", encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger