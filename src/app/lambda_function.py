from enum import unique
import logging

import app.extract as extract
import boto3

# import app.transform as transform
from app.transform import load_from_db, transform_data, quantities_added
from app.load import get_ssm_parameters_under_path, insert_column_values_products, insert_column_values_branches, update_db

from app.transform import remove_payment_details, index_branches, index_products, separating_orders, count_products_ordered
from app.load import loading_branches, test_sql

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 


def lambda_handler(event, context):
    LOGGER.info(event)

    file_path = "/tmp/some_file.csv"

    s3_event = event["Records"][0]["s3"]
    bucket_name = s3_event["bucket"]["name"]
    object_name = s3_event["object"]["key"] 

    #LOGGER.info(f"Triggered by file {object_name} in bucket {bucket_name}")

    s3 = boto3.client("s3")
    s3.download_file(bucket_name, object_name, file_path)

    # creds = get_ssm_parameters_under_path("/team5/redshift")


    ## EXTRACT THE DATA

    data = extract.raw_data_extract(file_path)
    
    #print(data)
    #LOGGER.info(data[0])

    ## TRANSFORM THE DATA

    remove_payment_details(data)

    #print(data)

    branchdata = index_branches(data)

    print(branchdata)


    productsdata = index_products(data)

    print(productsdata)
 
    separatedorders = separating_orders(data)

    print(separatedorders)

    orders_counted_products = count_products_ordered(data)

    print(orders_counted_products)



    ## LOAD INTO AWS REDSHIFT


    creds = get_ssm_parameters_under_path("/team5/redshift")

    print(creds)

    
    id, order_id, unique_products, prices, unique_branches, existing_branches, items = load_from_db(creds)
    
    orders, unique_products, unique_branches, prices, quantities = transform_data(data, order_id, unique_branches, unique_products, prices)

    unique_orders = quantities_added(orders, quantities)

    #LOGGER.info(unique_orders)
    #LOGGER(f"First row is: {unique_orders[0]}")

    insert_column_values_products(unique_products, prices, items, creds)
    insert_column_values_branches(unique_branches, existing_branches, creds)
    update_db(id, unique_orders, creds)



    LOGGER.info(unique_branches)
    LOGGER.info(unique_products)


    #loading_branches(branchdata, creds)

    test_sql(creds)