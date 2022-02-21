import logging
from app.load import get_ssm_parameters_under_path, loading_branches, loading_products, loading_orders, loading_order_quantities
import boto3
import csv

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 

def load_handler(event, context):
    ## LOAD INTO AWS REDSHIFT

    creds = get_ssm_parameters_under_path("/team5/redshift")
    # LOGGER.info(creds)
    # LOGGER.info(event)
    file_path = "/tmp/some_file.csv"

    s3_event = event["Records"][0]["body"]
    LOGGER.info(type(s3_event))
    LOGGER.info(s3_event)
    bucket_name = s3_event["bucket_name"]
    object_name = s3_event["bucket_key"]
    file_type = s3_event["data_type"]


    s3 = boto3.client("s3")
    s3.download_file(bucket_name, object_name, file_path)

    def load_csv_file(file_path):
        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            LOGGER.info(reader)
            return reader
        # for line in reader:

    data = load_csv_file(file_path)

    LOGGER.info(data[0])


    # if '_branches' in object_name:
    #     loading_branches(data, creds)

    # if '_products' in object_name:
    #     loading_products(data, creds)

    # if '_orders' in object_name:
    #     loading_orders(data, creds)

    # if '_products_ordered' in object_name:
    #     loading_order_quantities(data, creds)
