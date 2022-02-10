from app.extract import raw_data_extract as orders_from_csv
from load import run_db

# orders_from_csv = [{'date': '25/09/2021 10:00', 'location': 'Brighton', 'customer': 'John Smith', 'products': 'Hamburger - 2.75, Large Fries - 2.30, Large Fries - 2.30, Large Fries - 2.30, Kebab - 6.00', 'total_cost': '5.05', 'pay_method': 'CARD', 'card_no': '5494173772652516'},
# {'date': '25/09/2021 10:20', 'location': 'Brighton', 'customer': 'Michael Lewis', 'products': 'Steak - 7.30, Large Fries - 2.30', 'total_cost': '9.60', 'pay_method': 'CASH', 'card_no': ''}]


def load_from_db():
    try:
        unique_products = []
        prices = []

        unique_branches = []

        existing_branches = []
        items = []

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

        order_id = 1

        sql = """SELECT Order_ID FROM Orders
                    ORDER BY Order_ID DESC"""

        all_ids = run_db(sql)
        order_id = all_ids[0][0] + 1    
        order_id = 1
    except Exception:
        pass
    order_id = 1
    id = order_id

    return id, order_id, unique_products, unique_branches, existing_branches, items


def transform_data(orders_from_csv, order_id, unique_branches, unique_products, prices):
    orders = []
    
    quantities = []

    for line in orders_from_csv:
            final_products = []
            test_for_products = []
            products = []
            test_for_products = line["products"]

            if line["location"] not in unique_branches:
                unique_branches.append(line["location"])

            if ', ' in test_for_products:
                test_for_products = line["products"].split(', ')

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
                orders.append({"id" : order_id, "Date_Time" : line["date"], "Branch" : unique_branches.index(line["location"])+1, "Product_Name" : unique_products.index(i)+1, "Quantity" : 0, "Total_Price" : line["total_cost"]})

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
                    orders.append({"id" : order_id, "Date_Time" : line["date"], "Branch" : unique_branches.index(line["location"])+1, "Product_Name" : unique_products.index(products[0])+1, "Quantity" : 1, "Total_Price" : line["total_cost"]})
                    quantities.append(1)

            order_id += 1   

    return orders, unique_products, unique_branches, prices, quantities
    
    
def quantities_added(orders, quantities):
    for y, z in enumerate(orders):
        count = quantities[y]
        z["Quantity"] = count

    unique_orders = ([i for n, i in enumerate(orders) if i not in orders[n + 1:]])

    return unique_orders

order_id = load_from_db()[1]
# id2 = load_from_db()[0]
# print(order_id)
unique_products = load_from_db()[2]
unique_branches = load_from_db()[3]
prices = load_from_db()[4]

existing_branches = load_from_db()[6]
items = load_from_db()[5]

orders_test = transform_data(orders_from_csv, order_id, unique_branches)[0]
quantities = transform_data(orders_from_csv, order_id)[4]
unique_orders_test = quantities_added(orders_test, quantities)
# print(orders_test)
print(unique_orders_test)









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