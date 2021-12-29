from dash_application import dash_app, Output, Input, sme_main, report_plots


@dash_app.callback(
    Output('feature_graphic', 'figure'),
    [Input('selected_graph', 'value')],

)

def update_state(choice):
    
    my_plot =report_plots.plots(choice,sme_main)
    return my_plot



@dash_app.callback(
    Output('feature_graphic', 'figure'),
    [Input('selected_graph', 'value')],

)

def update_graph(choice):
    
    my_plot =report_plots.plots(choice,sme_main)
    return my_plot
