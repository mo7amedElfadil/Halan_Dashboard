
from dash.dependencies import Input, Output,State, MATCH


from dash_application.data import data
from dash_application.plots import report_plots
from dash_application import dash_app1 ,reg_app  
from dash_application.layouts import create_data_table, container_component_layout, create_dashboard_layout_dynamic
from dash_application.regression import plot_prediction
from dash_application.input_data import input_data

sme_main=input_data()

  
@reg_app.callback(
   Output('reg_graphic', 'figure'),
    [Input("bias_slider", "value"),
    Input("lag_slider", "value"),
    ],
   
)
def regression( bias,lag):
    reg_plot = plot_prediction(bias,lag)
    
    return reg_plot


@reg_app.callback(
   Output('bias_value', 'children'),
    [Input("bias_slider", "value"),
    ],
   
)
def print_bias( bias):
    return f'Bias Value: {bias}'
    

@reg_app.callback(
   Output('lag_value', 'children'),
    [Input("lag_slider", "value"),
    ],
   
)
def print_lag( lag):
    return  f'Lag Value: {lag}'



@dash_app1.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    return container_component_layout(tab,sme_main)
    
@dash_app1.callback(Output('table_container', 'children'),
                [Input('graph_type','value'),
         Input('order_status', 'value'),
          Input('order_period','value'),
           Input('stakeholder','value')])
def update_table(graph_type,order_status,order_period,stakeholder):
    df = data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder)
    return create_data_table(df)
  
@dash_app1.callback(
    Output("container", "children"),
    [Input("add_chart", "n_clicks")],
    [State("container", "children")],
)
def display_graphs(n_clicks, div_children):
    new_child = create_dashboard_layout_dynamic(n_clicks)
    div_children.append(new_child)
    return div_children
  


@dash_app1.callback(
        Output({'type':'feature_graphic','index':MATCH}, 'figure'),
        [Input(component_id={'type':'graph_type','index':MATCH}, component_property='value'),
         Input(component_id={'type':'order_status','index':MATCH}, component_property= 'value'),
          Input(component_id={'type':'order_period','index':MATCH}, component_property= 'value'),
           Input(component_id={'type':'stakeholder','index':MATCH}, component_property= 'value'),
   
             ],
    )

def update_state(graph_type,order_status,order_period,stakeholder):
    try:
        if graph_type == "GMV":
                my_plot = report_plots.plots_gmv(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),order_period) 
           
        elif graph_type=="order_reason_of_failure":       
            if order_period=='Monthly':
                if stakeholder=="Halan":
                    my_plot =report_plots.plots_pie_traces(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)   
                else:
                    my_plot =report_plots.plots_treemap(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)   
            else:
                my_plot =report_plots.plots_sunburst(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)   
       
        elif graph_type == 'order_status_percentage':
            if order_period=='Monthly':
                my_plot =report_plots.plots_sunburst_percentage(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period,order_status)                  
            else: 
                if stakeholder == 'Halan':
                    my_plot =  report_plots.plots_percentage(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),order_period,order_status)  
                else:
                    my_plot = report_plots.plots_percentage_traces(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)  
        elif graph_type=='order_status_count':
            if stakeholder =='Halan':
                if order_period!='Monthly':
                    my_plot =report_plots.plots(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),order_period,order_status)      
                else:
                    my_plot = report_plots.plots_bar(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period,graph_type) 
            else:
                if order_period!='Monthly':
                    my_plot =report_plots.plots_traces(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period)   
                else:
                    my_plot = report_plots.plots_bar(data.halan_dataframes(sme_main,graph_type,order_status,order_period,stakeholder),stakeholder,order_period,graph_type) 
        else:
            my_plot =report_plots.plots_treemap_main(sme_main,stakeholder,order_status)
        return my_plot

    except:
       my_plot= report_plots.plots_img()
       return my_plot



@dash_app1.callback(
        Output('feature_graphic', 'figure'),
        [Input('graph_type', 'value')],
         [Input('order_status', 'value')],
          [Input('order_period', 'value')],
           [Input('stakeholder', 'value')],   )
def update_state(graph_type,order_status,order_period,stakeholder):
    if graph_type == "GMV":
       my_plot = report_plots.plots_gmv(data.halan_dataframes(sme_main,graph_type,
       order_status,order_period,stakeholder),order_period) 
    elif stakeholder =='Halan' and graph_type=="order_reason_of_failure":
        my_plot =report_plots.plots_traces(data.halan_dataframes(sme_main,graph_type,
        order_status,order_period,stakeholder),stakeholder,order_period)   
    elif stakeholder =='Halan' and graph_type!="order_status_percentage":
       my_plot =report_plots.plots(data.halan_dataframes(sme_main,graph_type,
       order_status,order_period,stakeholder),order_period)  
    elif stakeholder == 'Halan' and graph_type == 'order_status_percentage':
        my_plot =  report_plots.plots_percentage(data.halan_dataframes(sme_main,graph_type,
        order_status,order_period,stakeholder),order_period,order_status)  
    elif stakeholder != 'halan' and graph_type == 'order_status_percentage':
        my_plot = report_plots.plots_percentage_traces(data.halan_dataframes(sme_main,graph_type,
        order_status,order_period,stakeholder),stakeholder,order_period)  
    else:
       my_plot =report_plots.plots_traces(data.halan_dataframes(sme_main,graph_type,order_status,
       order_period,stakeholder),stakeholder,order_period)   
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

