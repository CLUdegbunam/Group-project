import logging

import app.extract as extract
import boto3

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 

def load_handler(event, context):
    ## LOAD INTO AWS REDSHIFT
    
    pass
    # creds = get_ssm_parameters_under_path("/team5/redshift")

    # #print(creds)
    # branchdata,productsdata,separatedorders,orders_counted_products = lambda_handler(event, context)


    # loading_branches(branchdata, creds)

    # loading_products(productsdata, creds)

    # loading_orders(separatedorders, creds)

    # loading_order_quantities(orders_counted_products, creds)
