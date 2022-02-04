import csv
import os
import psycopg2
from db1 import create_tables, insert_column_values_products, insert_column_values_branches
from dotenv import load_dotenv


order_id = 0

each_order_products = []
unique_orders = []

quantities = []
item_ids_with_quantity = []

Branchess = []
current_branches = []

products123 = []
items = []

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


def load_ids():
    try:
        sql = "SELECT Branch FROM Branches"
        a = run_db_with_return(sql)
        for branch in a:
            if branch[0] not in Branchess:
                Branchess.append(branch[0])
                current_branches.append(branch[0])

        sql = "SELECT Product_Name, Price FROM Products"
        b = run_db_with_return(sql)
        for item in b:
            if item[0] not in products123:
                products123.append(item[0])
                price_for_product.append(item[1])
                items.append(item[0])

        sql = """SELECT Order_ID FROM Orders
                 ORDER BY Order_ID DESC"""
        global order_id
        all_ids = run_db_with_return(sql)
        order_id = all_ids[0][0]
        order_id = int(order_id)

        return order_id 

    except Exception:
        pass

load_ids()

filename = "chesterfield_25-08-2021_09-00-00.csv"

with open(f"{filename}", 'r') as cafe_orders:
    reader = csv.reader(cafe_orders)

    for line in reader:
        final_products = []
        test_for_products = []
        products = []

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
        
        unique_orders.append({"Date_Time" : line[0], "Branch" : Branchess.index(line[1])+1, "Product_Name" : final_products, "Total_Price" : line[4]})

for i in unique_orders:
    indexes = []
    for y in i["Product_Name"]:
        indexes.append(products123.index(y)+1)
    each_order_products.append(indexes)
    
for i in each_order_products:   
    list = []
    for y in i:
        x = 0
        quantity = 0
        temp_number = y
        for y in i:
            if temp_number == i[x]:
                quantity += 1
            x += 1
        list.append(quantity)     
    quantities.append(list)

for i, y in enumerate(each_order_products):
    orders12345 = []
    z = quantities[i]
    for a, b in enumerate(z):
        c = y[a]
        orders12345.append({"Product_id" : c, "quantity" : b})

    item_ids_with_quantity.append([[i for n, i in enumerate(orders12345) if i not in orders12345[n + 1:]]])


def update_db():
    orderID = order_id + 1

    for i in unique_orders:
        sql = f"""
        SET datestyle = dmy;
        INSERT INTO Orders (
        Order_ID, Date_Time, Branch_ID, Total_Price)
        VALUES ({orderID}, '{i['Date_Time']}',
        {i["Branch"]}, {i["Total_Price"]})
        """
        run_db(sql)
        orderID += 1

    orderID = order_id + 1
    for i in item_ids_with_quantity:
        for y in i[0]:
            sql = f"""
            INSERT INTO Products_Ordered (
            Order_ID, Product_ID, Quantity)
            VALUES ({orderID}, {y["Product_id"]},
            {y["quantity"]})
            """
            run_db(sql)
        orderID += 1


sql = create_tables()
run_db(sql)

insert_column_values_products(products123, price_for_product, items, run_db)
insert_column_values_branches(Branchess, current_branches, run_db)

update_db()