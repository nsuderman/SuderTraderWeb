import pandas as pd
from finviz.screener import Screener
import enum
import os
import json
import requests


GENERIC_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/json',
    'user-agent': 'Mozilla/5.0'
}

location = os.getcwd()


class Price(enum.Enum):
    any = ''
    under1 = 'sh_price_u1'
    under2 = 'sh_price_u2'
    under3 = 'sh_price_u3'
    under4 = 'sh_price_u4'
    under5 = 'sh_price_u5'
    under7 = 'sh_price_u7'
    under10 = 'sh_price_u10'
    under15 = 'sh_price_u15'
    under20 = 'sh_price_u20'
    under30 = 'sh_price_u30'
    under40 = 'sh_price_u40'
    under50 = 'sh_price_u50'
    over1 = 'sh_price_o1'
    over2 = 'sh_price_o2'
    over3 = 'sh_price_o3'
    over4 = 'sh_price_o4'
    over5 = 'sh_price_o5'
    over7 = 'sh_price_o7'
    over10 = 'sh_price_o10'
    over15 = 'sh_price_o15'
    over20 = 'sh_price_o20'
    over30 = 'sh_price_o30'
    over40 = 'sh_price_o40'
    over50 = 'sh_price_o50'
    over60 = 'sh_price_o60'
    over70 = 'sh_price_o70'
    over80 = 'sh_price_o80'
    over90 = 'sh_price_o90'
    over100 = 'sh_price_o100'
    between1_5 = 'sh_price_1to5'
    between1_20 = 'sh_price_1to20'
    between5_10 = 'sh_price_5to10'
    between5_20 = 'sh_price_5to20'
    between5_50 = 'sh_price_5to50'
    between10_20 = 'sh_price_10to20'
    between10_50 = 'sh_price_10to50'
    between20_50 = 'sh_price_20to50'
    between50_100 = 'sh_price_50to100'


class CurrentVolume(enum.Enum):
    any = ''
    under50k = 'sh_curvol_u50'
    under100k = 'sh_curvol_u100'
    under500k = 'sh_curvol_u500'
    under750k = 'sh_curvol_u750'
    under1m = 'sh_curvol_u1000'
    over50k = 'sh_curvol_o50'
    over100k = 'sh_curvol_o100'
    over500k = 'sh_curvol_o500'
    over750k = 'sh_curvol_o750'
    over1m = 'sh_curvol_o1000'
    over2m = 'sh_curvol_o2000'
    over5m = 'sh_curvol_o5000'
    over10m = 'sh_curvol_o10000'
    over20m = 'sh_curvol_o20000'


def stock_screener_finviz(price='sh_price_1to20', volume_over='sh_curvol_o5000'):
    try:
        filters = [price, volume_over]
        stock_list = Screener(filters=filters, table='Overview', order='price')
        stock_list.to_csv(location + '/stock_fetch/stocks.csv')
        print(f'FinViz Returned {len(stock_list.data)} tickers from Price Param {price} & '
                    f'Volume Param {volume_over}')

    except Exception as e:
        print(f'No Results Returned from Price Param {price} & Volume Param {volume_over}')
        print(f'Pulling Data from Last Successful Query')

    df = pd.read_csv(location + '/stock_fetch/stocks.csv')
    return df


def otc_screener(min_volume):
    OTC_TICKERS_URK = 'https://www.otcmarkets.com/research/stock-screener/api?securityType=Common%20Stock&market=20,21,22,10,6,5,2,1&sortField=symbol&pageSize=100000&'
    r = make_request(OTC_TICKERS_URK).text.strip('"').replace('\\"', '"')
    r = json.loads(r)['stocks']
    tickers = pd.DataFrame()
    for stock in r:
        symbol = stock['symbol'].strip()
        info={}
        if 'symbol' in stock:
            info['Ticker'] = [stock['symbol']]
        if 'securityName' in stock:
            info['name'] = [stock['securityName']]
        if 'market' in stock:
            info['market'] = [stock['market']]
        if 'industryId' in stock:
            info['industry_id'] = [stock['industryId']]
        if 'industry' in stock:
            info['industry'] = [stock['industry']]
        if 'volume' in stock:
            info['volume'] = [stock['volume']]
        if 'volumeChange' in stock:
            info['volume_change'] = [stock['volumeChange']]
        if 'price' in stock:
            info['price'] = [stock['price']]
        if 'shortInterest' in stock:
            info['short_interest'] = [stock['shortInterest']]
        if 'shortInterestPercent' in stock:
            info['short_percent'] = [stock['shortInterestPercent']]

        if stock['volume'] > int(min_volume):
            temp_df = pd.DataFrame(info)
            tickers = tickers.append(temp_df,ignore_index=True)
    return tickers


def make_request(url, method='GET', headers=None, json=None, data=None):
    if headers is None:
        headers = GENERIC_HEADERS
    if method == 'GET':
        return requests.get(url, headers=headers)
    elif method == 'POST':
        return requests.post(url, json=json, headers=headers, data=None)
    raise ValueError(f'Invalid method {method}')