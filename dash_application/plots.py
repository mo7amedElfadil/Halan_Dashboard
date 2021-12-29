import pandas as pd
import plotly.graph_objs as go
from dash_application.static_dicts import *


class report_plots:
    
    def plots(choice,sme_main,selected_status= 'Delivered'):
        #graph 1
        if choice == 'Daily orders recieved':
            sme_graph = pd.DataFrame(sme_main.groupby('order_date')['order_date'].value_counts()).reset_index(level=1, drop=True).rename(columns={'order_date': 'order_count'}).reset_index()
            return {'data':[
                
                go.Scatter( x=sme_graph['order_date'],
                    y=sme_graph['order_count'],
                    dx=5,
                    dy=1,
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
                title =  'Daily orders received',
                xaxis = dict(title = 'Order Date'),
                yaxis = dict(title = 'Order Count'),
                autosize = True,
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30),
                 
               plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                
                font= font1,
           ) }
        #graph 2
        elif choice == 'Weekly orders recieved':
             sme_graph = pd.DataFrame(sme_main.groupby('week')['week'].value_counts()).reset_index(level=1, drop=True).rename(columns={'week': 'order_count'}) .reset_index()
             return {'data':[
                
                go.Bar( x=sme_graph['week'],
                    y=sme_graph['order_count'],
                     text=sme_graph['order_count'],
                   
                  )],

            'layout':go.Layout(
                title =  'Weekly orders received',
                xaxis = dict(title = 'Order Week'),
                yaxis = dict(title = 'Order Count'),
                plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                autosize = True,
                font= font1,
           ) }
        #graph 3       
        elif choice == 'Daily orders delivered':
            sme_graph = pd.DataFrame(sme_main.groupby('order_date')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
            
            sme_graph = sme_graph[ (sme_graph['order_status']=='Delivered')].drop('order_status', axis=1)

            
            return {'data':[
                        
                        go.Scatter( x=sme_graph['order_date'],
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
                        title =  'Daily orders delivered',
                    autosize = True,
                        xaxis = dict(title = 'Order Date'),
                        yaxis = dict(title = 'Order Count'),
                    plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        
                    font= font1,
                ) }

    #graph 4       
        elif choice ==  'Weekly orders delivered':
            sme_graph = pd.DataFrame(sme_main.groupby(['day','month_name'])['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
            option = 'Delivered'
            sme_graph  = sme_graph[(sme_graph['order_status']==option)].drop('order_status', axis=1)
            sme_graph['halan_week'] = sme_graph['day']
            sme_graph['halan_week'] =sme_graph['halan_week'].replace(range(1,9),'week 1')
            sme_graph['halan_week'] =sme_graph['halan_week'].replace(range(9,16),'week 2')
            sme_graph['halan_week'] =sme_graph['halan_week'].replace(range(16,23),'week 3')
            sme_graph['halan_week'] =sme_graph['halan_week'].replace(range(23,32),'week 4')
            sme_graph = sme_graph.drop('day', axis=1)
            sme_graph = pd.DataFrame(sme_graph.groupby(['month_name','halan_week'])['order_count'].sum()).reset_index()

            return {'data':[
                        
                        go.Bar( x=sme_graph['halan_week'],
                            y=sme_graph['order_count'],
                            #color=orders_delivered_weekly["month_name"],
                            # barmode="group",
                            text=sme_graph['order_count'],
                        
                        )],

                    'layout':go.Layout(
                        title =  'Weekly orders delivered',
                        xaxis = dict(title = 'Halan Week'),
                        yaxis = dict(title = 'Order Count'),
                    plot_bgcolor = css_styles['gray1'],
                        paper_bgcolor =css_styles['gray2'],
                        font= font1,
                        autosize = True,
                ) }
        #graph 5
        elif choice ==  'Monthly status comparison':
            sme_graph =pd.DataFrame(sme_main.groupby('month_name')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
            return {'data':[
                
                go.Bar( x=sme_graph['order_status'],
                    y=sme_graph['order_count'],
                    #color=orders_delivered_weekly["month_name"],
                    #barmode="group",
                     text=sme_graph['order_count'],
                   
                  )],

            'layout':go.Layout(
                title =  'Monthly status comparison',
                xaxis = dict(title = 'Order Status'),
                yaxis = dict(title = 'Order Count'),
             plot_bgcolor = css_styles['gray1']  ,
                paper_bgcolor =css_styles['gray2'],
                font= font1,
                autosize = True,
           ) }
        #graph 6
        elif choice ==   'SME status comparison':
            sme_graph = sme_main[['sme_name','order_status','order_value','order_date']]
            filtered_sme_status = sme_graph[sme_graph['order_status']==selected_status]
            
            
            return {'data':[
                        
                        go.Bar( x=sme_graph['week'],
                            y=sme_graph['order_count'],
                            text=sme_graph['order_count'],
                        
                        )],

                    'layout':go.Layout(
                        title =  'Weekly orders received',
                        xaxis = dict(title = 'Order Week'),
                        yaxis = dict(title = 'Order Count'),
                        plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        autosize = True,
                        font= font1,
                ) }
        #graph 7
        elif choice ==  'SME status percentage comparison':
            sme_bus_grp = sme_main.groupby(["sme_name"])
            stores_dict = {}

            for x in sme_bus_grp:
                stores_dict[x[0]] = sme_bus_grp.get_group(x[0])['order_id'].count()

            stores_df = pd.DataFrame.from_dict(stores_dict, orient='index',columns=[ 'order_count'])


            sme_asc = sme_main.groupby("sme_name")['order_status'].value_counts()
            sme_asc = sme_asc.to_frame(name='status_breakdown')


            sme_orders = pd.concat([sme_asc, stores_df], axis=0,sort=True)
            stores_series = sme_asc.index.get_level_values('sme_name')
            sme_asc['order_count'] = stores_df.loc[stores_series].values
            sme_asc = sme_asc.reset_index()

            sme_asc['status_percentage'] = sme_asc['status_breakdown']/sme_asc['order_count']
            #sme_asc = sme_asc.style.format({'daily_delivered_percentage': "{:.2%}"})
            
            
            sme_graph = sme_asc
            return {'data':[
                        
                        go.Bar( x=sme_graph['week'],
                            y=sme_graph['order_count'],
                            text=sme_graph['order_count'],
                        
                        )],

                    'layout':go.Layout(
                        title =  'Weekly orders received',
                        xaxis = dict(title = 'Order Week'),
                        yaxis = dict(title = 'Order Count'),
                        plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        autosize = True,
                        font= font1,
                ) }



        #graph 8      
        elif choice ==   'Daily status percentage comparison':
            sme_graph = pd.DataFrame(sme_main.groupby('order_date')['order_status'].value_counts()).rename(columns={'order_status': 'order_count'}).reset_index()
            dfx = pd.DataFrame(sme_graph.groupby(['order_date'])['order_count'].agg('sum')).rename(columns={'order_count': 'order_sum'}).reset_index()
            sme_graph = pd.merge(sme_graph, dfx, on="order_date")
            sme_graph['status_percentage'] = sme_graph['order_count']/sme_graph['order_sum']

            
            sme_graph = pd.DataFrame(sme_main.groupby('week')['week'].value_counts()).reset_index(level=1, drop=True).rename(columns={'week': 'order_count'}) .reset_index()
            return {'data':[
                        
                        go.Bar( x=sme_graph['week'],
                            y=sme_graph['order_count'],
                            text=sme_graph['order_count'],
                        
                        )],

                    'layout':go.Layout(
                        title =  'Weekly orders received',
                        xaxis = dict(title = 'Order Week'),
                        yaxis = dict(title = 'Order Count'),
                        plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        autosize = True,
                        font= font1,
                ) }
        elif choice ==   'Daily status comparison':
            sme_graph = pd.DataFrame(sme_main.groupby('week')['week'].value_counts()).reset_index(level=1, drop=True).rename(columns={'week': 'order_count'}) .reset_index()
            return {'data':[
                        
                        go.Bar( x=sme_graph['week'],
                            y=sme_graph['order_count'],
                            text=sme_graph['order_count'],
                        
                        )],

                    'layout':go.Layout(
                        title =  'Weekly orders received',
                        xaxis = dict(title = 'Order Week'),
                        yaxis = dict(title = 'Order Count'),
                        plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        autosize = True,
                        font= font1,
                ) }
        elif choice ==   'Order reason of failure':
            sme_graph = sme_main.dropna(subset=['order_reason_of_failure'])
            
            return {'data':[
                        
                        go.Bar( x=sme_graph['week'],
                            y=sme_graph['order_count'],
                            text=sme_graph['order_count'],
                        
                        )],

                    'layout':go.Layout(
                        title =  'Weekly orders received',
                        xaxis = dict(title = 'Order Week'),
                        yaxis = dict(title = 'Order Count'),
                        plot_bgcolor = css_styles['gray1']  ,
                        paper_bgcolor =css_styles['gray2'],
                        autosize = True,
                        font= font1,
                ) }
                        
        else:
            sme_graph = pd.DataFrame(sme_main.groupby('week')['week'].value_counts()).reset_index(level=1, drop=True).rename(columns={'week': 'order_count'}) .reset_index()
            return {'data':[
                    
                    go.Bar( x=sme_graph['week'],
                        y=sme_graph['order_count'],
                        text=sme_graph['order_count'],
                    
                    )],

                'layout':go.Layout(
                    title =  'Weekly orders received',
                    xaxis = dict(title = 'Order Week'),
                    yaxis = dict(title = 'Order Count'),
                    plot_bgcolor = css_styles['gray1']  ,
                    paper_bgcolor =css_styles['gray2'],
                    autosize = True,
                    font= font1,
            ) }
            