from dash import Dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

from datetime import datetime
from dash_application.input_data import input_data



from dash_application.static_dicts import  NAVBAR_STYLE, CONTENT_STYLE, theme, css_styles,card_style_1, card_style_2,c0,c2,features_graph_type,features_order_status,features_stakeholder,features_order_period, features,tab_style
from dash_application.dash_components import toggle_switch, dark_theme_provider, nav_bar
from dash_application.layouts import dashboard_layout, create_data_table_layout,report_layout



sme_main = input_data()



def create_dash_app_ddl(flask_app,base_pathname):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname=base_pathname,external_stylesheets =[dbc.themes.BOOTSTRAP] ) #['https://codepen.io/chriddyp/pen/bWLwgP.css']

    dash_app.layout = html.Div(id='dark-theme-provider-demo',
    children=[
            html.Br(),
            
           
            toggle_switch,

            html.Div(
                id='dark-theme-component-demo',
                children=[
                dark_theme_provider,
                ],
                style={'display': 'block', 'margin-left': 'calc(50% - 110px)'}

            ),



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
                dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Tab one', value='tab-1'),
                dcc.Tab(label='Tab two', value='tab-2'),
                ]),
                html.Div(id='tabs-content'),
                ],),


            html.Div([
                dcc.Checklist(id = 'select_modifiers',
                    options=[
                        {'label': 'Date', 'value': 'order_date'}, 
                        {'label': 'Business', 'value': 'sme_name'}, 
                        {'label': 'Order Value Range', 'value': 'order_value'},
                        {'label': 'Driver', 'value': 'driver_name'},
                    
                    ],
                    value=['order_date', 'sme_name'],
                    labelStyle={'display': 'inline-block'},
                        )
                    ],),



          
                dcc.Dropdown(
                options= [{'label':i, 'value': i } for i in features_order_status],
                multi=True,
                value="MTL",
                ),
               


            html.Div([
                    dcc.Slider(
                                min=-5,
                                max=10,
                                step=0.5,
                                value=-3,
                                )  
                ],),

                
             html.Div([
                    dcc.RadioItems(
                                options=[
                                {'label': 'New York City', 'value': 'NYC'},
                                {'label': 'Montréal', 'value': 'MTL'},
                                {'label': 'San Francisco', 'value': 'SF'},
                                ],
                                value='MTL',
                                #labelStyle={'display': 'inline-block'}
                                )
                ],),


            html.Div([
                                html.Div([
                                    dcc.DatePickerRange(
                                        id='date-picker-range',
                                        start_date=datetime(2021, 6, 1),
                                        end_date_placeholder_text='Select a date!',
                                    )


                                ])  
                        ],),
                
                        
            html.Div([
             dcc.Slider(
                        min=0,
                        max=9,
                        marks={i: 'Label {}'.format(i) for i in range(10)},
                        value=5,
                        )
                ],),


                            
            html.Div([
                dcc.RangeSlider(
                        count=1,
                        min=-5,
                        max=10,
                        step=0.5,
                        value=[-3, 7],
                        )
                    ],),

            
                html.Div([
                dcc.RangeSlider(
                        marks={i: 'Label {}'.format(i) for i in range(-5, 7)},
                        min=-5,
                        max=6,
                        value=[-3, 4],
                        )
                    ],),

                
                    html.Div([
                    dcc.Input(
                            placeholder='Enter a value...',
                            type='text',
                            value='',
                            )
                        ],),



                                    
                    html.Div([
                            dcc.Textarea(
                            placeholder='Enter a value...',
                            value='This is a TextArea component',
                            style={'width': '100%'},
                            )
                        ],),



            html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'selected_graph',
                                    options = [{'label':i, 'value': i } for i in features],
                                    value = 'Daily orders recieved',

                                ) ],
                                ),  html.Br(),
            ]),


         
     

            html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'graph_type',
                                    options = [{'label':i, 'value': i } for i in features_graph_type],
                                    value = 'order_status_count',

                                ) ],
                                ),  html.Br(),
            ]),
     
                    html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'order_status',
                                    options = [{'label':i, 'value': i } for i in features_order_status],
                                    value = 'Received',

                                ) ],
                                ),  html.Br(),
            ]),    
            
              html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'order_period',
                                    options = [{'label':i, 'value': i } for i in features_order_period],
                                    value = 'Daily',

                                ) ],
                                ),  html.Br(),
            ]),

               html.Div([
                    html.Div([
                                dcc.Dropdown(
                                    id = 'stakeholder',
                                    options = [{'label':i, 'value': i } for i in features_stakeholder],
                                    value = 'Halan',

                                ) ],
                                ),  html.Br(),
            ]),
                
                
                html.Div([
                            html.Button('Submit', id='button'),
                            
                            html.Div(id='output-container-button',
                            children='Enter a value and press submit'),
                            ]),  


                html.Div([
                        dcc.Graph(id='feature_graphic'),
                        
                        ], style=c2,
                        ),                          

                            ], style=c0,

                            )

    return dash_app


def create_dash_app(flask_app,base_pathname):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname=base_pathname,external_stylesheets = [dbc.themes.BOOTSTRAP])
    dash_app.layout = html.Div( id='div_0',
    children=[
            
                 
              
                    nav_bar(),
                    
       
         
            html.Div(
                id='dark-theme-component-demo',
                children=[
                            dashboard_layout,
                           
                        ],  style= tab_style
            )
               
            
    ],style=theme)

    return dash_app




def create_dash_app_datatable(flask_app,base_pathname):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname=base_pathname,external_stylesheets = [dbc.themes.BOOTSTRAP])
    dash_app.layout = html.Div( id='div_0',
    children=[
            
                    nav_bar(),
                   
            html.Div(
                id='dark-theme-component-demo',
                children=[
                       
                   create_data_table_layout(sme_main),
                   
                        ], style = tab_style,
            ),
               
            

    ],style=theme)

    return dash_app


    
def create_dash_app_report(flask_app,base_pathname):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname=base_pathname,external_stylesheets = [dbc.themes.BOOTSTRAP])
    dash_app.layout = html.Div( id='div_0',
    children=[
            
                    nav_bar(),
              
            html.Div(
                id='dark-theme-component-demo',
                children=[

                 report_layout,
                   
                        ], style = tab_style,
            ),
               
            

    ],style=theme)

    return dash_app