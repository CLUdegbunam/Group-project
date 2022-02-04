import csv
import os
import psycopg2
from db1 import create_tables#, insert_column_values
from dotenv import load_dotenv

#  Why do you have so many global variables? 
order_id = 0

products = []
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

#  TODO - Duplicate code
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

# TODO - this is bad practice, do not load these into global variables. load at the time of need. and pass data around using parameters
def load_ids():
    try:
        # TODO - Separate these into individual methods.
        sql = "SELECT Branch FROM Branches"
        a = run_db_with_return(sql)
        for branch in a:
            if branch[0] not in Branchess:
                Branchess.append(branch[0])
                current_branches.append(branch[0])

        sql = "SELECT Item_Name, Price FROM Items"
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

    except Exception as e:
        pass
# TODO - loading into global variables is bad practice.
load_ids()

# TODO - put this into a function, passsing the file as a parameters
with open("chesterfield_25-08-2021_09-00-00.csv", 'r') as chesterfield_cafe_orders:
    reader = csv.reader(chesterfield_cafe_orders)

    for line in reader:
        final_products = []
        test_for_products = []

        test_for_products = line[3]
        if ', ' in test_for_products:
            test_for_products = line[3].split(', ')
        # TODO - bad naming of a variable. what does x mean? 
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
        # TODO - will this ever be invoked? x is incremented above?
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
        
        unique_orders.append({"Date_Time" : line[0], "Branch" : Branchess.index(line[1])+1, "Item_Name" : final_products, "Total_Price" : line[4]})
#  TODO - could this be its own function? that returns a list? 
for i in unique_orders:
    indexes = []
    for y in i["Item_Name"]:
        indexes.append(products123.index(y)+1)
    each_order_products.append(indexes)
#  TODO - could this be its own function that returns a list? 
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
#  TODO - could this be its own function that returns a list?
for i, y in enumerate(each_order_products):
    orders12345 = []
    # TODO - bad naming of variable
    z = quantities[i]
    for a, b in enumerate(z):
        c = y[a]
        orders12345.append({"id" : i+1, "item_id" : c, "quantity" : b})

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
            INSERT INTO Items_Ordered (
            Order_ID, Item_ID, Quantity)
            VALUES ({orderID}, {y["item_id"]},
            {y["quantity"]})
            """
            run_db(sql)
        orderID += 1


def display_all_orders():
    sql = """
    SELECT o.Order_ID, b.Branch, to_char(o.Date_Time, 'DD-MM-YYYY HH:MI'), it.Item_Name, io.Quantity, o.Total_Price
    FROM Orders o
    INNER JOIN Branches b ON b.Branch_ID = o.Branch_ID
    INNER JOIN Items_Ordered io ON o.Order_ID = io.Order_ID
    INNER JOIN Items it ON it.Item_ID = io.Item_ID
    """
    # TODO - why is this wrapped in ()
    orders = (run_db_with_return(sql))
    for order in orders:
        print({"Order_ID": order[0], "Branch": order[1], "Date and Time" : order[2], "Product Ordered" : order[3], "Quantity" : order[4], "Total Price" : order[5]})


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
            from db1 import insert_column_values
            insert_column_values()
            # run_db(sql)

        elif option == '3':  
            update_db()

        elif option == '4':
            display_all_orders()

        elif option == '0':
            break

    except Exception as e:
        print("Exception", e)
        break