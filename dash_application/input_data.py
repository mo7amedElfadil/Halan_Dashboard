import pandas as pd
import datetime
from datetime import datetime
import calendar

from dash_application.config import config
import psycopg2




def input_data():
    month = str(datetime.now().strftime('%B'))
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


    #sme_main = pd.read_excel('sme_sample2.xlsx')
    # Close the cursor and connection to so the server can allocate
    # bandwidth to other requests
    cur.close()
    conn.close()


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

