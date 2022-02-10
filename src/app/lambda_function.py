import logging

import app.extract as extract
import app.load as load
import boto3



LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 


def lambda_handler(event, context):
    LOGGER.info(event)

    file_path = "/tmp/some_file.csv"

    s3_event = event["Records"][0]["s3"]
    bucket_name = s3_event["bucket"]["name"]
    object_name = s3_event["object"]["key"] 

    LOGGER.info(f"Triggered by file {object_name} in bucket {bucket_name}")

    s3 = boto3.client("s3")
    s3.download_file(bucket_name, object_name, file_path)

    #Extract
    data = extract.raw_data_extract(file_path) 
    LOGGER.info(data[0])
    #Transform
    product_list = []
    #Load
    creds = load.get_ssm_parameters_under_path("/team5/redshift")
    insert_response = load.excute_sql(sql, creds)
    LOGGER.info(insert_response)