import pandas as pd
import datetime
from datetime import datetime
import calendar
from dash_application.config import config
import psycopg2

def input_data():
    month = str(datetime.now().strftime('%B'))
    try:
        # Establish a connection to the database by creating a cursor object
        # Obtain the configuration parameters
        params = config()
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # Create a new cursor
        cur = conn.cursor()
        # A function that takes in a PostgreSQL query and outputs a pandas database 
        def create_pandas_table(sql_query, database = conn):
            table = pd.read_sql_query(sql_query, database)
            return table
        # Utilize the create_pandas_table function to create a Pandas data frame
        # Store the data as a variable
        sme_main = create_pandas_table("SELECT * FROM sme_main")
        # Close the cursor and connection to so the server can allocate
        # bandwidth to other requests
    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    # finally:
    #     # closing database connection.
    #     if conn:  
    #         cur.close()
    #         conn.close()
    #         print("PostgreSQL connection is closed")
  
    sme_main['order_date']=pd.to_datetime(sme_main['order_date'],format='%Y-%m-%d')
    sme_main['day'] = pd.DatetimeIndex(sme_main['order_date']).day
    sme_main['year'] = pd.DatetimeIndex(sme_main['order_date']).year
    sme_main['month']= pd.DatetimeIndex(sme_main['order_date']).month
    sme_main['week'] = (sme_main['order_date'].dt.strftime('%W').astype(int) )
    sme_main['month_name'] = sme_main['month'].apply(lambda x: calendar.month_name[x])
    sme_main['driver_fee'] = sme_main['order_delivery_fees']*0.7
    sme_main['halan_return'] = sme_main['order_delivery_fees']*0.3
    sme_main['sme_return'] = sme_main['order_value'] - sme_main['order_delivery_fees']
    return sme_main


def insert_data(records):
    params = config()
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**params)
        # Create a new cursor
        cursor = connection.cursor()

        postgres_insert_query = """ INSERT INTO sme_main (order_id, client_contact_no, client_city, client_address,sme_name,driver_name,order_delivery_fees,order_value,order_status,order_reason_of_failure,order_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        record_to_insert = records
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
  
 
def update_data(records):
    params = config()
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**params)
        # Create a new cursor
        cursor = connection.cursor()
       
      
      
        postgres_insert_query = """ Update  sme_main set driver_name= %s,order_delivery_fees= %s,order_value= %s,order_status= %s,order_reason_of_failure= %s,order_date= %s where order_id= %s"""
        record_to_insert = records
        cursor.execute(postgres_insert_query, record_to_insert )

        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
  
  