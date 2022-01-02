
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import dash_daq as daq
from dash_application.input_data import input_data
from dash_application.static_dicts import theme, NAVBAR_STYLE, CONTENT_STYLE, art_style
sme_main = input_data()


confirm = dcc.ConfirmDialog(
id='confirm',
message='Danger danger! Are you sure you want to continue?'
)

confirbutton = dcc.ConfirmDialogProvider(
children=html.Button(
'Click Me',
),
id='danger-danger',
message='Danger danger! Are you sure you want to continue?'
),

store = dcc.Store(id='my-store', data={'my-data': 'data'}),



graduatedbar = daq.GraduatedBar(
id='my-daq-graduatedbar',
value=4
)


switch = daq.BooleanSwitch(
id='my-daq-booleanswitch',
on=True
)

colorpicker =daq.ColorPicker(
id='my-daq-colorpicker',
label="colorPicker"
)

indicator =daq.Indicator(
id='my-daq-indicator',
value=True,
color="#00cc96"
)

knob =daq.Knob(
    id='my-daq-knob',
min=0,
max=10,
value=8
)

leddisplay = daq.LEDDisplay(
id='my-daq-leddisplay',
value="3.14159"
)

numericinput = daq.NumericInput(
id='my-daq-numericinput',
min=0,
max=10,
value=5
)

slider =daq.Slider(
id='my-daq-slider',
value=17,
min=0,
max=100,
targets={"25": {"label": "TARGET"}}
)

tank = daq.Tank(
id='my-daq-tank',
min=0,
max=10,
value=5
)

toggle_switch = daq.ToggleSwitch(
id='daq-light-dark-theme',
label=['Light', 'Dark'],
style={'postition':'relative'},
value=False,
)

dark_theme_provider = daq.DarkThemeProvider(theme=theme)



#####################################
# Create Auxiliary Components Here
#####################################

def nav_bar():
    
    navbar = html.Div(
    [
        html.H4("SME Performance Dashboard",style={'textAlign':'center'}),
        html.Hr(), 
        dbc.Nav(
            [
                #dbc.NavItem([toggle_switch,dcc.Location(id='url', refresh=False,)]),
                 
                dbc.NavItem(dbc.NavLink("DashBoard", href="/dashboard",active="exact", external_link=True,style=art_style)),
               
                dbc.NavItem(dbc.NavLink("DataTable", href="/datatable", active="exact", external_link=True,style=art_style)),
                
                dbc.NavItem(dbc.NavLink("Report", href="/report", active="exact", external_link=True,style=art_style)),
            ],
            pills=True,
            horizontal=True,
            fill= True,
            style={'postition':'relative','margin-right': '2rem', },
            
        ),
       
    ],
    style=NAVBAR_STYLE,
    )  
    return navbar
