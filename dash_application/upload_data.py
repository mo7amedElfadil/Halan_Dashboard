import pandas as pd
from dash_application.config import config
import psycopg2
import calendar

def clean_data(sme_main):
 
    sme_main.rename(columns={'Client Mobile NO': 'client_contact_no',
    'Order ID': 'order_id', 'Client City': 'client_city', 'Client Address': 'client_address', 
    'Business': 'sme_name',  'Status': 'order_status', 'Reason of failure': 'order_reason_of_failure', 
    'Driver': 'driver_name', 'Fees': 'order_delivery_fees', 'Order Value': 'order_value','Date': 'order_date'}, inplace=True)
    #Dropping irrelevant columns and those with null values,repeating values, and incorrect order_id
    sme_main.drop(['Count','Order Status','Business Address','Business City','Viecle','Client Zone'], axis=1, inplace=True)
    #Dropping negative order values, null or incorrect IDs and contact numbers and null client addresses
    sme_main = sme_main[sme_main['order_value']>=0]
    sme_main.dropna(subset=['order_id','client_contact_no','client_address'], inplace=True) 
    sme_main.drop(sme_main[(sme_main['order_id']< 100000) ].index,inplace=True)
    sme_main.drop(sme_main[(sme_main['order_id']> 999999) ].index,inplace=True)
    sme_main.drop(sme_main[(sme_main['client_contact_no']> 999999999) ].index,inplace=True)
    sme_main.drop(sme_main[(sme_main['client_contact_no']< 100000000) ].index,inplace=True)
    #One of the order statuses was null and after referring to the org, delivered was replaced
    sme_main[['order_status']] = sme_main[['order_status']].fillna('Delivered')
    #Formatting date
    try:
        sme_main['order_date']=pd.to_datetime(sme_main['order_date'],format='%Y-%m-%d')
    except:
        sme_main['order_date']=pd.to_datetime(sme_main['order_date'],format='%m/%d/%Y')
    #exporting the cleaned data to csv to then be uploaded into the database
    sme_main.to_csv('dash_application/csv/order_table.csv', index=False)
    #Creating new features
    sme_main['day'] = pd.DatetimeIndex(sme_main['order_date']).day
    sme_main['year'] = pd.DatetimeIndex(sme_main['order_date']).year
    sme_main['month']= pd.DatetimeIndex(sme_main['order_date']).month
    sme_main['week'] = (sme_main['order_date'].dt.strftime('%W').astype(int) + 1)
    sme_main['month_name'] = sme_main['month'].apply(lambda x: calendar.month_name[x])
    #calculating stakeholders individual shares
    sme_main['driver_fee'] = sme_main['order_delivery_fees']*0.7
    sme_main['halan_return'] = sme_main['order_delivery_fees']*0.3
    sme_main['sme_return'] = sme_main['order_value'] - sme_main['order_delivery_fees']

    return sme_main
   
def parseCSV(filePath,user_id):
    sme_main = pd.read_csv(filePath)
    sme_main = clean_data(sme_main)
    # sme_main.to_csv('dash_application/csv/sme_main.csv', index=False)

    with open('dash_application/csv/order_table.csv', 'r') as f:    
        params = config()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()        
        cmd = 'COPY sme_main(client_contact_no,order_id, client_city,client_address, sme_name,order_status,order_reason_of_failure,driver_name,order_delivery_fees, order_value, order_date) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
        cursor.copy_expert(cmd, f)
        conn.commit()


    