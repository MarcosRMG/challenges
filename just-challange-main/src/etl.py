import pandas as pd
import re


    
def data_types(data):
    # Removing "W" from week number
    data['week'] = data['week'].apply(lambda x: re.search('\d+', x).group(0))
    # Year and Week to Datetime
    data.loc[:, 'date'] = data['year'].astype('str') + '-' + data['week']
    data.loc[:, 'date'] = pd.to_datetime(data['date'] + '-1', format='%Y-%W-%w')
    # Order by date
    data.sort_values('date', inplace=True)
    # Week to number
    data['week'] = data['week'].astype('int64')
    # Selecte columns 
    data = data.drop(columns='week')
    return data
    

def time_series(data):
    '''
    --> Data in Time series format
    '''
    data = data[['date', 'net_revenue']] 
    data.loc[:, 'date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data = data.groupby(pd.Grouper(freq="M")).sum()
    data = data[data.index >= '2014-01-01']
    data = data[['net_revenue']]
    return data