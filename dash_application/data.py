import pandas as pd
from dash_application.static_dicts import features_order_period,features_stakeholder,features_order_status    
from dash_application.input_data import input_data
import datetime
from datetime import datetime

sme_main = input_data()
class report_data:
    
    #Graph 1 data
    orders_recieved_daily =pd.DataFrame(sme_main.groupby('order_date')['order_date'].value_counts()).reset_index(level=1, drop=True).rename(columns={'order_date': 'order_count'}).reset_index()



    #Graph 2 Data 
    orders_recieved_weekly =pd.DataFrame(sme_main.groupby('week')['week'].value_counts()).reset_index(level=1, drop=True).rename(columns={'week': 'order_count'}) .reset_index()


    #Graph 3 Data
    daily_order_status =pd.DataFrame(sme_main.groupby('order_date')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()

    option = 'Delivered'
    orders_delivered_daily = daily_order_status[ (daily_order_status['order_status']==option)].drop('order_status', axis=1)


    #Graph 4 Data
    sme_week = pd.DataFrame(sme_main.groupby(['day','month_name'])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
    option = 'Delivered'
    orders_delivered_weekly  = sme_week[ (sme_week['order_status']==option)].drop('order_status', axis=1)
    orders_delivered_weekly['halan_week'] = orders_delivered_weekly['day']
    orders_delivered_weekly['halan_week'] =orders_delivered_weekly['halan_week'].replace(range(1,9),'week 1')
    orders_delivered_weekly['halan_week'] =orders_delivered_weekly['halan_week'].replace(range(9,16),'week 2')
    orders_delivered_weekly['halan_week'] =orders_delivered_weekly['halan_week'].replace(range(16,23),'week 3')
    orders_delivered_weekly['halan_week'] =orders_delivered_weekly['halan_week'].replace(range(23,32),'week 4')
    orders_delivered_weekly = orders_delivered_weekly.drop('day', axis=1)
    orders_delivered_weekly = pd.DataFrame(orders_delivered_weekly.groupby(['month_name','halan_week'])['order_count'].sum()).reset_index()
  

    #Graph 5 Data
    orders_status_monthly =pd.DataFrame(sme_main.groupby('month_name')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
 
    #Graph 6 Data
    sme_status = pd.DataFrame(sme_main.groupby(['order_date','sme_name','order_status'])['sme_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'sme_name': 'order_count'}).reset_index()
   
    #Graph 7 Data
    sme_bus_grp = sme_main.groupby(["sme_name"])
    stores_dict = {}
    for x in sme_bus_grp:
        stores_dict[x[0]] = sme_bus_grp.get_group(x[0])['order_id'].count()

    stores_df = pd.DataFrame.from_dict(stores_dict, orient='index',columns=[ 'order_count'])

    sme_asc = sme_main.groupby("sme_name")['order_status'].value_counts()
    sme_asc = sme_asc.to_frame(name='status_breakdown')

    sme_orders = pd.concat([sme_asc, stores_df], axis=0,sort=True)
    stores_series = sme_asc.index.get_level_values('sme_name')
    sme_asc['order_count'] = stores_df.loc[stores_series].values
    sme_asc = sme_asc.reset_index()

    sme_asc['status_percentage'] = sme_asc['status_breakdown']/sme_asc['order_count']
       
    #Graph 8 Data 
    daily_count = pd.DataFrame(sme_main.groupby('order_date')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
    dfx = pd.DataFrame(daily_count.groupby(['order_date'])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
    daily_count = pd.merge(daily_count, dfx, on="order_date")
    daily_count['status_percentage'] = daily_count['order_count']/daily_count['order_sum']

    #Graph 9 Data
    r_o_f = sme_main.dropna(subset=['order_reason_of_failure'])

class data:    
    
    def halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder):
        if graph_type == 'order_status_count':
        #    
            if order_status =="Received":
            ##    
                if order_period =="Daily":
                ###    
                    if stakeholder =='Halan':
                    ####
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        orders_recieved_daily_driver = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder],])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()

                        return orders_recieved_daily_driver
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ######################
                elif order_period=='Weekly':
                ###
                    if stakeholder =='Halan':
                    ####
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                    ####
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                    ####
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df.nlargest(5,'order_count')
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df.nlargest(10,'order_count')
                #######################
                
            elif order_status =="Delivered":
                if order_period =="Daily":
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ########################
                elif order_period=='Weekly':
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                #########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ###########################
                
                
                return   
            elif order_status =="Cancelled":
                if order_period =="Daily":
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ########################
                elif order_period=='Weekly':
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                #########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ###########################

            elif order_status =="Hold":
                if order_period =="Daily":
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ########################
                elif order_period=='Weekly':
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                #########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df= pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby(features_order_period[order_period])[features_order_period[order_period]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_order_period[order_period]: 'order_count'}).reset_index()
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main[sme_main['order_status']==order_status].groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[features_stakeholder[stakeholder]].value_counts()).reset_index(level=1, drop=True).rename(columns={features_stakeholder[stakeholder]: 'order_count'}).reset_index()
                        return sme_df
                ###########################
            ###########################################################
       ####################################################
        elif graph_type == 'order_status_percentage':      
            if order_status =="Delivered":
                if order_period =="Daily":
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
                ########################
                elif order_period=='Weekly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]

                        return driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
                #########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        #halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
                ###########################
                
                
                return   
            elif order_status =="Cancelled":
                if order_period =="Daily":
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df

                ########################
                elif order_period=='Weekly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
           #########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                     
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df

                ###########################

            elif order_status =="Hold":
                if order_period =="Daily":
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
           ########################
                elif order_period=='Weekly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                        halan_df = halan_df[halan_df['order_status']== features_order_status[order_status]] 
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
          #########################
                elif order_period=='Monthly':
                    if stakeholder =='Halan':
                        halan_df = pd.DataFrame(sme_main.groupby(features_order_period[order_period])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(halan_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        halan_df = pd.merge(halan_df, dfx, on=features_order_period[order_period])
                        halan_df['status_percentage'] = halan_df['order_count']/halan_df['order_sum']
                        halan_df = halan_df.drop(['order_count','order_sum'], axis=1)
                      
                        return halan_df
                    elif stakeholder =='Driver':
                        driver_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(driver_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        driver_df = pd.merge(driver_df, dfx, on=features_order_period[order_period])
                        driver_df['status_percentage'] = driver_df['order_count']/driver_df['order_sum']
                        driver_df = driver_df.drop(['order_count','order_sum'], axis=1)
                        driver_df = driver_df[driver_df['order_status']== features_order_status[order_status]]
                        return  driver_df
                    elif stakeholder =='SME':
                        sme_df = pd.DataFrame(sme_main.groupby([features_order_period[order_period],features_stakeholder[stakeholder]])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
                        dfx = pd.DataFrame(sme_df.groupby(features_order_period[order_period])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
                        sme_df = pd.merge(sme_df, dfx, on=features_order_period[order_period])
                        sme_df['status_percentage'] = sme_df['order_count']/sme_df['order_sum']
                        sme_df = sme_df.drop(['order_count','order_sum'], axis=1)
                        sme_df = sme_df[sme_df['order_status']== features_order_status[order_status]]
                        return sme_df
         ###########################
            ###########################################################
       ############################################

        elif graph_type == 'order_reason_of_failure':
            if stakeholder == 'Halan':
                order_reason_of_failure = pd.DataFrame(sme_main.dropna(subset=[graph_type]).groupby([features_order_period[order_period]])[graph_type].value_counts()).rename(columns={graph_type: 'order_count'}).reset_index()
            else:
                order_reason_of_failure = pd.DataFrame(sme_main.dropna(subset=[graph_type]).groupby([features_order_period[order_period],features_stakeholder[stakeholder]])[graph_type].value_counts()).rename(columns={graph_type: 'order_count'}).reset_index()
            return order_reason_of_failure

        elif graph_type == 'GMV':
            sme_gmv = sme_main[sme_main['order_status']=='Delivered']
            sme_gmv =  sme_gmv.groupby(features_order_period[order_period])[['order_delivery_fees','driver_fee', 'halan_return','sme_return','order_value']].sum().reset_index().set_index(features_order_period[order_period])
            return sme_gmv



    def summary_data(sme_main,graph_type,date = '2021-06-01'):
        


        if graph_type=='today_orders':
            date = datetime.today().strftime("%Y-%m-%d")
            
            sme_df = pd.DataFrame(sme_main[sme_main['order_date']==date].groupby(['order_date'])['order_date'].value_counts()).reset_index(level=1, drop=True).rename(columns={'order_date': 'order_count'}).reset_index()

            try:
                return sme_df['order_count'][sme_df['order_date']==date][0]
            except:
                return 0


        elif graph_type=='week_orders':
         
            week=23
            
            sme_df = pd.DataFrame(sme_main[sme_main['week']==week].groupby(['week'])['week'].value_counts()).reset_index(level=1, drop=True).rename(columns={'week': 'order_count'}).reset_index()

            try:
                return sme_df['order_count'][sme_df['week']==week][0]
            except:
                return 0
            


            

        elif graph_type=='month_orders':
           
            month='June'
            sme_df = pd.DataFrame(sme_main[sme_main['month_name']==month].groupby(['month_name'])['month_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'month_name': 'order_count'}).reset_index()

            try:
                return sme_df['order_count'][sme_df['month_name']==month][0]
            except:
                return 0

        
        elif graph_type=="driver_summary":
            df =sme_main
            df =df[df['order_date']=='2021-06-01']
            df = pd.DataFrame(df.groupby(['order_date','driver_name',])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'driver_name': 'order_count'}).reset_index()

            df2 =sme_main[sme_main['order_status']=='Delivered']
            df2 =df2[df2['order_date']=='2021-06-01']
            df2 = pd.DataFrame(df2.groupby(['order_date','driver_name',])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'driver_name': 'order_count'}).reset_index()



            summary=[]
            for driver in df['driver_name'].unique():
                r= df['order_count'][df['driver_name']==driver].values[0]
                d = df2['order_count'][df2['driver_name']==driver].values[0]
                summary.append(f'{driver}: ')
                summary.append(f'Number of orders recieved today: {r}')
                summary.append(f'Number of orders Delivered today: {d} ')
            print(summary)


            return summary
                
        
 
        elif graph_type=="store_summary":
            df =sme_main
            df =df[df['order_date']=='2021-06-01']
            df = pd.DataFrame(df.groupby(['order_date','sme_name',])['sme_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'sme_name': 'order_count'}).reset_index()

            df2 =sme_main[sme_main['order_status']=='Delivered']
            df2 =df2[df2['order_date']=='2021-06-01']
            df2 = pd.DataFrame(df2.groupby(['order_date','sme_name',])['sme_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'sme_name': 'order_count'}).reset_index()



            summary=[]
            for store in df['sme_name'].unique():
                try:
                    r= df['order_count'][df['sme_name']==store].values[0]
                except:
                    r=0
                try:
                    d = df2['order_count'][df2['sme_name']==store].values[0]
                except:
                    d = 0
                summary.append(f'{store}: ')
                summary.append(f'Number of orders recieved today: {r}')
                summary.append(f'Number of orders Delivered today: {d} ')
            print(summary)


            return summary
                
        

        elif graph_type=="driver_summary_acc":
            df =sme_main
            df =df[df['order_date']=='2021-06-01']
            df = pd.DataFrame(df.groupby(['order_date','driver_name',])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'driver_name': 'order_count'}).reset_index()

            df2 =sme_main[sme_main['order_status']=='Delivered']
            df2 =df2[df2['order_date']=='2021-06-01']
            df2 = pd.DataFrame(df2.groupby(['order_date','driver_name',])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'driver_name': 'order_count'}).reset_index()

            df3 =sme_main[sme_main['order_status']=='Delivered']
            df3 =df3[df3['order_date']=='2021-06-01']
            df3 = pd.DataFrame(df3.groupby(['order_date','driver_name','order_delivery_fees'])['driver_name'].value_counts()).reset_index(level=1, drop=True).rename(columns={'driver_name': 'order_count'}).reset_index()
            df3['driver_cut']=df3['order_delivery_fees']*0.7*df3['order_count']
            df3 = pd.DataFrame(df3.groupby('driver_name')['driver_cut'].sum()).reset_index( )
           

            summary=[]
            for driver in df['driver_name'].unique():
                r= df['order_count'][df['driver_name']==driver].values[0]
                d = df2['order_count'][df2['driver_name']==driver].values[0]
                c = df3['driver_cut'][df3['driver_name']==driver].values[0]
                summary.append(f'{driver}: ')
                summary.append(f'Number of orders recieved today: {r}')
                summary.append(f'Number of orders Delivered today: {d} ')
                summary.append(f"Driver's Cut for the day : {c} ")
            print(summary)


            return summary
                
        