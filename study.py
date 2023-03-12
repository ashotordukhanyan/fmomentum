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
    #clean nas
    shartShape = logreturns.shape
    logreturns.dropna(axis=0, how='all', inplace=True)
    if logreturns.shape != shartShape:
        logging.warning(f'Dropping {shartShape[0]-logreturns.shape[0]} dates with NA values')
        shartShape = logreturns.shape
    logreturns.dropna(axis=1, how='any', inplace=True)
    if logreturns.shape != shartShape:
        logging.warning(f'Dropping {shartShape[1]-logreturns.shape[1]} instruments with NA values')
        shartShape = logreturns.shape
    #drop rows witl all nas

if __name__ == '__main__':
    main()