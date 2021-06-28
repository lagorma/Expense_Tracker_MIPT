import pandas as pd 
import numpy as np

def analyse():
    (pd.DataFrame.from_dict(data=a, orient='index')
        .to_csv('expenses.csv', header=1))
    df = read_csv('expenses.csv')
    df.columns = ['Time','Expenses']
    df.to_csv('expenses.csv')
    dataset = pd.read_csv('expenses.csv', index_col=['Time'])


#Subsetting the dataset
#Index 11856 marks the end of year 2013
#df = pd.read_csv('train.csv', nrows = 11856)

#Creating train and test set
#Index 10392 marks the end of October 2013
    train=df[0:1]
    test=df[1:]

#Aggregating the dataset at daily level
    df.Timestamp = pd.to_datetime(df.Datetime,format='%m-%Y')
    df.index = df.Timestamp
    df = df.resample('D').mean()
    train.Timestamp = pd.to_datetime(train.Datetime,format='%m-%Y')
    train.index = train.Timestamp
    train = train.resample('D').mean()
    test.Timestamp = pd.to_datetime(test.Datetime,format='%m-%Y')
    test.index = test.Timestamp
    test = test.resample('D').mean()
    from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt
    y_hat_avg = test.copy()
    fit2 = SimpleExpSmoothing(np.asarray(train['Count'])).fit(smoothing_level=0.6,optimized=False)
    y_hat_avg['SES'] = fit2.forecast(len(test))
    return 
