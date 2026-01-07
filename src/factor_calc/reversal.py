# -*- encoding: utf-8 -*-
'''
@File    : reversal.py
@Date    : 2025-10-28 10:14:03
@Author  : DDB
@Version : 1.0
@Desc    : 反转因子集合
'''

import numpy as np
import pandas as pd
from typing import *

class REVERSAL:
    '''反转因子类'''
    def __init__(self, data, is_real:bool=False):
        """_summary_

        Args:
            data (_type_): _description_
            is_real (bool, optional): 因子数据是否延期 1 日.
        """
        self.data = data
        self.is_real = is_real


    def lags_pct_(self, lags:int=14):
        '''前N日的收益率'''
        factors = self.data.close.unstack()
        factors = factors.pct_change(lags, fill_method=None)
        if self.is_real:
            factors = factors.shift(1)
        factors = pd.DataFrame(factors.stack())
        factors.columns = [f'lags_{lags}_pct']
        return factors