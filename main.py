import pandas as pd
from stock_fetch import fin_viz_fetch as Tickers
from stock_fetch import yahoo_query_fetch as Data
from analysis import analysis as Analysis
from datetime import datetime
from datetime import timedelta
import streamlit as st

import warnings
warnings.filterwarnings("ignore")

start = datetime.now() + timedelta(-365)
end = datetime.now()


def get_data(price='sh_price_1to20',volume='sh_curvol_o5000',ticker=None):
    if ticker is None:
        tickers = Tickers.stock_screener(price=price,volume_over=volume)
        return_df = pd.DataFrame()
        my_bar = st.progress(0)
        i=0
        for index, row in tickers.iterrows():
            t_df = Data.get_ticker_data(row['Ticker'],start_dt=start,end_dt=end,interval='1d',min_lag_period=25)
            if t_df is not None:
                i += 1
                my_bar.progress(i/len(tickers))
                t_df = Analysis.add_momentum(t_df,mom_back=25)
                return_df = return_df.append(t_df.iloc[-1])
                #print(row['c1'], row['c2'])

        return_df = return_df.set_index('ticker')
        return_df.drop(columns=['splits','dividends'],inplace=True)
        my_bar.empty()
        return return_df
    else:
        t_df = Data.get_ticker_data(ticker=ticker,start_dt=start,end_dt=end,interval='1d',min_lag_period=25)
        if t_df is not None:
            t_df = Analysis.add_momentum(t_df,mom_back=25)
            try:
                t_df.drop(columns=['splits','dividends'],inplace=True)
            except:
                a=1
        return t_df


if __name__ == '__main__':

    st.set_page_config(page_title="SuderTrader")

    # Title the app
    st.title('Stock Finder')

    st.sidebar.markdown("## Ticker List")
    #-- Set time by GPS or event
    price = st.sidebar.selectbox('Select Price',
                                        ['sh_price_u5', 'sh_price_u10','sh_price_u15',
                                        'sh_price_u20','sh_price_u50','sh_price_1to5',
                                        'sh_price_1to20','sh_price_5to10','sh_price_5to20'],
                                        index=6)
    volume = st.sidebar.selectbox('Select Volume - 1000K interval',
                                  ['sh_curvol_o500','sh_curvol_o1000','sh_curvol_o2000',
                                   'sh_curvol_o5000'],index=3)

    if st.sidebar.button("Fetch Tickers"):
        data = get_data(price,volume)
        st.write(data)

    st.sidebar.markdown("## Ticker Data")
    ticker = st.sidebar.text_input("Ticker Symbol")

    if st.sidebar.button("Fetch Ticker Data"):
        data = get_data(ticker=ticker)
        st.write(data)





