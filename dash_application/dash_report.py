import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px

import numpy as np
import pandas as pd
import datetime
from datetime import datetime
import calendar


from config import config
import psycopg2

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

#calculating GMV
daily_gmv = sme_main.groupby('order_date')[['driver_fee', 'halan_return','sme_return','order_value']].sum().reset_index()
monthly_gmv =sme_main.groupby('month_name')[['driver_fee', 'halan_return','sme_return','order_value']].sum().reset_index()
weekly_gmv = sme_main.groupby('week')[['driver_fee', 'halan_return','sme_return','order_value']].sum().reset_index()
yearly_gmv = sme_main.groupby('year')[['driver_fee', 'halan_return','sme_return','order_value']].sum().reset_index()


sme_bus_grp = sme_main.groupby(["sme_name"])
stores_dict = {}

for x in sme_bus_grp:
    stores_dict[x[0]] = sme_bus_grp.get_group(x[0])['order_id'].count()

stores_df = pd.DataFrame.from_dict(stores_dict, orient='index',columns=[ 'order_count'])

sme_bus_list = sme_main['sme_name'].unique()
sme_asc = sme_main.groupby("sme_name")['order_status'].value_counts()
sme_asc = sme_asc.to_frame(name='status_breakdown')


sme_orders = pd.concat([sme_asc, stores_df], axis=0,sort=True)
stores_series = sme_asc.index.get_level_values('sme_name')
sme_asc['order_count'] = stores_df.loc[stores_series].values

sme_business = sme_main[['sme_name','order_status','order_date']]
sme_business = sme_business.groupby(['sme_name'])['order_status'].value_counts()

#display(sme_asc[sme_asc['status_breakdown']>=100]['status_breakdown'].unstack().plot.bar(legend=True,  title='Most Active SMEs'))




name = 'antique'
def store_stat(name):
    filt = sme_main['sme_name'] == name
    df = sme_main.loc[filt][['order_id','client_contact_no', 'client_address','order_status', 'order_delivery_fees', 'sme_return','order_date']]
    return df
    

client_city = pd.DataFrame(sme_main.groupby('client_city')['client_city'].value_counts()).rename(columns={'client_city': 'city_count'}).reset_index(level=1, drop=True).reset_index()

weekly_status = sme_main.groupby('week')['order_status'].value_counts()

weekly_fees = sme_main.groupby('week')['order_delivery_fees'].sum()

monthly_status = sme_main.groupby('month_name')['order_status'].value_counts()

monthly_fees = sme_main.groupby('month_name')['order_delivery_fees'].sum()

yearly_status = sme_main.groupby('year')['order_status'].value_counts()

yearly_fees = sme_main.groupby('year')['order_delivery_fees'].sum()

sme_delivered = sme_main.loc[sme_main['order_status'] == 'Delivered'].drop(['order_reason_of_failure'], axis=1)
sme_failed = sme_main.loc[sme_main['order_status'] != 'Delivered']

sme_driver_failed = sme_failed[['driver_name','order_id','order_status','order_value','order_delivery_fees','client_address','sme_name']].sort_values(['driver_name'], ascending=True)

sme_driver_delivered = sme_delivered[['driver_name','order_id','order_status','order_value','order_delivery_fees','client_address','sme_name']].sort_values(['driver_name'], ascending=True)


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
#month='June'
#orders_delivered_weekly  = orders_delivered_weekly[ (orders_delivered_weekly['month_name']==month)]


