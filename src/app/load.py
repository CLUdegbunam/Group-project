import boto3
import os
import psycopg2


def get_ssm_parameters_under_path(path: str) -> dict:
    ssm_client = boto3.client("ssm", region_name="eu-west-1")
    response = ssm_client.get_parameters_by_path(
        Path=path,
        Recursive=True,
        WithDecryption=True
    )
    formatted_response = {os.path.basename(x["Name"]):x["Value"] for x in response["Parameters"]}
    return formatted_response

def connect_to_redshift():  

    creds = get_ssm_parameters_under_path("/team5/redshift")


def run_db(sql, creds):
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

    