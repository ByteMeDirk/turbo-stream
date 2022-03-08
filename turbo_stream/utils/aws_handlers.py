import json
import logging

import boto3
import pandas as pd


def write_file_to_s3(bucket: str, key: str, data: (list[dict], str), profile_name=None):
    """
    Writes a file to s3. Json objects will be serialised before writing.
    :param bucket: The bucket to write to in s3.
    :param key: The key path and filename where the data will be stored.
    :param data: The data object to be written.
    :param profile_name: Optional AWS profile name.
    :return: None
    """
    logging.info(f"Attempting to write data to s3://{bucket}/{key}")

    if profile_name is None:
        boto3_session = boto3.Session()
    else:
        boto3_session = boto3.Session(profile_name=profile_name)

    s3_resource = boto3_session.resource("s3")
    s3_object = s3_resource.Object(bucket, key)
    data_frame = pd.DataFrame(data)
    file_fmt = key.split(".")[-1]

    if file_fmt == "json":
        data_frame = data_frame.to_json(orient="records")
        response = s3_object.put(Body=json.dumps(data_frame))
    elif file_fmt == "csv":
        data_frame = data_frame.to_csv(header=True)
        response = s3_object.put(Body=data_frame)
    elif file_fmt == "parquet":
        data_frame = data_frame.to_parquet()
        response = s3_object.put(Body=data_frame)
    else:
        response = s3_object.put(Body=data)

    return response
