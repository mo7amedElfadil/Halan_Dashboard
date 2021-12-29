
from dash import Dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import flask

import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px

import numpy as np
import pandas as pd
import datetime
from datetime import datetime
import calendar

from dash_application.input_data import input_data

from dash_application.static_dicts import *
from dash_application.plots import *
 


  
# importing

  
sme_main = input_data()


def create_dash_app(flask_app):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname='/dashboard/')

    dash_app.layout = html.Div( 
    children=[


            html.H1('Halan SME DashBoard', style={'textAlign':'center',
                                        'color':css_styles['darker'] ,
                                         'margin-bottom': '0.5rem',
                                        'font-family': css_styles['font-family-monospace'],
                                        'font-weight': '400',
                                        'line-height': '1.2',
                                        'border': '3px black solid',}
                                        ),
            html.Br(),





 html.Div([
    dcc.Checklist(id = 'select_modifiers',
        options=[
            {'label': 'Date', 'value': 'order_date'}, 
            {'label': 'Business', 'value': 'sme_name'}, 
            {'label': 'Order Value Range', 'value': 'order_value'},
            {'label': 'Driver', 'value': 'driver_name'},
           
        ],
        value=['MTL', 'SF'],
             )
        ],),



 html.Div([
                    html.Div([
                         dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=datetime(2021, 6, 1),
                            end_date_placeholder_text='Select a date!'
                        )


                    ])  
            ],),
     


            html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'selected_graph',
                                    options = [{'label':i, 'value': i } for i in features],
                                    value = 'Daily orders recieved'

                                ) ],
                                ),  html.Br(),
            ]),
     
              
            

 html.Div([
           dcc.Graph(id='feature_graphic')
        
        ], style=c2
         ),     html.Br(), 
        

            ], style=c0

            )

      




   
    
    
    return dash_app





