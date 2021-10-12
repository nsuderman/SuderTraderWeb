from yahooquery import Ticker
import pandas as pd


def get_ticker_data(ticker,start_dt,end_dt,interval,min_lag_period):
    t_df = Ticker(ticker).history(start=start_dt, end=end_dt, interval=interval, adj_ohlc=True)
    if isinstance(t_df, pd.DataFrame) and len(t_df.index) > min_lag_period * 2:
        zero_rows = len(t_df.loc[t_df['volume'] == 0].index)
        if zero_rows == 0:
            t_df['ticker'] = t_df._get_label_or_level_values('symbol')
            t_df.index = pd.to_datetime(t_df._get_label_or_level_values('date'))
        else:
            #Comment out for BackTrader
            t_df.loc[t_df['volume'] == 0,'volume'] = 7
            t_df['ticker'] = t_df._get_label_or_level_values('symbol')
            t_df.index = pd.to_datetime(t_df._get_label_or_level_values('date'))
    else:
        t_df = None

    return t_df