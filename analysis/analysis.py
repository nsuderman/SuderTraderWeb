import pandas as pd
import numpy as np
from scipy.stats import linregress
from ta.volatility import AverageTrueRange as ATR


def momentum(array):
    if isinstance(array, np.ndarray):
        returns = np.log(array)
        x = np.arange(len(returns))
        slope, _, rvalue, _, _ = linregress(x, returns)
        slope1 = slope * 100
        metric = round((slope * 100) * (rvalue ** 2),4)
        return metric
    else:
        return array

def add_momentum(t_df,mom_back=30):
    if t_df is not None:
        t_df['atr'] = ATR(t_df['high'],t_df['low'],t_df['close']).average_true_range()

        #Add Momentum Column
        t_df['momentum']=''

        #Add array
        list_of_values = []
        t_df['close'].rolling(mom_back).apply(lambda x: list_of_values.append(x.values) or 0, raw=False)
        t_df.loc[mom_back-1:,'mom_back'] = pd.Series(list_of_values).values

        if t_df is not None:
            for i, row in t_df.iterrows():
                t_df.at[i,'momentum'] = momentum(t_df.loc[i, 'mom_back'])

        t_df['momentum_change'] = t_df['momentum'].diff().astype(float)
        t_df['momentum_change'].round(decimals=4)

        t_df.drop(columns=['mom_back'],inplace=True)
        return t_df
    else:
        return None