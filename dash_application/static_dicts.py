from dash_application.input_data import input_data
sme_main = input_data()




sme_name_list = []

for sme_name in sme_main['sme_name'].unique():
    if sme_name_list == []:
        sme_name_list.append("")
    sme_name_list.append(sme_name)

sme_name_list.sort()
sme_name_list


Drivers_names_list = []

for driver_name in sme_main['driver_name'].unique():
    if Drivers_names_list == []:
        Drivers_names_list.append("")
    Drivers_names_list.append(driver_name)

Drivers_names_list.sort()
Drivers_names_list



order_reason_of_failure_list = []

for order_reason_of_failure in sme_main['order_reason_of_failure'].unique():
    if Drivers_names_list == []:
        order_reason_of_failure_list.append("")
    order_reason_of_failure_list.append(order_reason_of_failure)

#order_reason_of_failure_list.sort()




features = {
     'Daily orders received': 'Daily orders received',
      'Weekly orders received' : 'Weekly orders received',
      'Monthly orders received' :'Monthly orders received',
      'Daily orders delivered':'Daily orders delivered',
      'Weekly orders delivered':'Weekly orders delivered',
       'Monthly orders delivered':'Monthly orders delivered',
      'Daily status comparison':'Daily status comparison',
      'Weekly status comparison':'Weekly status comparison',
       'Monthly status comparison':'Monthly status comparison',
      'SME status comparison Daily' :'SME status comparison Daily',
      'SME status comparison Weekly' :'SME status comparison Weekly',
      'SME status comparison Monthly' :'SME status comparison Monthly',
     'SME status percentage comparison Daily'    :'SME status percentage comparison Daily',
     'SME status percentage comparison Weekly'    :'SME status percentage comparison Weekly',
     'SME status percentage comparison Monthly'    :'SME status percentage comparison Monthly',
     'Daily status percentage comparison':'Daily status percentage comparison',
      'Daily status comparison':'Daily status comparison',
      'Order reason of failure':'Order reason of failure',
      'Halan GMV':'Halan GMV',
}

features_graph_type = {
    'order_status_count':'order_status_count',
    "order_status_percentage":"order_status_percentage",
    'order_reason_of_failure':'order_reason_of_failure', #pie
     'GMV':'GMV',
}

features_order_status = {'Received':'Received',
                         "Delivered":"Delivered",
                         'Cancelled': 'Cancelled',
                         'Hold':'Hold',
                        }
#   {'label':i, 'value': i } for i in sme_main.columns,
features_order_period = {'Daily':'order_date', #ts
                         'Weekly': 'week',      #bar
                         'Monthly':'month_name',  #bar
                        }
features_stakeholder = {'Halan':'Halan',
                        'SME':'sme_name',
                        "Driver":"driver_name",
                       }

sme_columns = ['order_id', 'client_city', 'sme_name','order_value','order_date','driver_name','order_status','order_reason_of_failure','month_name','week','driver_fee',	'halan_return', 'sme_return']

dates_list_of_dict = []

for month in sme_main['month_name'].unique():
    dates_list_of_dict.append({'label':str(month),'value': month})

sme_status_options = []

for status in sme_main['order_status'].unique():
    sme_status_options.append({'label':str(status),'value': str(status)})

css_styles =  {
    'background':'#111111',
     'text':'#7FDBFF',
  'blue':'#5e72e4',
  'indigo': '#5603ad',
  'purple': '#8965e0',
  'pink': '#f3a4b5',
  'red': '#f5365c',
  'orange': '#fb6340',
  'yellow': '#ffd600',
  'green': '#2dce89',
  'teal': '#11cdef',
  'cyan': '#2bffc6',
  'white': '#ffffff',
  'gray': '#6c757d',
  'gray1':'#202020',
  'gray2':'#323232',
  'gray-dark': '#32325d',
  'light': '#ced4da',
  'lighter': '#e9ecef',
  'primary': '#e14eca',
  'secondary': '#f4f5f7',
  'success': '#00f2c3',
  'info': '#1d8cf8',
  'warning': '#ff8d72',
  'danger': '#fd5d93',
  'light': '#adb5bd',
  'dark': '#212529',
  'default': '#344675',
  'white': '#ffffff',
  
  'darker': 'black',
  'breakpoint-xs': 0,
  'breakpoint-sm': '576px',
  'breakpoint-md': '768px',
  'breakpoint-lg': '992px',
  'breakpoint-xl': '1200px',
  'font-family-sans-serif':' -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
  'font-family-monospace':' SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace', 
  }

