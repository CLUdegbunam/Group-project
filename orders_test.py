import csv
from operator import index
import os
import psycopg2
from db1 import create_tables, insert_column_values
from dotenv import load_dotenv


orders = []
items_ordered = []

products = []
final_products = []

Branchess = []

products123 = []
price_for_product = []

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

        cursor.close()
    finally:
        connection.close()
    

def run_db_with_return(sql):
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
    try:
        sql = f"SELECT Branch FROM Branches"
        a = run_db_with_return(sql)
        for branch in a:
            if branch[0] not in Branchess:
                Branchess.append(branch[0])
    except Exception as e:
        pass

load_id()


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
            pricess = []
            if '- ' in product:
                x =+ 1
                products = product.rsplit(' - ', 1)
                pricess.append(product.split(' - ', -2))
                products.remove(products[-1])

                if products[0] not in products123:
                    products123.append(products[0])
                    price_for_product.append(pricess[0][-1])

                final_products.append(products[0])

        if x == 0:
            if '- ' in test_for_products:
                products = test_for_products.rsplit(' - ', 1)
                pricess.append(products[1])
                products.remove(products[-1])

                if products[0] not in products123:
                    products123.append(products[0])
                    price_for_product.append(pricess[0])

                final_products.append(products[0])

        if line[1] not in Branchess:
            Branchess.append(line[1])

        for product in final_products:
            orders.append({"Date_Time" : line[0], "Branch" : Branchess.index(line[1])+1, "Total_Price" : line[4]})
            items_ordered.append({"Item_Name" : (products123.index(product)+1)})


def update_db():
    
    for i in orders:
        sql = f"""
        SET datestyle = dmy;
        INSERT INTO Orders (
        Order_ID, Date_Time, Branch_ID, Total_Price)
        VALUES (DEFAULT, '{i['Date_Time']}',
        {i["Branch"]}, {i['Total_Price']})
        """
        run_db(sql)
        
    for i in items_ordered:
        sql = f"""
        INSERT INTO Items_Ordered (
        Order_ID, Item_ID)
        VALUES (DEFAULT, {i['Item_Name']})
        """
        run_db(sql)


def display_all_orders():
    sql = """
    SELECT o.Order_ID, b.Branch, to_char(o.Date_Time, 'DD-MM-YYYY HH:MI'), it.Item_Name, o.Total_Price
    FROM Orders o
    INNER JOIN Branches b ON b.Branch_ID = o.Branch_ID
    INNER JOIN Items_Ordered io ON o.Order_ID = io.Order_ID
    INNER JOIN Item it ON it.Item_ID = io.Item_ID

    """
    orders = (run_db_with_return(sql))
    for order in orders:
        print(order)


while True:
    option = input("""
Enter '1' to create all the tables,
Enter '2' to add the columns to the tables
Enter '3' to add the orders to the tables 
Enter '4' to display all the orders
Enter '0' to exit application: 
""")
    try:
        if option == '1':
            sql = create_tables()
            run_db(sql)
        elif option == '2':
            sql = insert_column_values()
            run_db(sql)
        elif option == '3':  
            update_db()
        elif option == '4':
            display_all_orders()
        elif option == '0':
            break

    except Exception as e:
        print("Exception: ",e)
        break