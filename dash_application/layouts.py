from dash import dash_table, html,dcc
import dash_bootstrap_components as dbc
from dash import dash_table
from datetime import datetime
import plotly.graph_objs as go
from dash_application.static_dicts import CONTENT_STYLE, tab_style,  h1_style,card_style_1,graph_style, dates_list_of_dict
from dash_application.data import data, report_data
from dash_application.dash_components import spinner_component,drop_down_dashboard_dynamic, drop_down_dashboard
from dash_application.plots import report_plots

month = str(datetime.now().strftime('%B'))


def create_data_table_layout():
    return html.Div(
      children=  [
          drop_down_dashboard(),
          html.Div(id ='table_container',children=[ ])
        ]
    )

def create_data_table(df):
    
    return dash_table.DataTable(id='data_table',
            columns = [{'names':i,'id':i} for i in df.columns],
            data = df.to_dict('records'),
            style_header=h1_style,
                style_table={'overflowX': 'scroll'},  
                style_cell={'minWidth': '80px', 'width': '180px',
                        'whiteSpace': 'normal','textAlign': 'left','padding': '5px'},                        
                         filter_action="native",
        sort_action="native",
        sort_mode="multi",
        selected_columns=[],
        selected_rows=[],
         page_action="native",
        page_current= 0,
        page_size= 20,

            )  


def create_report_layout_dynamic(sme_main):
    
    month='June'
    sme_main=sme_main[sme_main['month_name']==month]
    return html.Div(
        children=[ 

        
            html.H1('Halan SME Report for {}'.format(month), style=h1_style),
             
             dbc.Row([


                  dbc.Col([
                            html.H4('Select a month to generate the report for: '),
                        
                        ], width={'size':3,'offset':1},),

                 dbc.Col([
         
                        dcc.Dropdown(
                            id='g5-dropdown',
                            options = dates_list_of_dict,
                            value=month,
                            placeholder="Select a month",
                        
                            ),
                        
                        ], width={'size':3,},)


              ]),

          
        
          
           


 #Graph 1   
 html.Div([       
           spinner_component(    dcc.Graph(id='orders_Received_daily',style=card_style_1,
            figure=report_plots.plots(data.halan_dataframes(sme_main,'order_status_count','Received','Daily','Halan'),'Daily','Received')      
            ),)

 ],style=graph_style
 ), 

html.Hr(),
html.Br(),
 #Graph 2
 html.Div([
            spinner_component(   dcc.Graph(id='orders_Received_weekly',style=card_style_1,
            figure=report_plots.plots(data.halan_dataframes(sme_main,'order_status_count','Received','Weekly','Halan'),'Weekly','Received')      
           
           ),)
 ],style=graph_style
 ), 


html.Hr(),
html.Br(),

 #Graph 3
html.Div([
            spinner_component(  dcc.Graph(id='orders_delivered_daily',style=card_style_1,
            figure=report_plots.plots(data.halan_dataframes(sme_main,'order_status_count','Delivered','Daily','Halan'),'Daily','Delivered')      
            ),)
 ],style=graph_style
 ), 


html.Hr(),
html.Br(),
 #Graph 4
 html.Div([
            spinner_component(   dcc.Graph(id='orders_delivered_weekly',style=card_style_1,
            figure=report_plots.plots(data.halan_dataframes(sme_main,'order_status_count','Delivered','Weekly','Halan'),'Weekly','Delivered')      
            ),)

 ],style=graph_style
 ), 


html.Hr(),
html.Br(),
 #Graph 5




 html.Div([
    

    

 spinner_component(  
            dcc.Graph(id='orders_received_monthly',style=card_style_1,
            figure= report_plots.plots_bar(data.halan_dataframes(sme_main,'order_status_count','Received','Monthly','Halan'),'Halan','Monthly','order_status_count')
                 
                 
            ),)

 ],style=graph_style
 ), 



html.Hr(),
html.Br(),

 #Graph 6   
 html.Div([       
           
            spinner_component(  
             dcc.Graph(id='orders_delivery_percentage',style=card_style_1,
             figure= report_plots.plots_percentage(data.halan_dataframes(sme_main,'order_status_percentage','Delivered','Daily','Halan'),'Daily','Delivered')  
              
             ),)

 ],style=graph_style
 ), 


html.Hr(),
html.Br(),


 #Graph 7   
 html.Div([       
            
            spinner_component(   dcc.Graph(id='sme_status_percentage_comparison',style=card_style_1,
           figure=report_plots.plots_sunburst_percentage(data.halan_dataframes(sme_main,'order_status_percentage','Delivered','Monthly','SME'),'SME','Monthly','Delivered')                  
           
            ),)
            

 ],style=graph_style
 ), 

 #Graph 8   
 html.Div([       
            
            spinner_component(   dcc.Graph(id='drivers_status_percentage_comparison',style=card_style_1,
           figure=report_plots.plots_sunburst_percentage(data.halan_dataframes(sme_main,'order_status_percentage','Delivered','Monthly','Driver'),'Driver','Monthly','Delivered')    
           
            ),)
            

 ],style=graph_style
 ), 


#Graph 8
 html.Div([       
           
            spinner_component(   dcc.Graph(id='halan_ORF',style=card_style_1,
            figure=report_plots.plots_pie_traces(data.halan_dataframes(sme_main,"order_reason_of_failure",'Received','Monthly',"Halan"),"Halan",'Monthly')
                
            ),  ) 



 ],style=graph_style
 ), 




html.Hr(),
html.Br(), 

#Graph 8
 html.Div([       
           
        spinner_component(       dcc.Graph(id='sme_ORF',style=card_style_1,
            figure=report_plots.plots_pie_traces(data.halan_dataframes(sme_main,"order_reason_of_failure",'Received','Monthly',"SME"),"SME",'Monthly')
                
            ),   )



 ],style=graph_style
 ), 




html.Hr(),
html.Br(), 

#Graph 8
 html.Div([       
           
          spinner_component(     dcc.Graph(id='driver_ORF',style=card_style_1,
            figure=report_plots.plots_pie_traces(data.halan_dataframes(sme_main,"order_reason_of_failure",'Received','Monthly',"Driver"),"Driver",'Monthly')
                
            ),   )



 ],style=graph_style
 ), 




html.Hr(),
html.Br(), 

#Graph 9 
 html.Div([       
          spinner_component(    
            dcc.Graph(id='sme_status',style=card_style_1,
            figure=report_plots.plots_treemap(data.halan_dataframes(sme_main,"order_reason_of_failure",'Received','Monthly','SME'),'SME','Monthly')   
            
            ),   
          )


 ],style=graph_style
 ), 




html.Hr(),
html.Br(),

#Graph 10 
 html.Div([       
            spinner_component(  
            dcc.Graph(id='driver_status',style=card_style_1,
            figure=report_plots.plots_treemap(data.halan_dataframes(sme_main,"order_reason_of_failure",'Received','Monthly','Driver'),'Driver','Monthly')   
            
            ),  ) 



 ],style=graph_style
 ), 




html.Hr(),
html.Br(),



#Graph 11 
 html.Div([       
            spinner_component(  
            dcc.Graph(id='gmv_month',style=card_style_1,
            figure=  report_plots.plots_gmv(data.halan_dataframes(sme_main,"GMV",'Received','Monthly','Halan'),'Monthly') 
            
            
            ),   
            )


 ],style=graph_style
 ), 




html.Hr(),
html.Br(),


#Graph 12 
 html.Div([       
            spinner_component(  
            dcc.Graph(id='gmv_week',style=card_style_1,
            figure=  report_plots.plots_gmv(data.halan_dataframes(sme_main,"GMV",'Received','Weekly','Halan'),'Weekly') 
            
            
            ),   
            )


 ],style=graph_style
 ), 




html.Hr(),
html.Br(),


            ],style=CONTENT_STYLE,
            
    )



       
