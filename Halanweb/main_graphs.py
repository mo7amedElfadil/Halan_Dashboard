import imp

from dash_application.data import data
from dash_application.static_dicts import sme_columns, graph_description, features_graph_type,features_order_period,features_order_status,features_stakeholder
from dash_application.input_data import input_data
import plotly.express as px
import plotly.graph_objects as go
sme_main= input_data()


def guage_plot(value,title):
    return go.Figure(go.Indicator(
    mode = "gauge+number",
    value = value,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text':title}))


def gmv_plot(sme_graph,order_period):
    sme_graph = sme_graph.reset_index()
    n = len(sme_graph[features_order_period[order_period]].unique())
    fig = px.bar(sme_graph, x=['sme_return','driver_fee','halan_return'],
     y=features_order_period[order_period], title='{} there are {} '.format(order_period,n),
    text_auto=True,
    orientation='h',template = 'plotly_white')
    fig.update_layout(showlegend=True,   margin=dict(t=80,l=50,b=40,r=50),height=100*(n)+60, 
                        title='{} Gross Merchandise Value '.format(order_period),
                        xaxis_title=sme_columns[features_order_period[order_period]],
                        yaxis_title="Stakeholder Returns",
                        autosize = True, 
                        margin_pad = 10,       
                        font = dict(family="SF Pro Display, Roboto, Droid Sans, Arial"),
                        legend=dict(
            title=None, orientation="v", yanchor="bottom",   xanchor="right")                )
    fig.update_traces(textposition='auto')
    fig.update_yaxes(automargin=True,title_font = dict(size=12), 
     tickfont = dict(size = 9),)
    fig.update_xaxes(automargin=True, zeroline = True,      
     tickfont = dict(size = 11))
    newnames = {'sme_return':'Stores Return', 'driver_fee': 'Drivers Return','halan_return': "Halan's Margin"}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                    legendgroup = newnames[t.name],
                                    hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
    return  fig


def gmv_plot_monthly(sme_main):
    #switch to last month    
    sme_main = sme_main[sme_main['month_name']=='June']
    graph = gmv_plot(data.halan_dataframes(sme_main,'GMV',"Recieved",'Monthly','Halan'),'Monthly') 
    
    return graph


def gmv_plot_weekly(sme_main):
        
    graph = gmv_plot(data.halan_dataframes(sme_main,'GMV',"Recieved",'Weekly','Halan'),'Weekly') 
    
    return graph
   
def status_bar_plot(sme_graph,stakeholder,order_period,graph_type):
    fig = px.bar(sme_graph, x='order_count', y=features_order_period[order_period],
                  title=" {} Order Status Count for {} ".format(order_period,stakeholder),
                color='order_count', color_continuous_scale = "darkmint",
                 orientation='h',text="order_count",template = 'plotly_white')
    fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=20,r=50),height=150, 
                                 font = dict(family="Arial",),
                                xaxis_title=sme_columns['order_count'],
                                yaxis_title=sme_columns[features_order_period[order_period]],
                                    legend=dict( title="Number of Orders",
                        orientation="v", y=1, yanchor="bottom", x=1, xanchor="right"
                    )
                                )
    fig.update_traces(texttemplate='%{text:.3s}', textposition='auto')
    return fig
        

def delivered_plot_monthly(sme_main):
    graph = status_bar_plot(data.halan_dataframes(sme_main,'order_status_count',"Delivered",'Monthly',"Halan"),'Halan','Monthly','order_status_count') 
    return graph


    

def delivered_plot_line(sme_graph,order_period,order_status):
    avg = sme_graph['order_count'].mean()
    fig = px.line(sme_graph, x=features_order_period[order_period], y='order_count',text = 'order_count', 
            title='{} Order {} for Halan'.format(order_period,order_status),template = 'plotly_white')
    fig.update_layout(showlegend=True,   margin=dict(t=60,l=10,b=20,r=10),height=300,
     xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title=sme_columns['order_count'],
            font = dict(family="Arial",),)
    fig.update_traces(textposition='top center')
    fig.add_hline(y=avg,line_dash="dot",
              annotation_text="Avg. baseline", )
    return fig

def delivered_plot_weekly(sme_main):
    graph = delivered_plot_line(data.halan_dataframes(sme_main,'order_status_count',"Delivered",'Weekly',"Halan"),"Weekly",'Delivered') 
    return graph

def status_bar_plot_sme(sme_graph,stakeholder,order_period,graph_type):
    
    n =  len(sme_graph[features_order_period[order_period]].unique())
    fig = px.bar(sme_graph, x='order_count', y=features_order_period[order_period], color=features_stakeholder[stakeholder],
                  title=" {} Order Status Count for the top {} ".format(order_period,stakeholder), 
                orientation='h',text="order_count",template = 'plotly_white')
    fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=20,r=50),height=100*(n)+140, 
                                 font = dict(family="Arial",),
                                 xaxis_title=sme_columns['order_count'],
                            yaxis_title=sme_columns[features_order_period[order_period]],
                                    legend=dict( title="Stores",
                      orientation="h", y=-2, yanchor="top", x=1, xanchor="right"
                    )
                                )
    fig.update_traces(texttemplate='%{text:.3s}', textposition='auto')
    return fig

def received_plot_monthly(sme_main):
        
    graph = status_bar_plot_sme(data.halan_dataframes(sme_main,'order_status_count',"Received",'Monthly',"SME"),'SME',"Monthly",'order_status_count') 
    return graph

def plots_traces(sme_graph,stakeholder,order_period):
    n = len(sme_graph[features_stakeholder[stakeholder]].unique())//5
    fig = px.line(sme_graph, x=features_order_period[order_period], y='order_count',text = 'order_count',
            color=features_stakeholder[stakeholder], 
             template = 'plotly_white')
    if stakeholder=='Driver':
        fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=80,r=0),height=500+180,
                            font = dict(family="Arial",),
                            title='{} Order Count for {}'.format(order_period,stakeholder),
                              xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title=sme_columns['order_count'],
                            legend=dict(
                title="Drivers", orientation="vD", y=1, yanchor="bottom", x=1, xanchor="right"
            )
                        )
    else:
        fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=80,r=0),height=500+180,
                            font = dict(family="Arial",),
                            title='{} Order Count for {}'.format(order_period,stakeholder),
                              xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title=sme_columns['order_count'],
                            legend=dict(
                title="Stores", orientation="v", y=1, yanchor="top", x=1, xanchor="left"
            )
                        )
    
    fig.update_traces(textposition='top center')

    return fig

def received_plot_weekly(sme_main):
    graph = plots_traces(data.halan_dataframes(sme_main,'order_status_count',"Received",'Weekly',"SME"),"SME",'Weekly')   


    return graph

