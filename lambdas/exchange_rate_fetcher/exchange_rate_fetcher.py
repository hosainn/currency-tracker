"""Exchange rate fetcher lambda module"""

import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, _):
    """Lambda handler"""
    logger.info(json.dumps(event))

    return json.dumps(event)
