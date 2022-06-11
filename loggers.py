"""Loggers"""

# pylint: disable=C0103

import logging.config
import yaml


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
