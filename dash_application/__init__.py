
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from dash_application.dash_template import create_dash_app_tabbed ,create_reg_app

from Halanweb import app


dash_app1 = create_dash_app_tabbed(app,'/dashboard/')
reg_app = create_reg_app(app,'/forecast/')
#linking the dash app to the flask app's server
app1 = DispatcherMiddleware(app, {
    '/dashboard': dash_app1.server,
    '/forecast':reg_app.server,
})

import dash_application.callbacks 