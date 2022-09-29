import json
import logging.config

from bot.config import Config


def setup_logging():
    with open(Config.base_dir / "conf" / Config.env / "logging.json", "r") as f:
        conf = json.load(f)
    logging.config.dictConfig(conf)
