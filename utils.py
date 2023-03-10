import functools
import pandas as pd

def df_file_cache(cache_name , dir='c:/temp/pickles'):
    ''' Decorator that caches function dataframe output as pkl files'''
    def _decorator(f):
        @functools.wraps(f)
        def _inner(*args, **kwargs):
            """A wrapper function"""
            key = "_".join([str(x) for x in args]) + "~"+"_".join([f'{str(k)}={str(v)}' for k,v in kwargs.items()])
            fname = f'{dir}/{cache_name}_{key}.pkl'
            try:
                return pd.read_pickle(fname)
            except:
                pass
            df = f(*args,**kwargs)
            df.to_pickle(fname)
            return df
        return _inner
    return _decorator

