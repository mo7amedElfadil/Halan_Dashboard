import calendar
import datetime

import pandas as pd
import datetime
from datetime import datetime
import calendar

import psycopg2




def input_data():
    month = str(datetime.now().date('%B'))
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
from configparser import ConfigParser


def config(filename=r'dash_application\database.ini', section='postgresql'):
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


def order_id_generator():
    latest = input_data()['order_id'].max()
    print(type(latest))
    print(datetime.today())
    w = datetime.today().strftime("%Y-%m-%d")[1]
    d = datetime.today().strftime("%Y-%m-%d")[2]//7 +1
    if int(latest[0:2])<w or not latest:
        x= '000'
        
        return f'{w}{d}{x:.3}'
    else:
        
        x=int(latest[-4:])+1
        x= str(x)
        y=int(latest[0:2])+1
        return f'{y}{d}{x:.3}'