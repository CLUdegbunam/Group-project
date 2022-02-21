import logging
import os
import csv
import app.extract as extract
import boto3
import json

from app.load import get_ssm_parameters_under_path

from app.transform import remove_payment_details, index_branches, index_products, separating_orders, count_products_ordered
from app.load import loading_branches, loading_products, loading_orders, loading_order_quantities


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
    LOGGER.info(data[0])

    ## TRANSFORM THE DATA

    # remove_payment_details(data)

    #print(data)

    branchdata = index_branches(data)
    LOGGER.info(data[0])
    print(branchdata)


    productsdata = index_products(data)

    print(productsdata)
 
    separatedorders = separating_orders(data)

    print(separatedorders)

    orders_counted_products = count_products_ordered(data)

    print(orders_counted_products)


    base_filename = os.path.splitext(object_name)[0]

    sqs = boto3.client('sqs')

    send_file(s3, sqs, branchdata, "branches", base_filename + "_branches.csv")
    send_file(s3, sqs, productsdata, "products", base_filename + "_products.csv")
    send_file(s3, sqs, separatedorders, "orders", base_filename + "_orders.csv")
    send_file(s3, sqs, orders_counted_products, "products_ordered", base_filename + "_products_ordered.csv")

    
def send_file(s3, sqs, data_set, data_type: str, bucket_key: str):
    write_csv("/tmp/output.csv", data_set)
    LOGGER.info(f"Wrote local CSV for: {data_set}")

    bucket_name = "team5-transformed-cafe-data"
    s3.upload_file("/tmp/output.csv", bucket_name, bucket_key)
    LOGGER.info(f"Uploading to S3 into bucket {bucket_name} with key {bucket_key}")

    message = {
        "bucket_name" : bucket_name,
        "bucket_key" : bucket_key,
        "data_type" : data_type
    }
    
    sqs.send_message(
        QueueUrl='https://sqs.eu-west-1.amazonaws.com/123980920791/team5jack-load-queue',
        MessageBody=json.dumps(message)
    )



def write_csv(filename: str, data: list[dict[str, str]]):
    with open(filename, 'w') as csv_file:
        dict_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(data)






    ## LOAD INTO AWS REDSHIFT


    # creds = get_ssm_parameters_under_path("/team5/redshift")

    # #print(creds)

    # loading_branches(branchdata, creds)

    # loading_products(productsdata, creds)

    # loading_orders(separatedorders, creds)

    # loading_order_quantities(orders_counted_products, creds)

    # #test_sql(creds)

    # LOGGER.info("Completed execution")

    #return branchdata,productsdata,separatedorders,orders_counted_products
