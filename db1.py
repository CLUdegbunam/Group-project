def create_tables():
    sql = """  
    CREATE TABLE IF NOT EXISTS Item (
        Item_ID SMALLSERIAL PRIMARY KEY,
        Item_Name VARCHAR(255) NOT NULL,
        Price FLOAT(2) NOT NULL,
        UNIQUE (Item_Name)
    );

    CREATE TABLE IF NOT EXISTS Orders(
        Order_ID SMALLSERIAL,
        Date_Time timestamp NOT NULL,
        Branch_ID INT NOT NULL,
        Total_price FLOAT(2) NOT NULL,
        PRIMARY KEY (Order_ID, Branch_ID)
    );
    CREATE TABLE IF NOT EXISTS Branches (
        Branch_ID SMALLSERIAL PRIMARY KEY,
        Branch VARCHAR(255) NOT NULL,
        UNIQUE (Branch)
    );
    CREATE TABLE IF NOT EXISTS Items_Ordered (
        Order_ID SMALLSERIAL,
        Item_ID INT NOT NULL,
        PRIMARY KEY (Order_ID, Item_ID)
    );
    """
    return sql

def insert_column_values():    
            from orders_test import products123, price_for_product, run_db, Branchess
            for prices, item in enumerate(products123):
                price = price_for_product[prices]
                price = float(price)

                sql = F"""
                INSERT INTO Item 
                VALUES (
                DEFAULT, '{item}', {price}
                )
                ON CONFLICT DO NOTHING
                """
                run_db(sql)

            for Branch in Branchess:
                sql = f"""
                INSERT INTO Branches(
                Branch_ID, Branch
                )
                VALUES
                (DEFAULT, '{Branch}')
                ON CONFLICT DO NOTHING
            """
                run_db(sql)