def create_dashboard_layout_dynamic(n_clicks):
    return html.Div( 
        children=[
            drop_down_dashboard_dynamic(n_clicks),         
            html.Div([
            dbc.Row([
                    dbc.Col([
            spinner_component(dcc.Graph(id={
                'type':'feature_graphic',
                'index': n_clicks,
            },
                style=card_style_1),),           
            ], width={'size':12,'offset':0},)
                ]),
            ], style=graph_style
            ),   
                ], style=CONTENT_STYLE

                )


def create_dashboard_layout():
    return html.Div(
                id='dark-theme-component-demo',
                children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Add Chart', id='add_chart', n_clicks=0, color="primary", className="me-1",style={'font-size':'14px'}),
                        ],width={'size':3,'offset':1}, align='center'),

                    ], justify='between'),
                     dbc.Row([
                        dbc.Col([
                            html.Div(children=[

                                html.Div(id='selectors', children=[]),
                            html.Div(id='container', children=[]),
                            ]),
                            
                        ]),

                    ]),
                        ],  style= tab_style
            )
                        

def container_component_layout(tab,df):
    
    if tab=='dashboard':
        return create_dashboard_layout()
    
    elif tab=='report':
        
        return create_report_layout_dynamic(df)
    elif tab=='data_table':
        
        return [create_data_table(df),create_data_table_layout()]
    else:
        return create_dashboard_layout()
