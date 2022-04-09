import plotly.express as px
import plotly.graph_objs as go
from dash_application.static_dicts import sme_columns,css_styles, font1, features_order_period,features_stakeholder    
from plotly.subplots import make_subplots
from skimage import io 

class report_plots:
    def plots_img():
        img = io.imread('dash_application/assets/img.jpg')
        fig = px.imshow(img, height=400)
        fig.update_layout(hovermode=False, title="There is no graph representation for the selected features. \nTry changinging the order Status!",)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return fig

    def plots_pie_traces(sme_graph,stakeholder,order_period):
        plot = 'px'
        if plot =='px':
            if stakeholder!='Halan':

                r = int(len(sme_graph[features_stakeholder[stakeholder]].unique())/2) 
                n = len(sme_graph[features_stakeholder[stakeholder]].unique())           
                fig = make_subplots(rows=r, cols=2,  specs=[[{'type':'pie'}, {'type':'pie'}] for i in range(r)])
        
                stakeholder_list = sme_graph[features_stakeholder[stakeholder]].unique()
                it = 0
                for i in range(r):
                    for j in range(2):
                        if n==0:
                            break
                        else:
                            df3 = sme_graph[sme_graph[features_stakeholder[stakeholder]]==(stakeholder_list[it])]
                            fig.add_trace( go.Pie(labels=df3['order_reason_of_failure'],values=df3['order_count'], title=stakeholder_list[it]),
                                    i+1, j+1)
                            it= it+1
                fig.update_traces(textposition='inside')
                fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',height=300*r+80, margin=dict(t=60,l=20,b=20,r=20),
                font = dict(family="Arial",),
                title="{} Order Reason of failure for {}".format(order_period,stakeholder), legend=dict(
                        orientation="h", y=1, yanchor="bottom", x=1, xanchor="right"
                    ))
                return fig
            else:
                r = 1
                fig = make_subplots(rows=r, cols=r,  specs=[[{'type':'pie'}] for i in range(r)])
                df3 = sme_graph
                fig.add_trace( go.Pie(labels=df3['order_reason_of_failure'],values=df3['order_count'], title="Halan"), 
                        1, 1)
                fig.update_traces(textposition='inside',texttemplate='%{percent}')
                fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide',margin=dict(t=60,l=20,b=20,r=20),height=300*r+80,
                font = dict(family="Arial",),
                title="Order Reason of failure for {}".format(stakeholder), legend=dict(
                         orientation="v", 
                    ))
                return fig

    def plots_percentage(sme_graph,order_period,order_status):
        
        fig = px.line(sme_graph, x=features_order_period[order_period], y='status_percentage',text = 'status_percentage',
            title=f'{order_period} Orders {order_status} Percentage',template = 'plotly_white')
        fig.update_layout(showlegend=True,   margin=dict(t=60,l=10,b=10,r=10),height=200+80,
        xaxis_title=sme_columns[features_order_period[order_period]],
        yaxis_title=sme_columns['status_percentage'],
        font = dict(family="Arial",),
          )
        fig.update_traces(texttemplate='%{text:.2%}',textposition='top center')
        avg = sme_graph['status_percentage'].mean()
        fig.add_hline(y=avg,line_dash="dot",
              annotation_text="Avg. baseline", )
        return fig
        
    def plots_bar(sme_graph,stakeholder,order_period,graph_type):
        if stakeholder != 'Halan':
            n_stake = len(sme_graph[features_stakeholder[stakeholder]].unique())
        n =  len(sme_graph[features_order_period[order_period]].unique())
        if stakeholder == "Halan":
            fig = px.bar(sme_graph, x='order_count', y=features_order_period[order_period],
                title=" {} Order Status Count for {} ".format(order_period,stakeholder),
            color='order_count', color_continuous_scale = "darkmint",
                orientation='h',text="order_count",template = 'plotly_white')
            fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=20,r=50),height=180, 
                                font = dict(family="Arial",),
                                xaxis_title=sme_columns['order_count'],
                                yaxis_title=sme_columns[features_order_period[order_period]],
                                legend=dict( title=None,
                    orientation="v", y=1, yanchor="bottom", x=1, xanchor="right"
                )
                            )
            fig.update_traces(texttemplate='%{text:.3s}', textposition='auto')
            return fig
        elif n_stake>10:
            fig = px.bar(sme_graph, x='order_count', y=features_order_period[order_period], color=features_stakeholder[stakeholder],
                title=" {} Order Status Count for the top {} ".format(order_period,stakeholder), 
            orientation='h',text="order_count",template = 'plotly_white')
            fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=20,r=50),height=200*(n)+140, 
                            font = dict(family="Arial",),
                            xaxis_title=sme_columns['order_count'],
                            yaxis_title=sme_columns[features_order_period[order_period]],
                                legend=dict( title=None,
                    orientation="h", y=-2, yanchor="bottom", x=1, xanchor="right"
                ))
                
            fig.update_traces(texttemplate='%{text:.3s}', textposition='auto')
            return fig
        else:
            fig = px.bar(sme_graph, x='order_count', y=features_order_period[order_period], color=features_stakeholder[stakeholder],
            title=" {} Order Status Count for the top {} ".format(order_period,stakeholder),
            orientation='h',text="order_count",template = 'plotly_white')
            fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=20,r=50),height=200*(n)+80, 
                        font = dict(family="Arial",),
                        xaxis_title=sme_columns['order_count'],
                        yaxis_title=sme_columns[features_order_period[order_period]],
                        legend=dict( title=None,
                            orientation="h", y=-2, yanchor="bottom", x=1, xanchor="right"
                                    )
                            )
            fig.update_traces(texttemplate='%{text:.3s}', textposition='auto')
            return fig
    
    def plots_gmv(sme_graph,order_period):
        plot = 'px'
        if plot =='px':
            if features_order_period[order_period]=='order_date':
                sme_graph = sme_graph.reset_index()
                
        
                fig = px.bar(sme_graph, y=['sme_return','driver_fee','halan_return'], x=features_order_period[order_period], 
                title='{} Gross Merchandise Value '.format(order_period),
                    
                    
                    text_auto=True,
                    orientation='v',template = 'plotly_white')
                fig.update_traces(textposition='auto')
                fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=120,r=50),height=440, 
                                 xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title="Stakeholder Returns",
                                font = dict(family="Arial",),
                                    legend=dict(  title=None,
                         orientation="h", y=1, yanchor="bottom", x=1, xanchor="right"
                    )
                                )
                newnames = {'sme_return':'Stores Return', 'driver_fee': 'Drivers Return','halan_return': "Halan's Margin"}
                fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                      legendgroup = newnames[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                     )
                  )
                    
                return fig
            
            else:
                sme_graph = sme_graph.reset_index()
                n = len(sme_graph[features_order_period[order_period]].unique())
        
                fig = px.bar(sme_graph, x=['sme_return','driver_fee','halan_return'], y=features_order_period[order_period], title='{} there are {} '.format(order_period,n),#color=features_order_period[order_period],
                    
                    text_auto=True,
                    orientation='h',template = 'plotly_white')
                fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=20,r=50),height=150*(n), 
                                 title='{} Gross Merchandise Value '.format(order_period),
                                 xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title="Stakeholder Returns",
                                font = dict(family="Arial",),
                                    legend=dict(
                        title=None, orientation="h", y=1, yanchor="bottom", x=1, xanchor="right"
                    )
                                )
                    
                return fig
                
       

    def plots_treemap(sme_graph,stakeholder,order_period):
    
        stakeholder_list = (sme_graph.groupby(features_stakeholder[stakeholder])['order_count'].sum().reset_index().nlargest(5,'order_count'))[features_stakeholder[stakeholder]].unique()
        sme_graph=sme_graph[sme_graph[features_stakeholder[stakeholder]].isin(stakeholder_list)]
        fig =px.treemap(sme_graph, path=[features_order_period[order_period], features_stakeholder[stakeholder],'order_reason_of_failure'], values='order_count', maxdepth=4,
                title='{} Order Reason of Failure for {} '.format(order_period,stakeholder),
                  color='order_reason_of_failure',template='plotly_white') 
        fig.update_layout( height=800,margin=dict(t=70,l=0,b=20,r=0),
                 font = dict(family="Arial",),
            )
        return fig

    def plots_treemap_main(sme_graph,stakeholder):
        sme_graph['order_count'] = 1
        if stakeholder=='Halan':
            fig =px.treemap(sme_graph, path=['year','month_name','week','day','order_status','order_id'],
            title='{} Summary Tree Map '.format(stakeholder),
                  color='order_value',template='plotly_white', branchvalues ='total',
                  hover_data =['order_value','order_delivery_fees','halan_return','order_status','sme_name','driver_name'] ,
                  ) 
        
            fig.update_layout( height=700,margin=dict(t=70,l=0,b=20,r=0),
                    font = dict(family="Arial",),
                )
        else:
            fig =px.treemap(sme_graph, path=[ features_stakeholder[stakeholder],'year','month_name','week','day','order_status','order_id'],
            title='{} Summary Tree Map '.format(stakeholder), 
                  color= features_stakeholder[stakeholder],template='plotly_white', branchvalues ='total', maxdepth=4,
                   hover_data =['order_value','order_delivery_fees','halan_return','order_status','sme_name','driver_name'] ,
                   ) 
        
            fig.update_layout( height=700,margin=dict(t=70,l=0,b=20,r=0),
                    font = dict(family="Arial",),
                )
        return fig

    def plots_sunburst(sme_graph,stakeholder,order_period):
        if stakeholder == "Halan":
            fig = px.sunburst(sme_graph, path=[features_order_period[order_period],'order_reason_of_failure'], values='order_count', 
            title='{} Order Reason of Failure for {} '.format(order_period,stakeholder),
            color=features_order_period[order_period],template='plotly_white') 
            fig.update_layout( height=640,margin=dict(t=60,l=0,b=20,r=0),uniformtext_minsize=12, 
                 font = dict(family="Arial",),
            )
            fig.update_traces( textfont_size=14)
            return fig

        else:
            fig = px.sunburst(sme_graph, path=[features_order_period[order_period],'order_reason_of_failure', features_stakeholder[stakeholder]], values='order_count', 
            title='{} Order Reason of Failure for {} '.format(order_period,stakeholder),
            color=features_order_period[order_period],template='plotly_white')
            fig.update_layout( height=640,margin=dict(t=60,l=0,b=20,r=0),uniformtext_minsize=12,
                 font = dict(family="Arial",),
            )
            fig.update_traces( textfont_size=14)
            return fig
    def plots_sunburst_percentage(sme_graph,stakeholder,order_period,order_status):
        if stakeholder == "Halan":
            fig = px.sunburst(sme_graph, path=[features_order_period[order_period],'order_status'],
             values='status_percentage', title="{} {} Status Percentage out of {} total orders".format(order_period, order_status,stakeholder),
            color='status_percentage',template='plotly_white')
            fig.update_layout( height=740,margin=dict(t=60,l=0,b=20,r=0),uniformtext_minsize=12,
            font = dict(family="Arial",),
                 legend=dict(
                        title=None,)
            )
            fig.update_traces(textinfo="label+percent root", textfont_size=14)
            return fig
        else:
            fig = px.sunburst(sme_graph, path=[features_order_period[order_period],'order_status', features_stakeholder[stakeholder]], 
             values='status_percentage',   title="{} {} Status Percentage out of {} total orders".format(order_period, order_status,stakeholder),
            color='status_percentage',template='plotly_white') 
            fig.update_layout( height=740,margin=dict(t=60,l=0,b=20,r=0),uniformtext_minsize=12, 
            font = dict(family="Arial",),
                 legend=dict(
                        title=None,)
            )
            fig.update_traces(textinfo="label+percent root", textfont_size=14)
            return fig

    def plots_percentage_traces(sme_graph,stakeholder,order_period):
        plot = 'px'
        if stakeholder!='Halan':
            r=len(sme_graph[features_stakeholder[stakeholder]].unique())           
            fig = make_subplots(rows=r+1, cols=1, specs=[[{'type':'scatter'}] for i in range(r+1)])
    
            stakeholder_list = sme_graph[features_stakeholder[stakeholder]].unique()
            traces = []
            for names in sme_graph[features_stakeholder[stakeholder]].unique():
                graph_df = sme_graph[sme_graph[features_stakeholder[stakeholder]]==names]
                traces.append(go.Scatter(
                x=graph_df[features_order_period[order_period]],
                        y=graph_df['status_percentage'],
                    textfont_size=11,   
                        textposition='top right',
                    text = graph_df['status_percentage'],
                    texttemplate='%{text:.2%}',
                    mode = 'lines+markers+text',
                    name = names,
                    marker = {'size':15, 'opacity':0.5,
                                    'line':{'width':0.5} },
                
                ))
            fig.add_traces(traces,1,1)
            it = 0
            for i in range(r):
                for j in range(1):
                    if r==0:
                        break
                    else:
                        i=i+1
                        df3 = sme_graph[sme_graph[features_stakeholder[stakeholder]]==(stakeholder_list[it])]
                        fig.add_trace( go.Scatter( x=df3[features_order_period[order_period]], y=df3['status_percentage'],text = df3['status_percentage'],
                            name = stakeholder_list[it], showlegend=False, 
                        mode = 'lines+markers+text'),
                                i+1, j+1)
                        it= it+1
            fig.update_traces(textposition='top left',texttemplate='%{text:.2%}')
            if r>10:
                fig.update_layout( uniformtext_minsize=12, uniformtext_mode='hide',height=300*r+180,margin=dict(t=60,l=50,b=40,r=0),
                font = dict(family="Arial",),
                title='{} Order Status Percentage for {} '.format(order_period,stakeholder),
                xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title="Status Percentage",
                legend=dict(
                title=None, orientation="h", y=0.9999, yanchor="bottom", x=0.7, xanchor="right",
                    ))
            else:
                fig.update_layout( uniformtext_minsize=12, uniformtext_mode='hide',height=300*r+180,margin=dict(t=60,l=50,b=40,r=50),
                font = dict(family="Arial",),
                title='{} Order Status Percentage for {} '.format(order_period,stakeholder),
                   xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title="Status Percentage",
                legend=dict(
                title=None, orientation="h", y=1, yanchor="bottom", x=1, xanchor="right",
                    ))
            return fig
        else:
            traces = []
            for names in sme_graph[features_stakeholder[stakeholder]].unique():
                graph_df = sme_graph[sme_graph[features_stakeholder[stakeholder]]==names]
                traces.append(go.Scatter(
                x=graph_df[features_order_period[order_period]],
                    y=graph_df['status_percentage'],
                    textfont_size=14,
                    textposition='top right',
                    text = graph_df['status_percentage'],
                    texttemplate='%{text:.2%}',
                    mode = 'lines+markers+text',
                    name = names,
                    marker = {'size':15, 'opacity':0.5,
                                    'line':{'width':0.5} },
                ))
            return {'data': traces,
                    'layout':go.Layout(
                        title =  '{} order status percentage {} Plot:  '.format(stakeholder,order_period),
                        yaxis = dict(title = 'Status Percentage',tickformat= ',.2%',
                                    range= [0,1]),
                        xaxis= dict(title = '{}'.format(sme_columns[features_order_period[order_period]])),
                        hovermode= 'closest',
                    plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        font= font1,
                        autosize = True,
                        showlegend=True,
                        margin=dict(l=100, r=0, t=40, b=50),
                )}
   
    def plots_traces(sme_graph,stakeholder,order_period):
        plot = 'px'
        avg = sme_graph['order_count'].mean()
        n = len(sme_graph[features_stakeholder[stakeholder]].unique())//5
        if plot =='px':
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
                        title=None, orientation="h", y=0.99, yanchor="bottom", x=0.9, xanchor="right"
                    )
                                )
            else:
                fig.update_layout(showlegend=True,   margin=dict(t=60,l=50,b=80,r=0),height=500+180,
                                 font = dict(family="Arial",),
                                 title='{} Order Count for {}'.format(order_period,stakeholder),
                                  xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title=sme_columns['order_count'],
                                    legend=dict(
                        title=None, orientation="h", y=0.96, yanchor="bottom", x=0.9, xanchor="right"
                    )
                                )
            fig.update_traces(textposition='top center')
            fig.add_hline(y=avg,line_dash="dot",
              annotation_text="Avg. baseline", )
            return fig
        
    def plots(sme_graph,order_period,order_status):
        plot = 'px'
        avg = sme_graph['order_count'].mean()
        if plot =='px':
            fig = px.line(sme_graph, x=features_order_period[order_period], y='order_count',text = 'order_count', 
            title='{} Order {} for Halan'.format(order_period,order_status),template = 'plotly_white')
            fig.update_layout(showlegend=True,   margin=dict(t=60,l=10,b=20,r=10),height=440,
             xaxis_title=sme_columns[features_order_period[order_period]],
                                yaxis_title=sme_columns['order_count'],
            font = dict(family="Arial",),)
            fig.update_traces(textposition='top center')
            fig.add_hline(y=avg,line_dash="dot",
              annotation_text="Avg. baseline", )
            return fig
       