# -*- encoding: utf-8 -*-
'''
@File    : getData.py
@Date    : 2025-03-21 11:05:33
@Author  : DDB
@Version : 1.0
@Desc    : 掘金API的封装
'''


## goldmine
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *

## local
from src.read_token import get_token

## research needed
from datetime import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import *



class GOLDMINE:
    
    def __init__(self, token:str=None):

        ## set token
        if not token:
            token = get_token()
        self.token = token
        set_token(self.token)



    def get_symbols(
            self, 
            type:Literal['all', 'main', 'cy', 'kc']='all', 
            is_trade:bool=False
        )-> List[str]:
        """获取上证、深证股票 symbol

        Args:
            type (Literal[&#39;all&#39;, &#39;main&#39;, &#39;cy&#39;, &#39;kc&#39;]): ['全市', '主板', '创业', '科创']
            is_trade (bool): 筛选是否已经退市
        """
        data = get_symbols(sec_type1=1010, sec_type2=101001, df=True)
        type_lower = type.lower()
        type_dict = {
            'main': 10100101,
            'cy': 10100102,
            'kc': 10100103
        }

        if is_trade:
            data = data[(data['delisted_date'] >= '2038-01-01')]

        # 全 A 股
        if type_lower == 'all':
            symbols = data['symbol'].tolist()
        # A 股主板
        else:
            data = data[data.board == type_dict[type_lower]]
            symbols = data['symbol'].tolist()

        return symbols
    

    def get_ohlcv(
            self, 
            symbol_list:list | str = None,
            start_date:str = '2025-01-01',
            end_date:str = None,
            split:int = 1,
            freq:str = '1d',
            adj:int = 1
    ) -> pd.DataFrame:
        
        if not symbol_list: 
            symbol_list = self.get_symbols()
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        price_list = []
        if split > 1:
            dateRange = np.array_split(pd.date_range(start_date, end_date).strftime('%Y-%m-%d'), int(split))
            for Range in tqdm(dateRange):
                piece = history(symbol_list, frequency=freq, start_time=Range[0], end_time=Range[-1], adjust=adj, df=True)
                price_list.append(piece)
        else:
            piece = history(symbol_list, frequency=freq, start_time=start_date, end_time=end_date, adjust=adj, df=True)
            price_list.append(piece)

        price = pd.concat(price_list, axis=0)
        if price.empty: 
            return pd.DataFrame()
        price.eob = price.eob.dt.tz_localize(None)
        price = price.set_index(['eob', 'symbol']).drop(['frequency', 'position', 'bob'], axis=1)
        price.index.names = ['date', 'symbol']
        return price
    




if __name__ == '__main__':
    
    gm = GOLDMINE()
    for symbol_type in tqdm(['all', 'main', 'cy', 'kc']):
        symbols = gm.get_symbols(symbol_type)
        data = gm.get_ohlcv(symbols, start_date='2024-01-01', adj=1, split=int(len(symbols)/300))
        data.to_parquet(rf'./data/{symbol_type}.parquet')