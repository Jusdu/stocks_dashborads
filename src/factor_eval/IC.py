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

    def calc_IC(self, ret_nd:List=[1,5,10], method:Literal['pearson', 'spearman']='pearson'):

        ## 计算未来收益率
        return_data_lst = []
        for nd in ret_nd:
            forward_return_data = (
                data.close
                .unstack()
                .pct_change(nd, fill_method=None)
                .shift(-nd)     # 计算已知的未来收益
                .stack()
            )
            return_data_lst.append(forward_return_data)
        forward_return_data = pd.concat(return_data_lst, axis=1)
        forward_return_data.columns = [f'ret_lags_{nd}d' for nd in ret_nd]
        # print(return_data)

        ## 获取因子值
        factor_ret_data = pd.concat([factor_df, forward_return_data], axis=1)
        factor_IC = factor_ret_data.groupby('date').apply(
            lambda x: x.corr(method=method).iloc[1:, 0]
        ).dropna(how='all')
        # print(factor_ret_corr)
        ## 计算当月因子均值
        monthly_factor_IC = factor_IC.groupby(pd.Grouper(level=0, freq='MS')).mean()
        return monthly_factor_IC


if __name__ == '__main__':
    data = pd.read_parquet(r'D:\Coding\repo\stocks_dashborads\data\raw\all.parquet')
    factor_df = pd.read_parquet(r'D:\Coding\repo\stocks_dashborads\data\factors\momentum\lags_pct_14.parquet')

    EVAL = EVALUATION(data, factor_df)
    factor_IC = EVAL.calc_IC()
    print(factor_IC)