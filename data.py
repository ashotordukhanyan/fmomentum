import pandas as pd
import yfinance as yf
import finnhub
import functools
from typing import List
import logging
import datetime
from utils import df_file_cache

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
def getDailyData(start:datetime.date,end:datetime.date,universe:str='REGULAR') -> pd.DataFrame:
    tickers = yf.Tickers(getUniverse(universe))
    return tickers.history(interval='1d',start=start,end=end)
#
# def testIC():
#     logging.basicConfig(level=logging.DEBUG)
#     idxs = 'GSPC RUI RUT RUA'.split()
#     constituents = {i:tuple(getIndexConstituents('^'+i)) for i in idxs}
#     # for i,c in constituents.items():
#     #     logging.info(f'{i} has {len(c)} constituents')
#     for i in range(len(idxs)):
#         for j in range(i+1,len(idxs)):
#             ci = constituents[idxs[i]]
#             cj = constituents[idxs[j]]
#             logging.info(f"{idxs[i]}({len(ci)}) and {idxs[j]}({len(cj)}) have {len(set(ci)&set(cj))} common constituents")

#if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    #testIC()