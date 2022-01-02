import pandas as pd
import plotly.graph_objs as go
from dash_application.static_dicts import css_styles, font1, features_order_period,features_stakeholder,features_order_status,features_graph_type    





class report_plots:
    def plots_percentage(sme_graph,order_period):
        return {'data':[
                
                go.Scatter( 
                    x=sme_graph[features_order_period[order_period]],
                    y=sme_graph['status_percentage'],
                    
                     text=sme_graph['status_percentage'],
                     textfont_size=14,
                textposition='top right',
                     mode='lines+markers+text',
                     texttemplate='%{text:.2%}',
                marker = {'size':15, 'opacity':0.5,
                                'line':{'width':0.5,'color':'white'} },
             
                     
                  )],

            'layout':go.Layout(
                title =  '{} orders percentage'.format(order_period),
                xaxis = dict(title = order_period),
                yaxis = dict(title = 'Status Percentage',tickformat= ',.2%',
                                range= [0,1]),
                autosize = True,
                showlegend=True,
                
                margin=dict(l=40, r=0, t=40, b=30),
                 hovermode= 'closest',
               plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                
                font= font1,
           ) }
       
        
    def plots_gmv(sme_graph,order_period):

      
        traces = []

        for features in sme_graph.columns:
        

            traces.append(
                go.Bar(
                y=sme_graph[features].values.tolist(), 
                x=sme_graph.index,
                  
                textfont_size=14,
                    textposition='auto',
                  texttemplate='%{text:.3s}',
                text = sme_graph[features],     
                opacity =  0.7,
               
                
          
                name = features,
            ))

        return {'data':
                        traces,
                        

                    'layout':go.Layout(
                        title =  'GMV',
                        barmode='group',
                        xaxis = dict(title = order_period),
                        yaxis = dict(title = 'Order Count'),
                  plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                        autosize = True,
                     font= font1,
                    
                     #margin=dict(l=40, r=0, t=40, b=30),
                ) }



    def plots_percentage_traces(sme_graph,stakeholder,order_period):
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
                
                #hovertext = '{} {}'.format(names),
                
                name = names,
                
                marker = {'size':15, 'opacity':0.5,
                                'line':{'width':0.5,    'color':'white'} },
             
            ))

        return {'data': traces,
                'layout':go.Layout(
                    title =  '{} order status percentage {} Plot:  '.format(stakeholder,order_period),
                    yaxis = dict(title = 'Order Status Percentage',tickformat= ',.2%',
                                range= [0,1]),
                    xaxis= dict(title = '{}'.format(order_period)),
                    hovermode= 'closest',
                    
                plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    font= font1,
                    autosize = True,
                    showlegend=True,
                     margin=dict(l=100, r=0, t=40, b=50),
            )}
        
        

    def plots_traces(sme_graph,stakeholder,choice):
        traces = []
        if stakeholder=='Halan':
            stakeholder = 'order_reason_of_failure'
            for names in sme_graph[stakeholder].unique():
                graph_df = sme_graph[sme_graph[stakeholder]==names]
                traces.append(go.Scatter(
                y=graph_df['order_count'], 
                x=graph_df[features_order_period[choice]],
                textfont_size=14,
                    textposition='bottom center',
                text = graph_df['order_count'],
                #texttemplate='%{text:.2%}',
                mode = 'lines+markers+text',
                opacity =  0.5,
                #hovertext = '{} {}'.format(names),
                marker = {'size':15},
                name = names,
            ))

        else:
            for names in sme_graph[features_stakeholder[stakeholder]].unique():
                graph_df = sme_graph[sme_graph[features_stakeholder[stakeholder]]==names]
                traces.append(go.Scatter(
                y=graph_df['order_count'], 
                x=graph_df[features_order_period[choice]],
                textfont_size=14,
                    textposition='bottom center',
                text = graph_df['order_count'],
                #texttemplate='%{text:.2%}',
                mode = 'lines+markers+text',
                opacity =  0.5,
                #hovertext = '{} {}'.format(names),
                marker = {'size':15},
                name = names,
            ))
        
            

        return {'data': traces,
                'layout':go.Layout(
                    title =  '{} Plot:  '.format(stakeholder),
                   # yaxis = dict(tickformat= ',.2%',
                    #            range= [0,1]),
                    yaxis = dict(title = 'Order Count'),
                    xaxis= dict(title = '{}'.format(choice)),
                    hovermode= 'closest',
                    
                plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    font= font1,
                    autosize = True,
            )}





    def plots(sme_graph,choice):
        return {'data':[
                
                go.Scatter( x=sme_graph[features_order_period[choice]],
                    y=sme_graph['order_count'],
                    
                     text=sme_graph['order_count'],
                     textfont_size=14,
                textposition='top right',
                     mode='lines+markers+text',
                     marker = dict(
                         size = 12,
                        color= css_styles['cyan'],
                        symbol = 'circle',
                        
                       line = {'width': 2}
                     )
                     ,
                  )],

            'layout':go.Layout(
                title =  '{} orders received'.format(choice),
                xaxis = dict(title = choice),
                yaxis = dict(title = 'Order Count'),
                autosize = True,
                                
                margin=dict(l=40, r=0, t=40, b=30),
                 
               plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                
                font= font1,
           ) }
       
            