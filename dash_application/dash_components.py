

from datetime import date
from turtle import update
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import dash_daq as daq
from dash_application.input_data import input_data

from dash_application.static_dicts import features_graph_type,features_order_status,features_order_period,features_stakeholder
sme_main = input_data()






#####################################
# Create Auxiliary Components Here
#####################################
def slider_component(min, max,step, value, id):
    if id=='lag':
        return   dcc.Slider(
                            id=id+'_slider',
                            value=value,
                            step=step,
                            min=min,
                            max=max,
                            updatemode='mouseup',
                           
                            tooltip={'placement':'bottom'},
                            )
    else:
        return dcc.Slider(
                            id=id+'_slider',
                            value=value,
                            step=step,
                            min=min,
                            max=max,
                            updatemode='mouseup',
                            marks={i:i for i in range(min,max+step,step)},
                            tooltip={'placement':'bottom'},
                            )                        
def range_with_floats(start, stop, step):
    while stop > start:
        yield start
        start += step
def knob_component(min,max,value,id):
    return daq.Knob(
    id=id+'_knob',
  value=value,
    min=min,
    max=max,
)


def spinner_component(content):
    spin = dbc.Spinner(children=[content],  fullscreen=False,
          
            spinnerClassName="loader",
    )
         
    return spin


def drop_down_dashboard():
    return html.Div([ dbc.Row([
                dbc.Col([
                                dcc.Dropdown(
                                    id = 'graph_type',
                                    options = [{'label':i, 'value': i } for i in features_graph_type],
                                    value = 'order_status_count',
                     ) ,
                               
                     ] ,width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),
         
                dbc.Col([
                    
                    
                                dcc.Dropdown(
                                    id = 'order_status',
                                    options = [{'label':i, 'value': i } for i in features_order_status],
                                    value = 'Received',
                                        

                                ), 
                                
                     ], width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),
                dbc.Col([
        
                                dcc.Dropdown(
                                    id = 'order_period',
                                    options = [{'label':i, 'value': i } for i in features_order_period],
                                    value = 'Daily',
                                     


                                ) , 
                               

                      ], width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),  
                dbc.Col([    
                                dcc.Dropdown(
                                    id = 'stakeholder',
                                    options = [{'label':i, 'value': i } for i in features_stakeholder],
                                    value = 'Halan',
                                     
                                ) , 
                                 
                    ], width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),              
           
            ], justify='evenly'),
        ])
    

    
def drop_down_dashboard_dynamic(n_clicks):
    return html.Div(id= {
                        'type':"drop_down",
                        'index' : n_clicks,                                        
                    }, children=[ dbc.Row([
                dbc.Col([
                
            
                  
                            graph_type_dropdown(n_clicks),
                               
                     ] ,width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),
         
                dbc.Col([
                    
                    
                            order_status_dropdown(n_clicks), 
                                
                     ], width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),
                dbc.Col([
        
                            order_period_dropdown(n_clicks), 
                               

                      ], width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),  
                dbc.Col([    
                            stakeholder_dropdown(n_clicks), 
                                 
                    ], width={'size':3,'offset':0},xs =12,sm =6,md=3,lg =3, xl=3,xxl=3),              
           
            ], justify='evenly'),
        ])
 

 

def tabs_component():
    return html.Div([
                     dcc.Tabs(id="tabs", value='dashboard', 
                     persistence=True,persistence_type='session' ,children=[
                     dcc.Tab(label='Dashboard', value='dashboard'),
                     dcc.Tab(label='Report', value='report'),
                     dcc.Tab(label='Data Table', value='data_table'),
                     ]),
                     html.Div(id='tabs-content', children=[]),
                    ],)




def gauge_component(stakeholder,n_clicks,x):
    return daq.Gauge(
        id = {
            'type':stakeholder,
            'index' : n_clicks,                                        
        } ,
        label=stakeholder,
        value=x
    )

def graduated_bar_component(stakeholder,n_clicks,x):
    return daq.GraduatedBar(
        id = {
            'type':stakeholder,
            'index' : n_clicks,                                        
        } ,
        label=stakeholder,
        value=x
    )



def graph_type_dropdown(n_clicks,graph_type='order_status_count'):
    return   dcc.Dropdown(
                                    id ={
                                        'type':'graph_type',
                                        'index' : n_clicks,                                        
                                    } ,
                                    options = [{'label':i, 'value': j } for i,j in features_graph_type.items()],
                                    value = graph_type,
                                 

                                )

def order_status_dropdown(n_clicks):
    return  dcc.Dropdown(
                                    id ={
                                        'type':'order_status',
                                        'index' : n_clicks,                                        
                                    } , 
                                    options = [{'label':i, 'value': i } for i in features_order_status],
                                    value = 'Received',
                                 

                                )

def order_period_dropdown(n_clicks):
    return dcc.Dropdown(
                                    id = {
                                        'type':'order_period',
                                        'index' : n_clicks,                                        
                                    } ,
                                    options = [{'label':i, 'value': i } for i in features_order_period],
                                    value = 'Daily',
                                 


                                )
                             
def stakeholder_dropdown(n_clicks):
    return dcc.Dropdown(
                                    id ={
                                        'type':'stakeholder',
                                        'index' : n_clicks,                                        
                                    } , 
                                    options = [{'label':i, 'value': i } for i in features_stakeholder],
                                    value = 'Halan',
                                 
                                )