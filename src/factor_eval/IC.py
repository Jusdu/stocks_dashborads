# -*- encoding: utf-8 -*-
'''
@File    : concat_data.py
@Date    : 2025-09-01 17:37:01
@Author  : DDB
@Version : 1.0
@Desc    : 计算 IC
'''

import numpy as np
import pandas as pd
from typing import *


class EVALUATION:

    def __init__(self, data, factor_df):
        self.data = data
        self.factor_df = factor_df

    def calc_IC(self, ret_nd:List=[1,5,10]):

        ## 计算未来收益率
        return_data_lst = []
        for nd in ret_nd:
            return_data = (
                data.close
                .unstack()
                .pct_change(nd, fill_method=None)
                .shift(-nd)     # 计算已知的未来收益
                .stack()
            )
            return_data_lst.append(return_data)
        return_data = pd.concat(return_data_lst, axis=1)
        return_data.columns = [f'ret_lags_{nd}d' for nd in ret_nd]
        # print(return_data)

        ## 获取因子值
        factor_ret_data = pd.concat([factor_df, return_data], axis=1)
        factor_ret_corr = factor_ret_data.groupby('date').apply(
            lambda x: x.corr(method='pearson').iloc[1:, 0]
        ).dropna(how='all')
        print(factor_ret_corr)

if __name__ == '__main__':
    data = pd.read_parquet(r'E:\repo\stocks_dashborads\data\raw\all.parquet')
    factor_df = pd.read_parquet(r'E:\repo\stocks_dashborads\data\factors\momentum\lags_pct_14.parquet')

    EVAL = EVALUATION(data, factor_df).calc_IC()