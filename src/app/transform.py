#from app.extract import raw_data_extract #as orders_from_csv
from app.load import run_db

# orders_from_csv = [{'date': '25/09/2021 10:00', 'location': 'Brighton', 'customer': 'John Smith', 'products': 'Hamburger - 2.75, Large Fries - 2.30, Large Fries - 2.30, Large Fries - 2.30, Kebab - 6.00', 'total_cost': '5.05', 'pay_method': 'CARD', 'card_no': '5494173772652516'},
# {'date': '25/09/2021 10:20', 'location': 'Brighton', 'customer': 'Michael Lewis', 'products': 'Steak - 7.30, Large Fries - 2.30', 'total_cost': '9.60', 'pay_method': 'CASH', 'card_no': ''}]

#orders_from_csv = raw_data_extract 
#print(orders_from_csv())


def load_from_db(creds):
    try:
        unique_products = []
        prices = []

        unique_branches = []

        existing_branches = []
        items = []

        sql = "SELECT Branch FROM Branches"
        a = run_db(sql, creds)
        for branch in a:
            if branch[0] not in unique_branches:
                unique_branches.append(branch[0])
                existing_branches.append(branch[0])

        sql = "SELECT Product_Name, Price FROM Products"
        b = run_db(sql, creds)
        for item in b:
            if item[0] not in unique_products:
                unique_products.append(item[0])
                prices.append(item[1])
                items.append(item[0])

        order_id = 1

        sql = """SELECT Order_ID FROM Orders
                    ORDER BY Order_ID DESC"""

        all_ids = run_db(sql, creds)
        order_id = all_ids[0][0] + 1    
        order_id = 1
    except Exception:
        pass
    order_id = 1
    id = order_id

    return id, order_id, unique_products, prices, unique_branches, existing_branches, items


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

# order_id = load_from_db()[1]
# id2 = load_from_db()[0]
# print(order_id)
# unique_products = load_from_db()[2]
# unique_branches = load_from_db()[4]
# prices = load_from_db()[3]

# existing_branches = load_from_db()[5]
# items = load_from_db()[6]

# orders_test_list = transform_data(orders_from_csv, order_id, unique_branches, unique_products, prices)

# orders_test = orders_test_list[0]
# quantities = transform_data(orders_from_csv, order_id, unique_branches, unique_products, prices)[4]
# unique_orders_test = quantities_added(orders_test, quantities)
# # print(orders_test)
# print(unique_orders_test)









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



#remove payment details from data
def remove_payment_details(data):
    for item in data:
        keys_to_remove = ['pay_method', 'card_no']
        for key in keys_to_remove:
            del item[key]

    return data 

#index the branches of the fast food outlet
def index_branches(data):
    branches = []
    for item in data:
        branch = item['location']
        branchhash = hash(branch)
        branch_dict = {"id": branchhash, "branch" : branch}

        branches.append(branch_dict)
        uniqueBranches = list({object['id']:object for object in branches}.values())


    return uniqueBranches    


#index the products
def index_products(data):
    products = []
    for item in data:
        product = item['products']    
        product = product.split(', ')
        products.append(product)

        flatproducts=[]
        for sublist in products:
            for element in sublist:
                flatproducts.append(element)

        uniqueProducts = set(flatproducts)
        uniqueProducts = list(uniqueProducts)   

        result = []
        for item in uniqueProducts:
            val = item.rsplit(" - ", 1)
            #print (val)
            productdict = {}
            productdict['id'] = hash(val[0])
            productdict['product'] = val[0]
            productdict['price'] = val[1]
            #print(productdict)
            result.append(productdict)
            
   
       
    return result

        

#create data for orders table
def separating_orders(data):
    cleaned_orders = []
    for item in data:
        order_id = hash(item['customer'])
        date_time = item['date']
        branch_id = hash(item['location'])
        total_price = item['total_cost']

        new_item = {"order_id" : order_id, "date_time": date_time, "branch_id": branch_id, "total_price": total_price}

        cleaned_orders.append(new_item)

    return cleaned_orders    


def count_products_ordered(data):
    custinfo = []
    for item in data:
        
      
        order_id = hash(item['customer'])
        product = item['products']    
        products = product.split(', ')
    
     
        for p in products:
         
            val = p.rsplit(" - ", 1)

            product_id = hash(val[0])
            product_id = int(product_id)
            k = products.count(p)
            result = {'order_id':order_id, 'product':product_id, 'quantity': k}
    
            custinfo.append(result)


        unique_products_purchased=[]

        for i in custinfo:
            if i not in unique_products_purchased:
                unique_products_purchased.append(i) 
    
    return unique_products_purchased

