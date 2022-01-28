
def create_db():
    sql = "CREATE DATABASE Cafe_Orders";
    return sql

def create_tables():
    sql = """  
    CREATE TABLE IF NOT EXISTS Item (
        Item_ID SMALLSERIAL PRIMARY KEY,
        Item_Name VARCHAR(255) NOT NULL,
        Price FLOAT(2) NOT NULL
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
        Branch VARCHAR(255) NOT NULL
    );
    CREATE TABLE IF NOT EXISTS Items_Ordered (
        Order_ID INT NOT NULL,
        Item_ID INT NOT NULL,
        Quantity INT NOT NULL,
        PRIMARY KEY (Order_ID, Item_ID)
    );



    INSERT INTO Item (
        Item_ID, Item_Name, Price
        )
        VALUES
        (DEFAULT, 'Regular Flavoured iced latte - Hazelnut', 2.75),
        (DEFAULT, 'Regular Flavoured iced latte - Caramel', 2.75),
        (DEFAULT, 'Regular Flavoured iced latte - Vanilla', 2.75),
        (DEFAULT, 'Large Flavoured iced latte - Hazelnut', 3.25),
        (DEFAULT, 'Large Flavoured iced latte - Caramel', 3.25),
        (DEFAULT, 'Large Flavoured iced latte - Vanilla', 3.25),
        (DEFAULT, 'Large Flat white', 2.45),
        (DEFAULT, 'Regular Flavoured latte - Hazelnut', 2.55),
        (DEFAULT, 'Regular Flavoured latte - Caramel', 2.55),
        (DEFAULT, 'Regular Flavoured latte - Vanilla', 2.55),
        (DEFAULT, 'Regular Latte', 2.15),
        (DEFAULT, 'Large Flavoured latte - Hazelnut', 2.85),
        (DEFAULT, 'Large Flavoured latte - Caramel', 2.85),
        (DEFAULT, 'Large Flavoured latte - Vanilla', 2.85),
        (DEFAULT, 'Regular Flat white', 2.15),
        (DEFAULT, 'Large Latte', 2.45);


    INSERT INTO Branches(
        Branch_ID, Branch
        )
        VALUES
        (DEFAULT, 'Chesterfield'),
        (DEFAULT, 'Kensington')
    """
    return sql
    
# USE Cafe_Orders
# SELECT Orders.Branch_ID, Branches.Branch
# FROM Branches
# INNER JOIN Orders ON Orders.Branch_ID = Branches.Branch_ID