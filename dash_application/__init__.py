
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from dash_application.dash_template import create_dash_app_datatable, create_dash_app_ddl, create_dash_app,create_dash_app_report

from Halanweb import app
from dash_application.input_data import input_data

sme_main = input_data()





dash_app1 = create_dash_app(app,'/dashboard/')
dash_app2 = create_dash_app_report(app,'/report/')
dash_app3 = create_dash_app_datatable(app, '/datatable/')




app1 = DispatcherMiddleware(app, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server,
    '/dash3': dash_app3.server,
})

import dash_application.callbacks 