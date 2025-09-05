# -*- encoding: utf-8 -*-
'''
@File    : volatility.py
@Date    : 2025-09-04 17:05:46
@Author  : DDB
@Version : 1.0
@Desc    : 计算波动因子
'''

import numpy as np
import pandas as pd
from typing import *



class VOLATILITY:
    '''波动因子类'''
    def __init__(self, data, is_lags:bool=False):
        """_summary_

        Args:
            data (_type_): _description_
            is_lags (bool, optional): 因子数据是否延期 1 日.
        """
        self.data = data
        self.is_lags = is_lags


    def hist_volatility_n(self, days:int=24):
        '''N日的历史对数收益率的波动率'''
        close_df = self.data.close.unstack()
        ln_rt_df = np.log(close_df / close_df.shift(1))
        if self.is_lags:
            ln_rt_df = ln_rt_df.shift(1)
        std_df = ln_rt_df.rolling(days).std(ddof=1)
        factors = pd.DataFrame(std_df.stack())
        factors.columns = [f'hist_volatility_{days}']
        return factors
    
    def hist_vol_std_n(self, days:int=10):
        """N日成交量的历史波动率

        Args:
            days (int, optional): _description_. Defaults to 10.
        """
        vol_df = self.data.volume.unstack()
        ln_vol_df = np.log(vol_df)
        if self.is_lags:
            ln_vol_df = ln_vol_df.shift(1)
        std_df = ln_vol_df.rolling(days).std(ddof=1)
        factors = pd.DataFrame(std_df.stack())
        factors.columns = [f'hist_vol_std_{days}']
        return factors
