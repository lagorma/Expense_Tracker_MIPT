import sys
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
from pandas import read_csv
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

from scipy.optimize import minimize
from math import sqrt



def exponential_smoothing(panda_series, alpha):
    output = sum([alpha*(1-alpha) ** i *x for i,x in enumerate(reversed(panda_series))])
    return output

def analyse(a, exponential_smoothing):
    (pd.DataFrame.from_dict(data=a, orient='index')
        .to_csv('expenses.csv', header=1))
    df = read_csv('expenses.csv')
    df.columns = ['Time','Expenses']
    df.to_csv('expenses.csv')
    dataset = pd.read_csv('expenses.csv', index_col=['Time'])
    panda_series = dataset.Expenses
    smoothing_number = exponential_smoothing(panda_series, 0.7)
    testdata=dataset[:-1]
    estimated_values=testdata.copy()
    estimated_values['SES']=smoothing_number
    error=sqrt(mean_squared_error(testdata.Expenses, estimated_values.SES))
    #print(error)
    return round(smoothing_number)

