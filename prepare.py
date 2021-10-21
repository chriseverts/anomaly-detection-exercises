import numpy as np
import pandas as pd
from acquire import get_curriculum_logs_data
import warnings
warnings.filterwarnings('ignore')
import scipy.stats as stats


def prepare_codeup(df):
    
    df = get_curriculum_logs_data()

# combine date and time to one column then dropping those seperate columns
    df['timestamp'] = pd.to_datetime(df['date'].apply(str)+' '+df['time'])
    df.drop(['date', 'time'], axis=1, inplace=True)
    df.drop(df.loc[df['path']=='/'].index, inplace=True)# drop backslash which was ds.codeup
# set the timestamp column as my index
    df.timestamp = pd.to_datetime(df.timestamp)
    df = df.set_index('timestamp')
# dropping nulls and nans
    df=df.dropna(axis=1,how='all')
    df['cohort_id']= df['cohort_id'].astype(int)# convert to integer

    return df

def prep(df, user):
    df = df[df.user_id == user]
    pages = df['path'].resample('d').count()
    return pages

def compute_pct_b(pages, span, weight, user):
    midband = pages.ewm(span=span).mean()
    stdev = pages.ewm(span=span).std()
    ub = midband + stdev*weight
    lb = midband - stdev*weight
    bb = pd.concat([ub, lb], axis=1)
    my_df = pd.concat([pages, midband, bb], axis=1)
    my_df.columns = ['pages', 'midband', 'ub', 'lb']
    my_df['pct_b'] = (my_df['pages'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def find_anomalies(df, user, span, weight):
    pages = prep(df, user)
    my_df = compute_pct_b(pages, span, weight, user)
    # plt_bands(my_df, user)
    return my_df[my_df.pct_b>1]


def plt_bands(my_df, user):
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(my_df.index, my_df.pages, label='Number of Pages, User: '+str(user))
    ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
    ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
    ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
    ax.legend(loc='best')
    ax.set_ylabel('Number of Pages')
    plt.show()
