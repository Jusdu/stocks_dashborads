# -*- encoding: utf-8 -*-
'''
@File    : emotion.py
@Date    : 2025-09-04 14:42:01
@Author  : DDB
@Version : 1.0
@Desc    : 计算情绪因子
'''


import numpy as np
import pandas as pd
from typing import *



class EMOTION:
    '''情绪因子类'''
    def __init__(self, data, is_lags:bool=False):
        """_summary_

        Args:
            data (_type_): _description_
            is_lags (bool, optional): 因子数据是否延期 1 日.
        """
        self.data = data
        self.is_lags = is_lags


    def psy_n(self, days:int=12):
        '''N日的心理线'''
        factors = self.data.close.unstack()
        factors =(factors.diff() > 0).astype(int) # 上涨天=1, 否则=0
        if self.is_lags:
            factors = factors.shift(1)
        factors = factors.rolling(days).sum() / days * 100
        factors = pd.DataFrame(factors.stack())
        factors.columns = [f'emotion_psy_{days}']
        return factors
    
    def upDownCount_n(self):
        """今日的涨跌停家数

        Args:
            days (int, optional): _description_. Defaults to 10.
        """
        factors = self.data.close.unstack()
        factors = (factors.diff() > 0).astype(int) # 上涨天=1, 否则=0
        if self.is_lags:
            factors = factors.shift(1)
        factors = factors.sum(axis=1)
        factors = pd.DataFrame(factors)
        factors.columns = [f'upDownCount_']
        return factors



