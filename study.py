import data
import logging
import datetime
import numpy as np
def main():
    logging.basicConfig(level=logging.DEBUG)
    start = datetime.date(2022,3,1)
    end = datetime.date(2023,3,1)
    daily = data.getDailyData(start,end)
    logging.debug(f'Got daily data of shape{daily.shape}')
    logreturns = (1+((daily['Close'] - daily.shift(1)['Close']) / daily.shift(1)['Close'])).apply(np.log)
    secs = daily['Close'].columns
    closes = daily['Close']
    secs = closes.columns
    logreturns = closes.copy()
    for sec in secs:
        logreturns[sec]
if __name__ == '__main__':
    main()