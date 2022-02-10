from enum import unique
import logging

import app.extract as extract
import boto3

# import app.transform as transform
from app.transform import load_from_db, transform_data, quantities_added
from app.load import get_ssm_parameters_under_path, insert_column_values_products, insert_column_values_branches, update_db


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

    # creds = get_ssm_parameters_under_path("/team5/redshift")

    data = extract.raw_data_extract(file_path)
    
    LOGGER.info(data[0])
    
    id, order_id, unique_products, prices, unique_branches, existing_branches, items = load_from_db()
    
    orders, unique_products, unique_branches, prices, quantities = transform_data(data, order_id, unique_branches, unique_products, prices)

    unique_orders = quantities_added(orders, quantities)

    LOGGER.info(unique_orders[0])
    #LOGGER(f"First row is: {unique_orders[0]}")

    insert_column_values_products(unique_products, prices, items)
    insert_column_values_branches(unique_branches, existing_branches)
    update_db(id, unique_orders)