c0 = { 'margin': '0',
  'color': '#575962',
  'font-size':'20px',
  'font-weight':'400',
  'line-height': '1.6',}


c2 = { 
 'background' : '#ffd73e33' , 
 'color':css_styles['dark'],
 ' box-shadow': '0px 1px 15px 1px rgba(69, 65, 78, 0.08)',
 'border-bottom': '7px solid',
  'text-align': 'center',
  'overflow': 'hidden',
  'position': 'relative',
  'border-radius': '5px',
  
   'min-height': '3em',
  'resize': 'both',
  'display': 'flex',
 
}
art_style ={
     "position": "inherit",
     'margin': '1rem',
     'margin-left': '1rem',
     'margin-right': '1rem',
     'padding-top':'1rem',
     'padding-bottom':'1rem',
     'padding-right': '1rem',
     'border-radius': '60px',
    'background-color': '#e9ecef',
     'box-shadow': '2px 6px 15px 0 rgba(69,65,78,.1)',
    
     'border': '2px dotted #212529',
   
     }
card_style_1 =  {
 'border-radius': '5px',
  'background-color': '#212529',
  'color': '#7d7b7b',
  'margin-bottom': '30px',
  'box-shadow': '2px 6px 15px 0px rgba(69, 65, 78, 0.1)',
  'border': '0px', 
   'height': 'calc(100% - 30px)',
  'width':' calc(100% + 2px)',
  'align-items': 'center',
  'border-top':'1px dotted #ebecec',
  'padding': '15px 25px !important',
  }

card_style_2 = {
    'border-radius': '5px',
    'background-color': '#fff',
    'margin-bottom': '30px',
    'box-shadow': '2px 6px 15px 0 rgba(69,65,78,.1)',
    'border': '0',
    'border-top-color': 'currentcolor',
    'border-top-style': 'none',
    'border-top-width': '0px',
    'border-right-color': 'currentcolor',
    'border-right-style': 'none',
    'border-right-width': '0px',
    'border-bottom-color': 'currentcolor',
    'border-bottom-style': 'none',
    'border-bottom-width': '0px',
    'border-left-color': 'currentcolor',
    'border-left-style': 'none',
    'border-left-width': '0px',
    'border-image-outset': '0',
    'border-image-repeat': 'stretch',
    'border-image-slice': '100%',
    'border-image-source': 'none',
    'border-image-width': '1',
}

  

style_1 = {'display': 'block', 'margin-left': 'calc(50% - 110px)'}
div_style1 = {'backgroundColor':css_styles['light'], 'color':css_styles['dark'], 'border':'3px indigo solid', 'padding':10}

font1 ={'color': css_styles['text'],                
                'family' : css_styles['font-family-monospace'],
                
                'color': css_styles['white'],
                }


 
tabs_styles = {
    'height': '44px',
    'align-items': 'center'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',
 
}
 
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
}


NAVBAR_STYLE = {
    "position": "absolute",
    "top": 0,
    "left": 0,
    "right": 0,
   
    'height': '12rem',
    "padding": "2rem ",
    "background-color": "#f8f9fa",
    'box-shadow': '4px 4px 4px 4px lightgrey',
      'fontWeight': 'bold',
    'border-radius': '15px',
    'margin' : '1rem',
}

CONTENT_STYLE = {
    "top":0,
    "margin-top":'15rem',
    "margin-left": "2rem",
    "margin-right": "2rem",
    "position": "relative",
   
}


theme = {
    
'dark': False,
'detail': '#007439',
'primary': '#00EA64',
'secondary': '#6E6E6E',
 "top":0,
    "margin-top":'2rem',
    "margin-left": "2rem",
    "margin-right": "2rem",
    "background-color":'f4f5f7',
    'color': 'black',
     "position": "relative",
      'box-shadow': '4px 4px 4px 4px lightgrey',
      'border-radius': '15px',
      
}
