"""
Request Handler Methods & Wrappers
"""
import logging
import time
from functools import wraps
from random import random

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


def request_handler(wait: float = 1, backoff_factor: float = 0.5):
    """
    Wrapper to handle the request process.
    :param wait: Initial wait time.
    :param backoff_factor: Increase wait time by given factor.
    :return: None
    """

    def retry_decorator(function):
        @wraps(function)
        def func_with_retries(*args, **kwargs):
            _delay = wait * (1 + backoff_factor * random())
            logging.info(f"Waiting {_delay} seconds before attempt...")
            time.sleep(_delay)
            return function(*args, **kwargs)

        return func_with_retries

    return retry_decorator


def retry_handler(
        exceptions,
        total_tries: int = 4,
        initial_wait: float = 0.5,
        backoff_factor: int = 2,
        should_raise: bool = False,
):
    """
    Wrapper to handle the request process.
    :param exceptions: Exceptions to handle.
    :param total_tries: Total tries before raising an exception.
    :param initial_wait: Initial wait after first exception handled.
    :param backoff_factor: Increase wait period by given factor.
    :param should_raise: Bool raise exception after all tries.
    :return: None
    """

    def retry_decorator(function):
        @wraps(function)
        def func_with_retries(*args, **kwargs):
            tries = 1
            delay = initial_wait
            while True:
                try:
                    logging.info(f"Attempt {tries} of {total_tries}.")
                    return function(*args, **kwargs)
                except exceptions as exception:
                    if tries <= total_tries and should_raise:
                        raise Exception(
                            f"Function: {function.__name__}\n"
                            f"Failed despite best efforts after {total_tries} tries\n"
                            f"Exception {exception}."
                        )

                    logging.info(
                        f"Function: {function.__name__}\n"
                        f"Failed at {tries} tries, trying again in {delay} seconds...\n"
                        f"Exception {exception}."
                    )
                    tries += 1
                    time.sleep(delay)
                    delay = delay * backoff_factor

        return func_with_retries

    return retry_decorator
