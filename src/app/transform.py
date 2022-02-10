from app.extract import raw_data_extract as orders_from_csv
from app.load import run_db

order_id = 1

orders = []

unique_products = []
unique_branches = []

items = []
existing_branches = []

prices = []

quantities = []


def load_from_db():
    try:
        sql = "SELECT Branch FROM Branches"
        a = run_db(sql)
        for branch in a:
            if branch[0] not in unique_branches:
                unique_branches.append(branch[0])
                existing_branches.append(branch[0])

        sql = "SELECT Product_Name, Price FROM Products"
        b = run_db(sql)
        for item in b:
            if item[0] not in unique_products:
                unique_products.append(item[0])
                prices.append(item[1])
                items.append(item[0])

        sql = """SELECT Order_ID FROM Orders
                    ORDER BY Order_ID DESC"""

        all_ids = run_db(sql)
        order_id = all_ids[0][0] + 1    

    except Exception:
        pass

    id = order_id

    return id



def transform_data(orders_from_csv, order_id):
    for line in orders_from_csv:
            final_products = []
            test_for_products = []
            products = []
            test_for_products = line[3]

            if line[1] not in unique_branches:
                unique_branches.append(line[1])

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

                    if products[0] not in unique_products:
                        unique_products.append(products[0])
                        prices.append(pricess[0][-1])

                    final_products.append(products[0])
                                
            for i in final_products:
                orders.append({"id" : order_id, "Date_Time" : line[0], "Branch" : unique_branches.index(line[1])+1, "Product_Name" : unique_products.index(i)+1, "Quantity" : 0, "Total_Price" : line[4]})

                product = i
                counter = 0
                for i in final_products:
                    if product == i:
                        counter += 1
                quantities.append(counter)

            if x == 0:
                if '- ' in test_for_products:
                    products = test_for_products.rsplit(' - ', 1)
                    pricess.append(products[1])
                    products.remove(products[-1])
                    if products[0] not in unique_products:
                        unique_products.append(products[0])
                        prices.append(pricess[0])

                    final_products.append(products[0])
                    orders.append({"id" : order_id, "Date_Time" : line[0], "Branch" : unique_branches.index(line[1])+1, "Product_Name" : unique_products.index(products[0])+1, "Quantity" : 1, "Total_Price" : line[4]})
                    quantities.append(1)

            order_id += 1     

    return orders
    
    
def quantities_added(orders):
    for y, z in enumerate(orders):
        count = quantities[y]
        z["Quantity"] = count

    unique_orders = ([i for n, i in enumerate(orders) if i not in orders[n + 1:]])

    return unique_orders














# def seperate_products_ordered(orders):
#     for i in orders:
#         final_products = []
#         test_for_products = []
#         products = []
#         test_for_products = i[3]
#         if ', ' in i[3]:
#             test_for_products = i[3].split(', ')

#             x = 0
#             for product in test_for_products:
#                 pricess = []
#                 if '- ' in product:
#                     x =+ 1
#                     products = product.rsplit(' - ', 1)
#                     pricess.append(product.split(' - ', -2))
#                     products.remove(products[-1])

#                     if products[0] not in unique_products:
#                         unique_products.append(products[0])
#                         prices.append(pricess[0][-1])

#                     final_products.append(products[0])

#             if x == 0:
#                 if '- ' in test_for_products:
#                     products = test_for_products.rsplit(' - ', 1)
#                     pricess.append(products[1])
#                     products.remove(products[-1])
#                     if products[0] not in unique_products:
#                         unique_products.append(products[0])
#                         prices.append(pricess[0])


# def transform_raw_data(orders):
#     unique_orders = []
#     for i in orders:
#         for i[3] in i:
#             unique