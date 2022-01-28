import csv
import os
import psycopg2
from db1 import create_db, create_tables
from dotenv import load_dotenv


orders = []
items_ordered = []

products = []
final_products = []


with open("chesterfield_25-08-2021_09-00-00.csv", 'r') as chesterfield_cafe_orders:
    reader = csv.reader(chesterfield_cafe_orders)

    for line in reader:
        final_products = []
        test_for_products = []
        test_for_products = line[3]
        if ', ' in test_for_products:
            test_for_products = line[3].split(', ')

        x = 0
        for product in test_for_products:
            if '- ' in product:
                x =+1
                products = product.rsplit(' - ', 1)
                products.remove(products[-1])
                final_products.append(products[0])

        if x == 0:
            if '- ' in test_for_products:
                products = test_for_products.rsplit(' - ', 1)
                products.remove(products[-1])
                final_products.append(products[0])

            
        for product in final_products:
            orders.append({"Date_Time" : line[0], "Branch" : line[1], "Total_Price" : line[4]})
            items_ordered.append({"Item_Name" : product})


load_dotenv()
host = os.environ.get("pg_host")
user = os.environ.get("pg_user")
password = os.environ.get("POSTGRES_PASSWORD")
database = os.environ.get("pg_db")


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
        rows = cursor.fetchall()



        cursor.close()
    finally:
        connection.close()
    
    return rows


def load_id():
    for i in orders:
        sql = f"""
        SELECT Branch_ID {i['Branch']}
        FROM Branches
        """
        run_db(sql)


def update_db():
    
    for i in orders:
        sql = f"""
        SET datestyle = dmy;
        INSERT INTO Orders (
            Order_ID, Date_Time, Branch_ID, Total_Price
        )
        VALUES (
        DEFAULT,
        '{i['Date_Time']}',
        1,
        {i['Total_Price']}
        )
        """
        run_db(sql)

    

def abc():    
    for i in items_ordered:
        sql = f"""
        INSERT INTO Items_Ordered (
            Order_ID, Item_ID, Quantity
        )
        VALUES (
            DEFAULT,
            1,
            2
        )
        """
        run_db(sql)
        # '{i['Item_Name']}'

def display_orders():
    sql = """
    SELECT o.Order_ID, b.Branch, o.Date_Time, o.Total_Price
    FROM Branches b
    INNER JOIN Orders o ON o.Branch_ID = b.Branch_ID
    """
    print(run_db(sql))

option = input("""
Enter '1' to create an All_Orders database,
Enter '2' to create an Orders table,
Enter '3' to add the orders to the table: 
Enter '4' to display all the orders: 
""")

while True:
    try:
        if option == "":
            option = input("""
Enter '1' to create a Cafe_Orders database,
Enter '2' to create an Orders table,
Enter '3' to add the orders to the table,
Enter '4' to display all the orders: 
""")

        elif option == '1':
            sql = create_db()
            run_db(sql)
            break
        elif option == '2':
            sql = create_tables()
            run_db(sql)
            break
        elif option == '3':
            update_db()
            # abc()
            break
        elif option == '4':
            display_orders()
            break

    except Exception as e:
        print("Exception: ",e)
        break

# load_id()