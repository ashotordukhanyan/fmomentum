import pandas as pd
import yfinance as yf
import finnhub
import functools
from typing import List
import logging
import datetime
from utils import df_file_cache
import pandas_market_calendars as mcal

@functools.lru_cache(maxsize=1)
def getFinHubClient():
    from  secretkeys import FINHUB_API_KEY
    return finnhub.Client(api_key=FINHUB_API_KEY)

@functools.lru_cache(maxsize=10,typed=True)
def getIndexConstituents( idx:str) -> List[str]:
    res =  getFinHubClient().indices_const(symbol=idx)
    assert res['symbol'] == idx, f'{res["symbol"]}!={idx}'
    return res['constituents']

SPDR_SECTOR_ETFS = "XLC XLY XLP XLE XLF XLV XLI XLB XLRE XLK XLU".split()
BROAD_MKT_ETFS = 'SPY QQQ RUI RUT RUA'.split()

@functools.lru_cache(maxsize=1)
def getUniverse(name:str) -> List[str]:
    if name == 'REGULAR':
        return sorted(list(set(getIndexConstituents('^RUI')+SPDR_SECTOR_ETFS + BROAD_MKT_ETFS)))
    else:
        raise ('UNDEFINED UNIVERSE ' + name)

@functools.lru_cache(maxsize=5)
@df_file_cache(cache_name='daily')
def getDailyData(start:datetime.date,end:datetime.date,universe:str='REGULAR', calendar = 'NYSE') -> pd.DataFrame:
    tickers = yf.Tickers(getUniverse(universe))
    cal = mcal.get_calendar(calendar)
    daily = tickers.history(interval='1d',start=start,end=end)
    valid_days = cal.valid_days(start,end).tz_localize(None)
    return daily[daily.index.isin(valid_days)]
