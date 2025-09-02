# -*- encoding: utf-8 -*-
'''
@File    : momentum.py
@Date    : 2025-09-01 16:52:39
@Author  : DDB
@Version : 1.0
@Desc    : 计算动量因子
'''

import numpy as np
import pandas as pd
from typing import *



class MOMENTUM:
    '''动量因子类'''
    def __init__(self, data, is_lags:bool=False):
        """_summary_

        Args:
            data (_type_): _description_
            is_lags (bool, optional): 因子数据是否延期 1 日.
        """
        self.data = data
        self.is_lags = is_lags


    def lags_pct_(self, lags:int=14):
        '''前N日的收益率'''
        factors = self.data.close.unstack()
        factors = factors.pct_change(lags, fill_method=None)
        if self.is_lags:
            factors = factors.shift(1)
        factors = pd.DataFrame(factors.stack())
        factors.columns = [f'momentum_lags_{lags}_pct']
        return factors
