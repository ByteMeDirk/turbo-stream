"""
Date Handler Methods
"""
import logging
from datetime import datetime

from dateutil.relativedelta import relativedelta

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


def _is_integer(num):
    try:
        float(num)
    except ValueError:
        return False
    else:
        return float(num).is_integer()


def phrase_to_date(phrase, date_format="%Y-%m-%d"):
    """
    Takes a typical phrase such as "3_days_ago" and returns a
    date based on that phrase.
    :phrase: str. Something like 3_days_ago or 1_month_ago, 2_years_ago etc...
    :return: '%Y-%m-%d'
    """

    if phrase == "yesterday":
        return (datetime.now() - relativedelta(day=1)).strftime(date_format)

    if phrase == "today":
        return (datetime.now()).strftime(date_format)

    split_phrase = phrase.split("_")
    phrase_increment = split_phrase[0]
    phrase_period = split_phrase[1]

    try:
        if not _is_integer(phrase_increment):
            raise ValueError(
                f"The given configuration date phrase: {phrase} is not valid, "
                f"please use the format: <integer>_<period>_ago"
            )

        if phrase_period in ["day", "days"]:
            return (
                    datetime.now() - relativedelta(days=int(phrase_increment))
            ).strftime(date_format)

        if phrase_period in ["week", "weeks"]:
            return (
                    datetime.now() - relativedelta(weeks=int(phrase_increment))
            ).strftime(date_format)

        if phrase_period in ["month", "months"]:
            return (
                    datetime.now() - relativedelta(months=int(phrase_increment))
            ).strftime(date_format)

        if phrase_period in ["year", "years"]:
            return (
                    datetime.now() - relativedelta(years=int(phrase_increment))
            ).strftime(date_format)

        raise ValueError(
            f"The given configuration date phrase: {phrase} is not valid, "
            f"please use the format: <integer>_<period>_ago"
        )

    except ValueError as err:
        raise ValueError(
            f"The given configuration date phrase: {phrase} is not valid, "
            f"please use the format: <integer>_<period>_ago"
        ) from err
