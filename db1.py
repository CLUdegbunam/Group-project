def create_tables():
    sql = """  
    CREATE TABLE IF NOT EXISTS Items (
        Item_ID SMALLSERIAL PRIMARY KEY,
        Item_Name VARCHAR(255) NOT NULL,
        Price FLOAT(2) NOT NULL,
        UNIQUE (Item_Name)
    );

    CREATE TABLE IF NOT EXISTS Orders(
        Order_ID INT NOT NULL PRIMARY KEY,
        Date_Time timestamp NOT NULL,
        Branch_ID INT NOT NULL,
        Total_Price FLOAT(2) NOT NULL
        
    );
    CREATE TABLE IF NOT EXISTS Branches (
        Branch_ID SMALLSERIAL PRIMARY KEY,
        Branch VARCHAR(255) NOT NULL,
        UNIQUE (Branch)
    );
    CREATE TABLE IF NOT EXISTS Items_Ordered (
        Order_ID INT NOT NULL,
        Item_ID INT NOT NULL,
        Quantity INT NOT NULL
    );
    """
    return sql


def insert_column_values():    
    from orders_test import products123, price_for_product, run_db, Branchess, current_branches, items
    for prices, item in enumerate(products123):
        price = price_for_product[prices]
        price = float(price)
        
        if item not in items:    
            sql = f"""
            INSERT INTO Items
            VALUES (
            DEFAULT, '{item}', {price}
            )
            ON CONFLICT DO NOTHING
            """
            run_db(sql)
            items.append(item)
    
    for Branch in Branchess:
        if Branch not in current_branches:    
            sql = f"""
            INSERT INTO Branches(
            Branch_ID, Branch)
            VALUES
            (DEFAULT, '{Branch}')
            """
            run_db(sql)
            current_branches.append(Branch)