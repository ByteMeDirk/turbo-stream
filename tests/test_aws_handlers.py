"""
Test turbo_stream.utils.aws_handlers
"""
import unittest

import pytest
from botocore.exceptions import ParamValidationError

from turbo_stream.utils.aws_handlers import *


class TestAWSHandlers(unittest.TestCase):
    """
    Testing the AWS Handlers.
    """

    def test_write_file_to_s3(self):
        """
        Ensure the connection exists.
        """
        with pytest.raises(ParamValidationError):
            write_file_to_s3(
                bucket="test-bucket",
                key="test-key",
                data=[{"key": "value"}],
            )
