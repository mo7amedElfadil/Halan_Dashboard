from dash import dash_table, html,dcc
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import datetime
import plotly.graph_objs as go
import pandas as pd
from dash_application.static_dicts import tab_selected_style, card_style_2, dates_list_of_dict,NAVBAR_STYLE, CONTENT_STYLE, css_styles, font1, div_style1,sme_status_options,c0,c2,features_graph_type,features_order_period,features_order_status,features_stakeholder
from dash_application.data import report_data

month = str(datetime.now().strftime('%B'))
### Layout 1
layout1 = html.Div([
    html.H2("Page 1"),
    html.Hr(),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                            html.H4('Example Graph Page'),
                            #create tabs
                            dbc.Tabs(
                                [
                                    #graphs will go here eventually using callbacks
                                    dbc.Tab(label='graph1',tab_id='graph1'),
                                    dbc.Tab(label='graph2',tab_id='graph2')
                                ],
                                id="tabs",
                                active_tab='graph1',
                                ),
                            html.Div(id="tab-content",className="p-4")
                            ]
                        ),
                    ],
                    width=6 #half page
                ),
                
                dbc.Col(
                    [
                        html.H4('Additional Components here'),
                        html.P('Click on graph to display text', id='graph-text')
                    ],
                    width=6 #half page
                )
                
            ],
        ), 
    ]),
])


### Layout 2
layout2 = html.Div(
    [
        html.H2('Page 2'),
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H4('Country'),
                                html.Hr(),
                                dcc.Dropdown(
                                    id='page2-dropdown',
                                    options=[
                                        {'label': '{}'.format(i), 'value': i} for i in [
                                        'United States', 'Canada', 'Mexico'
                                        ]
        ]
                                ),
                                html.Div(id='selected-dropdown')
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.H4('Fruit'),
                                html.Hr(),
                                dcc.RadioItems(
                                    id='page2-buttons',
                                    options = [
                                        {'label':'{}'.format(i), 'value': i} for i in [
                                        'Yes ', 'No ', 'Maybe '
                                        ]
                                    ]
                                ),
                                html.Div(id='selected-button')
                            ],
                        )
                    ]
                ),
            ]
        )
    ])


def create_data_table_layout(df):
    data_table_layout = html.Div(
      children=  [
            dash_table.DataTable(id='data_table',
            columns = [{'names':i,'id':i} for i in df.columns],
            data = df.to_dict('rows'),
            style_header={'backgroundColor': "#5e72e4",
                              'fontWeight': 'bolds',
                              'textAlign': 'center',},
                style_table={'overflowX': 'scroll'},  
                style_cell={'minWidth': '80px', 'width': '180px',
                        'whiteSpace': 'normal'},                        
                         filter_action="native",
        sort_action="native",
        sort_mode="multi",
                # row_selectable="multi",
                  selected_columns=[],
        selected_rows=[],
         page_action="native",
        page_current= 0,
        page_size= 20,

            ),
        ],style =CONTENT_STYLE
    )

    return data_table_layout


report_layout = html.Div(
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
                
                go.Scatter( x=report_data.orders_recieved_daily['order_date'],
                    y=report_data.orders_recieved_daily['order_count'],
                    dx=5,
                    dy=1,
                     text=report_data.orders_recieved_daily['order_count'],
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

 ],style=card_style_2
 ), 

html.Hr(),
html.Br(),
 #Graph 2
 html.Div([
            dcc.Graph(id='orders_recieved_weekly',
            figure={'data':[
                
                go.Bar( x=report_data.orders_recieved_weekly['week'],
                    y=report_data.orders_recieved_weekly['order_count'],
                     text=report_data.orders_recieved_weekly['order_count'],
                   
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
 ],style=card_style_2
 ), 


html.Hr(),
html.Br(),

 #Graph 3
html.Div([
            dcc.Graph(id='orders_delivered_daily',
            figure={'data':[
                
                go.Scatter( x=report_data.orders_delivered_daily['order_date'],
                    y=report_data.orders_delivered_daily['order_count'],
                     text=report_data.orders_delivered_daily['order_count'],
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
 ],style=card_style_2
 ), 


html.Hr(),
html.Br(),
 #Graph 4
 html.Div([
            dcc.Graph(id='orders_delivered_weekly',
            figure={'data':[
                
                go.Bar( x=report_data.orders_delivered_weekly['halan_week'],
                    y=report_data.orders_delivered_weekly['order_count'],
                    #color=orders_delivered_weekly["month_name"],
                    # barmode="group",
                     text=report_data.orders_delivered_weekly['order_count'],
                   
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

 ],style=card_style_2
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
                
                go.Bar( x=report_data.orders_status_monthly['order_status'],
                    y=report_data.orders_status_monthly['order_count'],
                    #color=orders_delivered_weekly["month_name"],
                    #barmode="group",
                     text=report_data.orders_status_monthly['order_count'],
                   
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

 ],style=card_style_2
 ), 



html.Hr(),
html.Br(),

 #Graph 6   
 html.Div([       
           
            dcc.Dropdown(id = 'sme_status_picker',options = sme_status_options, value = 'Delivered'),
              html.Br(),
             dcc.Graph(id='sme_status_comparison'),

 ],style=card_style_2
 ), 


html.Hr(),
html.Br(),


 #Graph 7   
 html.Div([       
             dcc.Dropdown(id = 'sme_status_percentage_picker',options = sme_status_options, value = 'Delivered'),
               html.Br(),
            dcc.Graph(id='sme_status_percentage_comparison'),
            

 ],style=card_style_2
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



 ],style=card_style_2
 ), 




html.Hr(),
html.Br(),



            ],style=CONTENT_STYLE
            
    )



dashboard_layout = html.Div( 
    children=[


        



            html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'graph_type',
                                    options = [{'label':i, 'value': i } for i in features_graph_type],
                                    value = 'order_status_count'

                                ) ],
                                ),  html.Br(),
            ]),
     
                    html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'order_status',
                                    options = [{'label':i, 'value': i } for i in features_order_status],
                                    value = 'Received'

                                ) ],
                                ),  html.Br(),
            ]),    
            
              html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'order_period',
                                    options = [{'label':i, 'value': i } for i in features_order_period],
                                    value = 'Daily'

                                ) ],
                                ),  html.Br(),
            ]),

               html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'stakeholder',
                                    options = [{'label':i, 'value': i } for i in features_stakeholder],
                                    value = 'Halan'

                                ) ],
                                ),  html.Br(),
            ]),
            
            

 html.Div([
           dcc.Graph(id='feature_graphic',style=c2)
        
        ], style=card_style_2
         ),     html.Br(), 
        

            ], style=CONTENT_STYLE

            )

          
