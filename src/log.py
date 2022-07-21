import json
import logging.config

from src.config import BASE_PATH


def setup_logging():
    with open(BASE_PATH / "conf" / "logging.json", "r") as f:
        conf = json.load(f)
    logging.config.dictConfig(conf)
