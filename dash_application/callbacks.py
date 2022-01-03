import plotly.graph_objs as go
from dash.dependencies import Input, Output,State
import dash_daq as daq
from dash import html


from dash_application.data import data,report_data
from dash_application.plots import report_plots
from dash_application import dash_app1, dash_app2,dash_app3
from dash_application.layouts import layout1, layout2, dashboard_layout, report_layout,create_data_table_layout
from dash_application.static_dicts import theme, css_styles,font1
from dash_application.input_data import input_data

sme_main=input_data()

@dash_app1.callback(
        Output('feature_graphic', 'figure'),
        [Input('graph_type', 'value')],
         [Input('order_status', 'value')],
          [Input('order_period', 'value')],
           [Input('stakeholder', 'value')],
    )

def update_state(graph_type,order_status,order_period,stakeholder):
    if graph_type == "GMV":
       my_plot = report_plots.plots_gmv(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),order_period) 
    elif stakeholder =='Halan' and graph_type=="order_reason_of_failure":
        my_plot =report_plots.plots_traces(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)   
    elif stakeholder =='Halan' and graph_type!="order_status_percentage":
       my_plot =report_plots.plots(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),order_period)  
    elif stakeholder == 'Halan' and graph_type == 'order_status_percentage':
        my_plot =  report_plots.plots_percentage(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),order_period)  
    elif stakeholder != 'halan' and graph_type == 'order_status_percentage':
        my_plot = report_plots.plots_percentage_traces(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)  
    else:
       my_plot =report_plots.plots_traces(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)   
    return my_plot



@dash_app1.callback(
Output('dark-theme-component-demo', 'style'),
[Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        return {'background-color': '#303030', 'color': 'white'}
    else:
        return {'background-color': '#f4f5f7', 'color': 'black'}




@dash_app2.callback(
    Output('sme_status_comparison', 'figure'),
    [Input('sme_status_picker', 'value')]
)
def update_figure_6(selected_status):
    filtered_sme_status = report_data.sme_status[report_data.sme_status['order_status']==selected_status]

    traces = []

    for sme_name in report_data.sme_status['sme_name'].unique():
        sme_graph_df = filtered_sme_status[filtered_sme_status['sme_name']==sme_name]
       
       
        traces.append(go.Scatter(
            x=sme_graph_df['order_date'],
            y=sme_graph_df['order_count'],
            mode = 'markers',
            opacity =  0.7,
            marker = {'size':15},
            name = sme_name
        ))

    return {'data': traces,
            'layout':go.Layout(
                title =  'SME status comparison',
                xaxis = dict(title = 'Order Dates'),
               hovermode= 'closest',
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           )}


@dash_app2.callback(
    Output('sme_status_percentage_comparison', 'figure'),
    [Input('sme_status_percentage_picker', 'value')]
)

def update_figure_7(selected_status):
    filtered_sme_status_percentage = report_data.sme_asc[report_data.sme_asc['order_status']==selected_status]

    traces = []

    for sme_name in report_data.sme_asc['sme_name'].unique():
        sme_percentage_graph_df = filtered_sme_status_percentage[filtered_sme_status_percentage['sme_name']==sme_name]
       
       
        traces.append(go.Scatter(
            y=sme_percentage_graph_df['status_percentage'], 
            x=sme_percentage_graph_df['sme_name'],
             textfont_size=14,
                textposition='bottom center',
            text = sme_percentage_graph_df['status_percentage'],
            texttemplate='%{text:.2%}',
            mode = 'markers+text',
            opacity =  0.7,
           
            marker = {'size':15},
            name = sme_name
        ))

    return {'data': traces,
            'layout':go.Layout(
                title =  'SME status percentage comparison. Selected Status:  ' + selected_status,
                yaxis = dict(tickformat= ',.2%',
                             range= [0,1]),
                xaxis= dict(title = 'Business Name'),
                hovermode= 'closest',
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           )}


@dash_app2.callback(
    Output('daily_status_comparison', 'figure'),
    [Input('daily_status_picker', 'value')],
    [Input('daily_status_percentage_picker', 'value')]
)

def update_figure_8(selected_status,selected_data):
    filtered_daily_status_percentage = report_data.daily_count[report_data.daily_count['order_status']==selected_status]

 
 
    if selected_data == 'status_percentage':

        return {'data':[ go.Scatter(
                y=filtered_daily_status_percentage[selected_data], 
                x=filtered_daily_status_percentage['order_date'],
                text = filtered_daily_status_percentage[selected_data],
                mode = 'lines+markers+text',
                opacity =  0.7,
            texttemplate='%{text:.2%}',
                marker = {'size':15, 'opacity':0.5,
                                'line':{'width':0.5,    'color':'white'} },
             textposition="top center",
                
            )],
                'layout':go.Layout(
                    title =  'Daily status percentage comparison. Selected Status:  ' + selected_status,
                    yaxis = dict(tickformat= ',.2%',
                                range= [0,1]),
                    xaxis= dict(title = 'Order date'),
                    hovermode= 'closest',
                plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    font= font1,
                   autosize = True, 
                    
            )}
    else:
        
        return {'data':[ go.Scatter(
                y=filtered_daily_status_percentage[selected_data], 
                x=filtered_daily_status_percentage['order_date'],
                text =filtered_daily_status_percentage[selected_data],
                mode = 'lines+markers+text',
                opacity =  0.7,
            
                marker = {'size':15, 'opacity':0.5,
                                'line':{'width':0.5,    'color':'white'} },
                  textposition="top center",
            )],
                'layout':go.Layout(
                    title =  'Daily status percentage comparison. Selected Status:  ' + selected_status,
                   
                    xaxis= dict(title = 'Order date'),
                    hovermode= 'closest',
                plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    font= font1,
                    autosize = True,
            )}


@dash_app2.callback(
Output('dark-theme-component-demo', 'style'),
[Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        return {'background-color': '#303030', 'color': 'white'}
    else:
        return {'background-color': 'white', 'color': 'black'}



@dash_app3.callback(
Output('dark-theme-component-demo', 'style'),
[Input('daq-light-dark-theme', 'value')]
)
def change_bg(dark_theme):
    if(dark_theme):
        return {'background-color': '#303030', 'color': 'white'}
    else:
        return {'background-color': 'white', 'color': 'black'}





