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




features_graph_type = {
    'Order Status Count':'order_status_count',
    "Order Status Percentage":"order_status_percentage",
    'Order Reason of Failure':'order_reason_of_failure', #pie
     'GMV':'GMV',
}

graph_description= {
        "GMV":"Gross Market Value",
        "Order Status Count":'Number of Orders',
    'Order Reason of Failure':'Reasons Orders Fail',
    'Order Status Percentage':'Order Delivery Percentage',
        



}

features_order_status = {'Received':'Received',
                         "Delivered":"Delivered",
                         'Cancelled': 'Cancelled',
                         'Hold':'Hold',
                        }
features_order_period = {'Daily':'order_date', #ts
                         'Weekly': 'week',      #bar
                         'Monthly':'month_name',  #bar
                        }
features_stakeholder = {'Halan':'Halan',
                        'SME':'sme_name',
                        "Driver":"driver_name",
                       }

sme_columns = {
    "client_contact_no":"Client Contact Number",
     "order_id":"Order ID",
      "client_city":"Client City",
       "client_address":"Client Address",
        "sme_name":"Store Name",
         "order_status":"Order Status",
          "order_reason_of_failure":"Order Reason of Failure",
           "driver_name":"Driver Name",
            "order_delivery_fees":"Order Delivery Fee",
             "order_value":"Order Value",
              "order_date":"Order Date",
               "day":"Day",
               "year":"Year",
                "month":"Month",
                "week":"Week",
                 "month_name":"Month Name",
                 "driver_fee":"Driver Fee",
                 "halan_return":"Halan Return",
                 "sme_return":"Store Return",
                 "order_count":"Number of Orders",
                  'status_percentage': "Percentage of Orders"


}
dates_list_of_dict = []

for month in sme_main['month_name'].unique():
    dates_list_of_dict.append({'label':str(month),'value': month})


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



card_style_1 = { 
 'background' : '#ffd73e33' , 
 'color':css_styles['dark'],
 ' box-shadow': '0px 1px 15px 1px rgba(69, 65, 78, 0.08)',
 'border': '2px solid',
  'text-align': 'center',
  
  'position': 'relative',
  'border-radius': '5px',
  'background-color': '#212529',
  
  'resize': 'block',
  'display': 'flex',
 'border-top':'1px dotted #ebecec',
  'padding': '15px 25px !important',
  
}

font1 ={'color': css_styles['text'],                
                'family' : css_styles['font-family-monospace'],
                
                }


tab_style = {
   
    
    'fontWeight': 'bold',
    'border-radius': '5px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',
       
  
    
    'background-repeat':'repeat',
    
}
 



CONTENT_STYLE = {
    
   
    "padding": "20px",
    
    "position": "relative",
   
 
}
graph_style = {

    "margin":'4px',
    
  
}


h1_style ={'textAlign':'center',
        'color':css_styles['darker'] ,
        "background-color":'#3cc3ec',
          'fontWeight': 'bold',
             'border-radius': '20px',
        
        }





user_type = {
    'super':['driver','account','logout'],
    'gm':['dash','account','logout'],
    'de':['de page','account','logout'],
}

page_dict = {
    'driver':['ico_loc','link'],
    'de page':['ico_loc','link'],
    'dash':['ico_loc','link'],
    'account':['ico_loc','link'],
}

[['ico_loc','link'],['ico_loc','link'],['ico_loc','link']]