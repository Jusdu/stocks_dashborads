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
        factors.columns = [f'momentum_lags_{lags}_pct']
        return factors
    

    def N_slope(self, n:int=14):
        """前 N 日的斜率"""
        # y
        Close_df = self.data.close.unstack()
        arr = Close_df.values

        # x
        x = np.arange(n)
        weights = x - x.mean()
        denom = np.sum(weights**2)

        # 每列窗口标准化
        y_mean = Close_df.rolling(n).mean().to_numpy()
        y_std = Close_df.rolling(n).std(ddof=0).to_numpy()
        y_norm = (arr - y_mean) / y_std

        # 卷积计算 slope
        slopes = np.apply_along_axis(
            lambda col: np.convolve(col, weights[::-1], mode="valid") / denom,
            axis=0,
            arr=y_norm
        )

        # 对齐 index/columns
        factors = pd.DataFrame(np.full_like(arr, np.nan, dtype=float),
                        index=Close_df.index, columns=Close_df.columns)
        factors.iloc[n-1:, :] = slopes
        
        if self.is_real:
            factors = factors.shift(1)
        factors = pd.DataFrame(factors.stack())
        factors.columns = [f'{n}d_slope']
        return factors

