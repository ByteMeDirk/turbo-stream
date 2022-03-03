import json
import logging

import boto3
import pandas as pd


def write_file_to_s3(bucket: str, key: str, data: list[dict], profile_name=None):
    """
    Writes a file to s3. Json objects will be serialised before writing.
    :param bucket:
    :param key:
    :param data:
    :param profile_name:
    :param file_format:
    :return:
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
        s3_object.put(Body=json.dumps(data_frame))
    elif file_fmt == "csv":
        data_frame = data_frame.to_csv(header=True)
        s3_object.put(Body=data_frame)
    elif file_fmt == "parquet":
        data_frame = data_frame.to_parquet()
        s3_object.put(Body=data_frame)
    else:
        s3_object.put(Body=data)
