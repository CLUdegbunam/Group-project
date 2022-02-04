import csv
import os
import psycopg2
from dotenv import load_dotenv

# TODO - better naming of variables
cafe50___25_08_2021___orders = []
# TODO - hard coded the file name! maybe this should be a method
with open("chesterfield_25-08-2021_09-00-00.csv", 'r') as chesterfield_cafe_orders:
    # TODO - You could use a dict reader?
    reader = csv.reader(chesterfield_cafe_orders)

    for line in reader:
        cafe50___25_08_2021___orders.append({"Date and Time" : line[0], "Location" : line[1], "Products and Prices" : line[3], "Total Price" : line[4]})

# TODO - this should be in the db module? import the db1.py and use the functionality in there.
load_dotenv()
host = os.environ.get("pg_host")
user = os.environ.get("pg_user")
password = os.environ.get("POSTGRES_PASSWORD")
database = os.environ.get("pg_db")

# TODO - this should be in the db.py module? and imported in?
def run_db(sql):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        connection.autocommit=True
        cursor = connection.cursor()
        cursor.execute(sql)

        cursor.close()
    finally:
        connection.close()

#  TODO - this is duplicate code from another file? 
def create_db():
    create_table = "CREATE DATABASE All_Orders"
    run_db(create_table)


def create_table():
    create_clean_table = """
    CREATE TABLE IF NOT EXISTS Orders
    (
    Orders_id SMALLSERIAL PRIMARY KEY NOT NULL,
    Date_and_Time varchar(255),
    Location varchar(255),
    Products_and_Prices varchar(555),
    Total_Price float(2)
    )
    """
    run_db(create_clean_table)

# TODO - you should be passing in the list as a parameter
def update_db():
    for order in cafe50___25_08_2021___orders:
        sql = f"""INSERT INTO Orders 
        (Orders_id, Date_and_Time, Location, Products_and_Prices, Total_Price) 
        VALUES 
        (DEFAULT, 
        '{order['Date and Time']}', 
        '{order['Location']}', 
        '{order['Products and Prices']}', 
        {order['Total Price']})
        """
        run_db(sql)


option = input("""
Enter '1' to create an All_Orders database,
Enter '2' to create an Orders table,
Enter '3' to add the orders to the table: 
""")

while True:
    if option == "":
        option = input("""
Enter '1' to create an All_Orders database,
Enter '2' to create an Orders table,
Enter '3' to add the orders to the table: 
        """)

    elif option == '1':
        create_db()
        break
    elif option == '2':
        create_table()
        break
    elif option == '3':
        update_db()
        break
