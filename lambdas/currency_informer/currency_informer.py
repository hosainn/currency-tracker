"""Currency informer lambda module"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from enum import Enum

import boto3
import pytz
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DYNAMODB = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get("TABLE_NAME")

EXCHANGE_RATES_TABLE = DYNAMODB.Table(TABLE_NAME)


class CurrencyRateStatus(Enum):
    """
    Enum representing status levels for currency exchange rates.

    Attributes:
        HIGH (str): Indicates a high current rate compared to the previous rate.
        LOW (str): Indicates a low current rate compared to the previous rate.
        EQUAL (str): Indicates a equal current rate compared to the previous rate.
        NOT_AVAILABLE (str): Indicates that the rate is not available for the current date.
    """

    HIGH = "high"
    LOW = "low"
    EQUAL = "equal"
    NOT_AVAILABLE = "not_available"


def get_exchange_rates_status(current_rate, previous_rate):
    """
    Compare current and previous exchange rates and return a status.

    Parameters:
        current_rate: The current exchange rate.
        previous_rate: The previous exchange rate.

    Returns:
        The status of the current rate compared to the previous rate.
    """
    if current_rate is None:
        status = CurrencyRateStatus.NOT_AVAILABLE
    elif previous_rate is None:
        status = CurrencyRateStatus.NOT_AVAILABLE
    elif current_rate > previous_rate:
        status = CurrencyRateStatus.HIGH
    elif current_rate < previous_rate:
        status = CurrencyRateStatus.LOW
    else:
        status = CurrencyRateStatus.EQUAL

    return status.value

def get_exchange_rates(date):
    """
    Fetch exchange rates for a specific date.

    Parameters:
        date: Target date to retrieve exchange rates for.

    Returns:
        Dict of exchange rates for the given date.
    """
    response = EXCHANGE_RATES_TABLE.query(
        KeyConditionExpression=Key('date').eq(date)
    )
    if len(response["Items"]) and response["Items"][0]:
        rates = response['Items'][0].get("rates", {})
        return rates
    return {}


def get_currency_rates_and_status(current_date_only, previous_date_only):
    """
    Get currency rates and their status for the current and previous dates.

    Parameters:
        current_date_only: Date to get current exchange rates for.
        previous_date_only: Date to get previous exchange rates for.

    Returns:
        Dict of currency rates with their current and previous values and status.
    """
    current_rates = get_exchange_rates(current_date_only)
    previous_rates = get_exchange_rates(previous_date_only)

    currencies = {}

    for currency in current_rates.keys():
        current_rate = current_rates.get(currency)
        previous_rate = previous_rates.get(currency)

        status = get_exchange_rates_status(current_rate, previous_rate)

        currencies[currency] = {
            "current_rate": float(current_rate) if current_rate is not None else None,
            "previous_rate": float(previous_rate) if previous_rate is not None else None,
            "status": status
        }
    return currencies

def process_currency_information():
    """
    Process and return currency information with CET timestamps and exchange rates.

    Returns:
        Dict: API response with status code 200 and body containing timestamps and rates.
    """
    cet_timezone = pytz.timezone('CET')
    current_cet_datetime = datetime.now(timezone.utc).replace(
        microsecond=0, tzinfo=pytz.utc).astimezone(cet_timezone
                                                   )
    timestamp_cet = datetime.now(timezone.utc).replace(
        microsecond=0, tzinfo=pytz.utc).astimezone(cet_timezone
    ).isoformat()
    current_date_only = current_cet_datetime.strftime('%Y-%m-%d')
    previous_date_only = (current_cet_datetime - timedelta(days=1)).strftime('%Y-%m-%d')

    response = {
        "timestamp_cet": timestamp_cet,
        "current_date": current_date_only,
        "previous_date": previous_date_only,
        "exchange_rates": {}
    }

    currencies_status = get_currency_rates_and_status(
        current_date_only, previous_date_only
    )
    response["exchange_rates"] = currencies_status

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def handler(event, _):
    """Currency rate informer Lambda handler function."""
    if event.get("httpMethod", "") == "GET":
        try:
            return process_currency_information()
        except Exception as e:
            logger.error("Internal server error: %s", str(e))
            return {
                'statusCode': 500,
                'body': json.dumps({"message": "Internal server error"})
            }
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({"message": "Method Not Allowed"}),
            'headers': {'Allow': 'GET'}
        }