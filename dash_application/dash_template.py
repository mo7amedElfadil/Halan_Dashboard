from dash import Dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash_application.input_data import input_data
from dash_application.static_dicts import   CONTENT_STYLE, tab_style 
from dash_application.dash_components import spinner_component, slider_component,tabs_component

sme_main = input_data()
 
def create_dash_app_tabbed(flask_app,base_pathname):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname=base_pathname,
    external_stylesheets = ['assets/bootstrap.min.css','assets/bWLwgP.css'],
    
    meta_tags=[ {'name': 'viewport', 'content': 'width=device-width, initial-scale=2.0, maximum-scale=1.2, minimum-scale=0.5,'}],
    )
    dash_app.title = "Dashboard"
    dash_app.layout = html.Div( 
    children=[

               
                 tabs_component(),
                 
          
                    
    ],style=CONTENT_STYLE)

    return dash_app

def create_reg_app(flask_app,base_pathname):
    dash_app = Dash(__name__, server = flask_app, url_base_pathname=base_pathname,
    external_stylesheets = ['assets/bootstrap.min.css','assets/bWLwgP.css'],
    
    meta_tags=[ {'name': 'viewport', 'content': 'width=device-width, initial-scale=2.0, maximum-scale=1.2, minimum-scale=0.5,'}],
    )
    dash_app.title = "Forecast"
    dash_app.layout = html.Div( 
    children=[

               
                          html.Div(
                id='dark-theme-component-demo',
                children=[
                   
                dbc.Row([
                        dbc.Col([
                            html.Div(children=[
                                 dbc.Row([
                        dbc.Col([
                         
                            dbc.Col([ 
                                dbc.Row([
                                dbc.Col( html.H2('Bias value:'),width={'size':2}),
                                dbc.Col([ dbc.Row([
                                    dbc.Col([slider_component(-10, 10, 1,1, 'bias'), ],width={'size':8,} ),
                                   dbc.Col([ html.H4(id='bias_value'),],width={'size':3,'offset':1}), ], ),
                                    html.H4("Changing the bias value affects the graph's gradient or elevation"),
                                 ],width={'size':10,} ),
                               ])
                                   
                            ]),
 
                            dbc.Col([

                                    dbc.Row([
                                dbc.Col(html.H2('Lag value:'),width={'size':2}),
                                dbc.Col([ dbc.Row([
                                    dbc.Col([slider_component(-2, 2, 0.01,0, 'lag'),],width={'size':8,} ),
                                    dbc.Col([ html.H4(id='lag_value'),],width={'size':3,'offset':1} ),]),
                                     html.H4('Changing the Lag value so affects the height and scale of the graph'),
                                 ],width={'size':10,} ),
                               ])
                                           
                                  
                            ]),
                           
                        
                          
                            
                        ],width={'size':11,'offset':1}),
                    

                    ]),
                                
                dbc.Row([
                        dbc.Col([
                          
                               spinner_component(dcc.Graph(id='reg_graphic',),),
                        ],width={'size':11,'offset':1}),

                    ]),

                            ]),
                            
                        ]),

                    ]),
                        ],  style= tab_style
            )
          
                    
    ],style=CONTENT_STYLE)

    return dash_app
