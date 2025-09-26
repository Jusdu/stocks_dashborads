# -*- encoding: utf-8 -*-
'''
@File    : calc_factor.py
@Date    : 2025-08-22 14:47:43
@Author  : DDB
@Version : 1.0
@Desc    : 计算因子并储存到 data/factors/
'''

import os
import pandas as pd
from src.factor_calc.momentum import MOMENTUM
from src.factor_calc.emotion import EMOTION
from src.factor_calc.volatility import VOLATILITY


class FACTORS:
    
    def __init__(self, data_ohlcv):
        self.save_path = r'.\data\factors'
        self.momentum = MOMENTUM(data_ohlcv, is_lags=False)
        self.emotion = EMOTION(data_ohlcv, is_lags=False)
        self.volatility = VOLATILITY(data_ohlcv, is_lags=False)


    def to_save(self, factor_df, factor_type, factor_name):
        factor_df.to_parquet(os.path.join(self.save_path, rf'{factor_type}/{factor_name}'))
    

    def all_to_save(self):

        # momentum
        #-----------------------------
        # for i in [14, 28]:
            # factor_lags_pct_n_df = self.momentum.lags_pct_(i)
            # self.to_save(factor_lags_pct_n_df, 'momentum', f'lags_pct_{i}.parquet')

        i = 14
        factor_N_slope = self.momentum.N_slope(i)
        self.to_save(factor_N_slope, 'momentum', f'slope_{i}.parquet')
        # print(factor_N_slope)

        # # emotion
        #-----------------------------
        # for i in [12, 24]:
        #     psy_n_df = self.emotion.psy_n(i)
        #     self.to_save(psy_n_df, 'emotion', f'psy_{i}.parquet')

        # upDownCount = self.emotion.upDownCount_n()
        # self.to_save(upDownCount, 'emotion', f'upDownCount.parquet')

        # volatility
        # for i in [12, 24]:
        #     hist_volatility_n_df = self.volatility.hist_volatility_n(i)
        #     self.to_save(hist_volatility_n_df, 'volatility', f'hist_volatility_{i}.parquet')
        
        # for i in [10, 20]:
        #     hist_vol_std_n_df = self.volatility.hist_vol_std_n(i)
        #     self.to_save(hist_vol_std_n_df, 'volatility', f'hist_vol_std_n{i}.parquet')


if __name__ == '__main__':

    data = pd.read_parquet(r'.\data\raw\all.parquet')
    Factors = FACTORS(data)
    Factors.all_to_save()
    # factor1 = Factors.momentum.lags_pct_()
