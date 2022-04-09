import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold




def plot_prediction(bias,lag):
    
    halan_regression3 = pd.read_csv('dash_application/csv/weekly_data2.csv')
    halan_regression3['average']=halan_regression3.iloc[:,1:5].mean(axis=1)
    df = halan_regression3.copy()
    df['w1']=df['w1']/df['average']
    df['w2']=df['w2']/df['average']
    df['w3']=df['w3']/df['average']
    df['w4']=df['w4']/df['average']

    columns = ['w1','w2','w3','w4']
    deseasonalized = pd.DataFrame()

    deseasonalized['Month']=[halan_regression3['Month'][j] for j in range(len(df)) for i in columns]
    deseasonalized['Week']=[int(i[-1]) for j in range(len(df)) for i in columns]


    deseasonalized['Original']=[halan_regression3[i][j] for j in range(len(df)) for i in columns]
    deseasonalized['Delivered'] =[halan_regression3[i][j]/df[i].mean(axis=0) for j in range(len(df)) for i in columns]       
    deseasonalized['MA12'] = deseasonalized['Original'].rolling(5).mean()# plot the data and MA
    deseasonalized['Series'] = np.arange(1,len(deseasonalized)+1)



    # drop unnecessary columns and re-arrange
    data = deseasonalized[['Series', 'Month', 'Week', 'Original']]


    x = np.array(data.drop(["Series","Original"], 1))
    y = np.array(data["Original"])
    #xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.1, random_state=42)
    model = Lasso(alpha=1.0, copy_X=True,
                    fit_intercept=True,
                max_iter=1000, normalize=False,
                positive=False,
                precompute=False,
                random_state=123,
                selection='cyclic', tol=0.0001,
                warm_start=False)
    model.fit(x, y)



    
    future_df = pd.DataFrame()
    future_df['Month'] =  [i for i in  np.arange(1,13) for j in  np.arange(1,5)]   
    future_df['Week'] = [j for i in  np.arange(1,13) for j in  np.arange(1,5)]  
    future_df['Series'] = np.arange(0,(48))

    predictions_future = model.predict( future_df.drop(['Series'],axis=1,))
    predictions = pd.DataFrame(predictions_future, columns=['Label'])
    future_df['Label']=predictions['Label']

    concat_df = pd.concat([data,future_df], axis=0)
    df2 = df.rename({'w1': 1, 'w2': 2,'w3':3,'w4':4}, axis=1) 
    avgs=[]
    for i in range(4):
        avgs.append(df2[i+1].mean())
    res = concat_df.dropna(subset=['Label'], axis=0)
    res.drop(['Original'], axis=1, inplace=True)
    res['reseason']= res['Label']   
    
    if not bias:
        bias = 1
    if not lag:
        lag= 0
    for i in range(len(res['reseason'])):
        res['reseason'][i]=res['reseason'][i]*(avgs[res['Week'][i]-1])*(1-lag)+bias*i
    concat_res = pd.concat([res,deseasonalized], axis=0)

    fig = px.line(concat_res, x="Series", y=["reseason",'Label',"Original"], template = 'plotly_white',
      hover_data=["Week", "Month",'Series'],
    title='Lasso Regression Reseasonalized Target Prediction',
    )
  
    fig.update_traces(textposition='top center')
    newnames = {'reseason':'Reseasonalized Predicted', 'Label': 'Predicted Weekly Average','Original': "Actual Weekly Average"}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                    legendgroup = newnames[t.name],
                                    hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])))
    fig.update_layout(showlegend=True,   margin=dict(t=60,l=10,b=20,r=10),height=300,
   
     xaxis_title="Week Number Time Series",
        yaxis_title="Number of Delivered Orders",
            font = dict(family="Arial",),)
    return fig    