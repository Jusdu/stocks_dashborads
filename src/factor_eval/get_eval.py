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

    def __init__(self, data, factor_df, ret_nd):
        self.data = data
        self.factor_df = factor_df
        self.ret_nd:List = ret_nd

        self.__init_calc__()
    
    
    def __init_calc__(self):
        """初始计算
        """
        self.forward_return_data = self.calc_forward_ret_data()


    def calc_forward_ret_data(self):
        """计算未来收益率
        """
        ## params init
        ret_nd = self.ret_nd if self.ret_nd else [1,5,10,22]

        return_data_lst = []
        for nd in ret_nd:
            forward_return_data = (
                self.data.close
                .unstack()
                .pct_change(nd, fill_method=None)
                .shift(-nd)     # 计算已知的未来收益
                .stack()
            )
            return_data_lst.append(forward_return_data)
        forward_return_data = pd.concat(return_data_lst, axis=1).sort_index()
        forward_return_data.columns = [f'forward_ret_{nd}d' for nd in ret_nd]
        return forward_return_data


    def calc_IC(self, method:Literal['pearson', 'spearman']='pearson'):

        ## 获取因子值
        factor_ret_data = pd.concat([self.factor_df, self.forward_return_data], axis=1)
        factor_IC = factor_ret_data.groupby('date').apply(
            lambda x: x.corr(method=method).iloc[1:, 0]
        ).dropna(how='all')

        ## 计算当月因子均值
        monthly_factor_IC = factor_IC.groupby(pd.Grouper(level=0, freq='MS')).mean()
        monthly_factor_IC.columns = [f'IC_{col.split('_')[-1]}' for col in monthly_factor_IC.columns]
        return monthly_factor_IC


    def calc_grouped(self, quantile:int=10, bins:int=None):
        """计算分组收益
        """
        cut = pd.qcut if quantile else pd.cut
        lens = quantile if quantile else bins
        factor_df = self.factor_df.copy()

        factor_df['grouped'] = factor_df.groupby('date')[factor_df.columns[0]].transform(
            lambda s: cut(s, lens, labels=False, duplicates='drop')
        )
        ## 组号从 1 开始
        factor_df['grouped'] += 1

        # 因子分组分布 - data
        factor_describe = factor_df.groupby('grouped').describe()
        factor_describe.columns = [col[-1] for col in factor_describe.columns]

        # 因子分组收益率
        forward_ret_data = self.forward_return_data.copy()
        forward_ret_data.columns = [f'{col.split('_')[-1]}' for col in forward_ret_data.columns]
        factor_grouped_forward_ret = pd.concat(
            [forward_ret_data, factor_df['grouped']], axis=1
        ).dropna(how='all')
        factor_grouped_forward_ret = factor_grouped_forward_ret.groupby(
            ['grouped', factor_grouped_forward_ret.index.get_level_values(0)]
        ).mean()


        return factor_describe, factor_grouped_forward_ret
        


if __name__ == '__main__':
    data = pd.read_parquet(r'E:\repo\stocks_dashborads\data\raw\all.parquet')
    factor_df = pd.read_parquet(r'E:\repo\stocks_dashborads\data\factors\momentum\lags_pct_14.parquet')

    EVAL = EVALUATION(data, factor_df)
    factor_IC = EVAL.calc_IC()
    print(factor_IC)