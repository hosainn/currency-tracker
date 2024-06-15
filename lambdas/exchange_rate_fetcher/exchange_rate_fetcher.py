"""Exchange rate fetcher lambda module"""

import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from xml.etree import ElementTree

import boto3
import requests
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DYNAMODB = boto3.resource('dynamodb')
RETRY_COUNT = 3
TIMEOUT_IN_SECONDS = 10
REFERENCE_SITE_URL = os.environ.get("ECB_EXCHANGE_RATES_URL")
NAMESPACES_MAP = {'ns': os.environ.get("ECB_NAMESPACE_URL")}
TABLE_NAME = os.environ.get("TABLE_NAME")

@dataclass(frozen=True)
class Validation:
    """
    Encapsulates the response information.
    
    Attributes:
        is_valid (bool): True if the response was successful.
        status_code (int): The HTTP status code of the response.
        content (str): The content of the response.
    """
    is_valid: bool
    status_code: Optional[int]
    content: any

def fetch_exchange_rates():
    """
    Fetches the response from the ECB reference site with retry logic.
    
    Returns:
        Validation: Contains success status, status code, and content.
    """
    for attempt in range(RETRY_COUNT):
        status_code = content = None
        try:
            response = requests.get(REFERENCE_SITE_URL, timeout=TIMEOUT_IN_SECONDS)
            response.raise_for_status()

            status_code, content = response.status_code, response.text
            if status_code == 200 and content:
                return Validation(True, status_code, content)

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            logger.error("HTTP error occurred on attempt %s: %s", attempt + 1, e)
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error occurred on attempt %s: %s", attempt + 1, e)
        except requests.exceptions.Timeout as e:
            logger.error("Timeout occurred on attempt %s: %s", attempt + 1, e)
        except requests.RequestException as e:
            logger.error("An error occurred on attempt %s: %s", attempt + 1, e)

        time.sleep(1)

    content = "Failed to fetch exchange rates after multiple retries"

    return Validation(False, status_code, content)


def parse_exchange_rates_and_date(content_xml):
    """
    Parse exchange rates and date from the given XML content.

    Parameters:
        content_xml (str): XML content containing exchange rate data.

    Returns:
        Validation: Contains success status, status code, and content.

    Raises:
        ValueError: If exchange rates or date cannot be found in the XML.
        ElementTree.ParseError: If there's an error parsing the XML content.
    """

    try:
        root = ElementTree.fromstring(content_xml)
        cube = root.find('.//ns:Cube/ns:Cube', NAMESPACES_MAP)

        if cube is None:
            raise ValueError("No exchange rates found in the XML")

        date = cube.get('time')
        rates = {
            cube.get('currency'): Decimal(cube.get('rate'))
            for cube in cube.findall('ns:Cube', NAMESPACES_MAP)
        }
    except ValueError as ve:
        logger.error("Failed to parse exchages rates and date: %s", str(ve))
        return Validation(False, None, str(ve))

    except ElementTree.ParseError as pe:
        logger.error("Failed to parse exchages rates and date: %s", str(pe))
        return Validation(False, None, str(pe))

    return Validation(True, None, (date, rates))


def store_exchange_rate_to_db(date, rates):
    """
    Store exchange rates and date to DynamoDB table.

    Parameters:
        date (str): Date of the exchange rates.
        rates (dict): Dictionary containing currency rates
            with currency codes as keys and rates as Decimal objects.

    Returns:
        Validation: Contains success status, status code, and content.

    Raises:
        ClientError: If there's an error in the DynamoDB client operation.
    """
    try:
        table = DYNAMODB.Table(TABLE_NAME)
        current_datetime = datetime.now(timezone.utc).isoformat()
        table.put_item(
            Item={
                'date': date,
                'timezone': "CET",
                'rates': rates,
                'timestamp': current_datetime
            }
        )

    except ClientError as ce:
        logger.error("Failed to store exchages rates and date: %s", str(ce))
        return Validation(False, None, str(ce))

    logger.info("Storing exchange rates: %s for the date %s", rates, date)
    return Validation(True, None, True)


def get_and_store_exchange_rates():
    """
    Fetches exchange rates, parses them, and stores them in DynamoDB.
    
    Returns:
        Validation: Validation object indicating success or failure of the operation.
    """
    exchange_rates = fetch_exchange_rates()

    if not exchange_rates.is_valid:
        return exchange_rates

    parsed_exchange_rates_and_date = \
            parse_exchange_rates_and_date(exchange_rates.content)
    if not parsed_exchange_rates_and_date.is_valid:
        return parsed_exchange_rates_and_date

    date = parsed_exchange_rates_and_date.content[0]
    rates = parsed_exchange_rates_and_date.content[1]

    return store_exchange_rate_to_db(date, rates)


def handler(event, _):
    """
    Exchange rate fetcher lambda handler
    
    Parameters:
        event (dict): Event data passed to the Lambda function.
    """
    logger.info("Lambda event: %s", json.dumps(event))

    #TODO: Implement error handling to notify an SNS topic if an error occurs during
    #       fetching and storing exchange rates.

    get_and_store_exchange_rates()

    return
