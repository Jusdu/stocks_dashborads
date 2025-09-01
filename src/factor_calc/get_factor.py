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


class FACTORS:
    
    def __init__(self, data):
        self.save_path = r'.\data\factors'
        self.momentum = MOMENTUM(data, is_lags=False)


    def to_save(self, factor_df, factor_type, factor_name):
        factor_df.to_parquet(os.path.join(self.save_path, rf'{factor_type}/{factor_name}'))
    

    def all_to_save(self):

        # momentum
        for i in [14, 28]:
            factor_lags_pct_n_df = self.momentum.lags_pct_(i)
            self.to_save(factor_lags_pct_n_df, 'momentum', f'lags_pct_{i}.parquet')


if __name__ == '__main__':

    data = pd.read_parquet(r'E:\repo\stocks_dashborads\data\raw\all.parquet')
    Factors = FACTORS(data)
    Factors.all_to_save()
    # factor1 = Factors.momentum.lags_pct_()
