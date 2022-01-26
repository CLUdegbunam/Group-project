import psycopg2 
from configparser import ConfigParser
import config
from dotenv import load_dotenv
import os

load_dotenv()
host = os.environ.get("PostgreSQL_host")
user = os.environ.get("PostgreSQL_user")
password = os.environ.get("PostgreSQL_pass")
database = os.environ.get("PostgreSQL_db")

def config(filename='dotenv', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect_db():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=host, user=user, password=password, database=database, autocommit=True)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_db():
    create_table = "CREATE DATABASE All_Orders"
    connect_db(create_table)