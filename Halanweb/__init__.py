from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


from dash import Dash



import dash_html_components as html

from dash_application.plots import *
from dash.dependencies import Input, Output

from dash_application import sme_main
from dash_application import create_dash_app










app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'




dash_app1 = create_dash_app(app)
dash_app2 = Dash(__name__, server = app, url_base_pathname='/reports/')
dash_app2.layout = html.Div([html.H1('Hi there, I am Dash2')])


@dash_app1.callback(
        Output('feature_graphic', 'figure'),
        [Input('selected_graph', 'value')],

    )

def update_state(choice):
        
    my_plot =report_plots.plots(choice,sme_main)
    return my_plot



        


from Halanweb import routes

