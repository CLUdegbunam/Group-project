import boto3
import os
import psycopg2
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO) 

def get_ssm_parameters_under_path(path: str) -> dict:
    ssm_client = boto3.client("ssm", region_name="eu-west-1")
    response = ssm_client.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True
    )
    formatted_response = {os.path.basename(x["Name"]):x["Value"] for x in response["Parameters"]}
    return formatted_response
    

def excute_sql(sql, creds):
    try:
        connection = psycopg2.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["db"],
            port = creds["port"]
        )
        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows != None:
            return rows
        cursor.close()
    
    except Exception:
        pass

    finally:
        connection.close()

def insert_column_values_products(product_list, creds): 
    for product in product_list:

        sql = f"""INSERT INTO Products(product_id, product_name, price)
            VALUES({product['product_id']}, '{product['product_name']}', {product['price']})
            """
        #print(sql)
        LOGGER.info(sql)
        excute_sql(sql, creds)

def insert_column_values_orders(orders_list, creds): 
    for order in orders_list:

        sql = f"""INSERT INTO orders(order_id, time-date, branch, total_price)
            VALUES({order['order_id']}, {order['time_date']},"{order['branch']}" {order['total_price']})
            """
        LOGGER.info(sql)
        excute_sql(sql, creds)

def insert_column_values_products_ordered(orders_list, creds): 
    for order in orders_list:

        sql = f"""INSERT INTO orders(order_id, time-date, branch, total_price)
            VALUES({order['order_id']}, {order['time_date']},"{order['branch']}" {order['total_price']})
            """
        LOGGER.info(sql)
        excute_sql(sql, creds)