#Graph 5 Data
orders_status_monthly =pd.DataFrame(sme_main.groupby('month_name')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
#orders_status_monthly = orders_status_monthly[orders_status_monthly['month_name']==month]

#Grpah 6 Data
sme_status =sme_main[['sme_name','order_status','order_value','order_date']]
#sme_status =  pd.DataFrame(sme_main.groupby('sme_name')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()

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
#sme_asc = sme_asc.style.format({'daily_delivered_percentage': "{:.2%}"})
 
 
 #Graph 8 Data 
daily_count = pd.DataFrame(sme_main.groupby('order_date')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
dfx = pd.DataFrame(daily_count.groupby(['order_date'])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
daily_count = pd.merge(daily_count, dfx, on="order_date")
daily_count['status_percentage'] = daily_count['order_count']/daily_count['order_sum']

#Graph 9 Data
r_o_f = sme_main.dropna(subset=['order_reason_of_failure'])


app = dash.Dash()
css_styles =  {
    'background':'#111111',
     'text':'#7FDBFF',
  'blue':'#5e72e4',
  'indigo': '#5603ad',
  'purple': '#8965e0',
  'pink': '#f3a4b5',
  'red': '#f5365c',
  'orange': '#fb6340',
  'yellow': '#ffd600',
  'green': '#2dce89',
  'teal': '#11cdef',
  'cyan': '#2bffc6',
  'white': '#ffffff',
  'gray': '#6c757d',
  'gray1':'#202020',
  'gray2':'#323232',
  'gray-dark': '#32325d',
  'light': '#ced4da',
  'lighter': '#e9ecef',
  'primary': '#e14eca',
  'secondary': '#f4f5f7',
  'success': '#00f2c3',
  'info': '#1d8cf8',
  'warning': '#ff8d72',
  'danger': '#fd5d93',
  'light': '#adb5bd',
  'dark': '#212529',
  'default': '#344675',
  'white': '#ffffff',
  'neutral': '#ffffff',
  'darker': 'black',
  'breakpoint-xs': 0,
  'breakpoint-sm': '576px',
  'breakpoint-md': '768px',
  'breakpoint-lg': '992px',
  'breakpoint-xl': '1200px',
  'font-family-sans-serif':' -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
  'font-family-monospace':' SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace', 
  }
font1 ={'color': css_styles['text'],                
                'family' : css_styles['font-family-monospace'],
                'size' : 16,
                'color': css_styles['white'],
                }

div_style1 = {'backgroundColor':css_styles['light'], 'color':css_styles['dark'], 'border':'3px indigo solid', 'padding':10}

dates_list_of_dict = []

for month in sme_main['month_name'].unique():
    dates_list_of_dict.append({'label':str(month),'value': month})

sme_status_options = []

for status in sme_status['order_status'].unique():
    sme_status_options.append({'label':str(status),'value': str(status)})



app.layout = html.Div(
children=[ 
            
            html.H1('Halan SME Report', style={'textAlign':'center',
                                        'color':css_styles['darker'] ,
                                         'margin-bottom': '0.5rem',
                                        'font-family': css_styles['font-family-monospace'],
                                        'font-weight': '400',
                                        'line-height': '1.2',
                                        'border': '3px black solid',
                                        }),
           


 #Graph 1   
 html.Div([       
            dcc.Graph(id='orders_recieved_daily',
            figure={'data':[
                
                go.Scatter( x=orders_recieved_daily['order_date'],
                    y=orders_recieved_daily['order_count'],
                    dx=5,
                    dy=1,
                     text=orders_recieved_daily['order_count'],
                     textfont_size=14,
                textposition='top right',
                     mode='lines+markers+text',
                     marker = dict(
                         size = 12,
                        color= css_styles['cyan'],
                        symbol = 'circle',
                        
                       line = {'width': 2}
                     )
                     ,
                  )],

            'layout':go.Layout(
                title =  'Daily orders received',
                xaxis = dict(title = 'Order Date'),
                yaxis = dict(title = 'Order Count'),
                autosize = True,
                
                 
               plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                
                font= font1,
           ) }),

 ],style=div_style1
 ), 

html.Hr(),
html.Br(),
 #Graph 2
 html.Div([
            dcc.Graph(id='orders_recieved_weekly',
            figure={'data':[
                
                go.Bar( x=orders_recieved_weekly['week'],
                    y=orders_recieved_weekly['order_count'],
                     text=orders_recieved_weekly['order_count'],
                   
                  )],

            'layout':go.Layout(
                title =  'Daily orders received',
                xaxis = dict(title = 'Order Week'),
                yaxis = dict(title = 'Order Count'),
                plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                autosize = True,
                font= font1,
           ) }),
 ],style=div_style1
 ), 


html.Hr(),
html.Br(),

 #Graph 3
html.Div([
            dcc.Graph(id='orders_delivered_daily',
            figure={'data':[
                
                go.Scatter( x=orders_delivered_daily['order_date'],
                    y=orders_delivered_daily['order_count'],
                     text=orders_delivered_daily['order_count'],
                      textfont_size=14,
                textposition='top right',
                   mode='lines+markers+text',
                     marker = dict(
                         size = 12,
                        color= css_styles['cyan'],
                        symbol = 'circle',
                        
                       line = {'width': 2}
                     )
                     ,
                  )],
            'layout':go.Layout(
                title =  'Daily orders delivered',
             autosize = True,
                xaxis = dict(title = 'Order Date'),
                yaxis = dict(title = 'Order Count'),
               plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                
               font= font1,
           ) }),
 ],style=div_style1
 ), 


html.Hr(),
html.Br(),
 #Graph 4
 html.Div([
            dcc.Graph(id='orders_delivered_weekly',
            figure={'data':[
                
                go.Bar( x=orders_delivered_weekly['halan_week'],
                    y=orders_delivered_weekly['order_count'],
                    #color=orders_delivered_weekly["month_name"],
                    # barmode="group",
                     text=orders_delivered_weekly['order_count'],
                   
                  )],

            'layout':go.Layout(
                title =  'Weekly orders delivered',
                xaxis = dict(title = 'Halan Week'),
                yaxis = dict(title = 'Order Count'),
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           ) }),

 ],style=div_style1
 ), 


html.Hr(),
html.Br(),
 #Graph 5




 html.Div([
     html.Label('Please Select the month'),

     dcc.Dropdown(
          id='g5-dropdown',
         options = dates_list_of_dict,
         value=month,
         placeholder="Select a month",
     ),

    



            dcc.Graph(id='orders_status_monthly',
            figure={'data':[
                
                go.Bar( x=orders_status_monthly['order_status'],
                    y=orders_status_monthly['order_count'],
                    #color=orders_delivered_weekly["month_name"],
                    #barmode="group",
                     text=orders_status_monthly['order_count'],
                   
                  )],

            'layout':go.Layout(
                title =  'Monthly status comparison',
                xaxis = dict(title = 'Order Status'),
                yaxis = dict(title = 'Order Count'),
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           ) }),

 ],style=div_style1
 ), 



html.Hr(),
html.Br(),

 #Graph 6   
 html.Div([       
           
            dcc.Dropdown(id = 'sme_status_picker',options = sme_status_options, value = 'Delivered'),
              html.Br(),
             dcc.Graph(id='sme_status_comparison'),

 ],style=div_style1
 ), 


html.Hr(),
html.Br(),


 #Graph 7   
 html.Div([       
             dcc.Dropdown(id = 'sme_status_percentage_picker',options = sme_status_options, value = 'Delivered'),
               html.Br(),
            dcc.Graph(id='sme_status_percentage_comparison'),
            

 ],style=div_style1
 ), 

#Graph 8   
 html.Div([       
            html.Div([
 dcc.Dropdown(id ='daily_status_picker',options = sme_status_options, value = 'Delivered'),
            html.Hr(),
             dcc.RadioItems(id ='daily_status_percentage_picker',
                            options = [{'label': 'Number of orders','value': 'order_count'},
                                        {'label': 'Delivery percentage','value': 'status_percentage'}],
                             value = 'status_percentage',
                             ),
            ]),
            html.Br(),
           
            dcc.Graph(id='daily_status_comparison'),   



 ],style=div_style1
 ), 




            ],style=div_style1
            
    )


@app.callback(
    Output('sme_status_comparison', 'figure'),
    [Input('sme_status_picker', 'value')]
)


def update_figure_6(selected_status):
    filtered_sme_status = sme_status[sme_status['order_status']==selected_status]

    traces = []

    for sme_name in sme_status['sme_name'].unique():
        sme_graph_df = filtered_sme_status[filtered_sme_status['sme_name']==sme_name]
       
       
        traces.append(go.Scatter(
            x=sme_graph_df['order_value'],
            y=sme_graph_df['sme_name'],
            mode = 'markers',
            opacity =  0.7,
            marker = {'size':15},
            name = sme_name
        ))

    return {'data': traces,
            'layout':go.Layout(
                title =  'SME status comparison',
                xaxis = dict(title = 'Order Value'),
               hovermode= 'closest',
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           )}


@app.callback(
    Output('sme_status_percentage_comparison', 'figure'),
    [Input('sme_status_percentage_picker', 'value')]
)

def update_figure_7(selected_status):
    filtered_sme_status_percentage = sme_asc[sme_asc['order_status']==selected_status]

    traces = []

    for sme_name in sme_asc['sme_name'].unique():
        sme_percentage_graph_df = filtered_sme_status_percentage[filtered_sme_status_percentage['sme_name']==sme_name]
       
       
        traces.append(go.Scatter(
            y=sme_percentage_graph_df['status_percentage'], 
            x=sme_percentage_graph_df['sme_name'],
             textfont_size=14,
                textposition='bottom center',
            text = sme_percentage_graph_df['status_percentage'],
            texttemplate='%{text:.2%}',
            mode = 'markers+text',
            opacity =  0.7,
           
            marker = {'size':15},
            name = sme_name
        ))

    return {'data': traces,
            'layout':go.Layout(
                title =  'SME status percentage comparison. Selected Status:  ' + selected_status,
                yaxis = dict(tickformat= ',.2%',
                             range= [0,1]),
                xaxis= dict(title = 'Business Name'),
                hovermode= 'closest',
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           )}


@app.callback(
    Output('daily_status_comparison', 'figure'),
    [Input('daily_status_picker', 'value')],
    [Input('daily_status_percentage_picker', 'value')]
)

def update_figure_8(selected_status,selected_data):
    filtered_daily_status_percentage = daily_count[daily_count['order_status']==selected_status]

 
 
    if selected_data == 'status_percentage':

        return {'data':[ go.Scatter(
                y=filtered_daily_status_percentage[selected_data], 
                x=filtered_daily_status_percentage['order_date'],
                text = filtered_daily_status_percentage[selected_data],
                mode = 'lines+markers+text',
                opacity =  0.7,
            texttemplate='%{text:.2%}',
                marker = {'size':15, 'opacity':0.5,
                                'line':{'width':0.5,    'color':'white'} },
             textposition="top center",
                
            )],
                'layout':go.Layout(
                    title =  'Daily status percentage comparison. Selected Status:  ' + selected_status,
                    yaxis = dict(tickformat= ',.2%',
                                range= [0,1]),
                    xaxis= dict(title = 'Order date'),
                    hovermode= 'closest',
                plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    font= font1,
                   autosize = True, 
                    
            )}
    else:
        
        return {'data':[ go.Scatter(
                y=filtered_daily_status_percentage[selected_data], 
                x=filtered_daily_status_percentage['order_date'],
                text =filtered_daily_status_percentage[selected_data],
                mode = 'lines+markers+text',
                opacity =  0.7,
            
                marker = {'size':15, 'opacity':0.5,
                                'line':{'width':0.5,    'color':'white'} },
                  textposition="top center",
            )],
                'layout':go.Layout(
                    title =  'Daily status percentage comparison. Selected Status:  ' + selected_status,
                   
                    xaxis= dict(title = 'Order date'),
                    hovermode= 'closest',
                plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    font= font1,
                    autosize = True,
            )}



if __name__ == '__main__':
    app.run_server(debug=True)

