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
        ret_nd = self.ret_nd if self.ret_nd else [1,5,10]

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
        forward_return_data = pd.concat(return_data_lst, axis=1)
        forward_return_data.columns = [f'forward_ret_{nd}d' for nd in ret_nd]
        return forward_return_data

    @staticmethod
    def calc_IC(factor_df, forward_return_data, method:Literal['pearson', 'spearman']='pearson'):

        ## 获取因子值
        factor_ret_data = pd.concat([factor_df, forward_return_data], axis=1)
        factor_IC = factor_ret_data.groupby('date').apply(
            lambda x: x.corr(method=method).iloc[1:, 0]
        ).dropna(how='all')

        ## 计算当月因子均值
        monthly_factor_IC = factor_IC.groupby(pd.Grouper(level=0, freq='MS')).mean()
        return monthly_factor_IC
    

    def calc_grouped_ret(self, forward_return_data, group_type:Literal['quantile', 'bins'], group_lens:int=10):
        """计算分组收益
        """

        factor_df = self.factor_df
        print(factor_df)
        factor_df['']






if __name__ == '__main__':
    data = pd.read_parquet(r'E:\repo\stocks_dashborads\data\raw\all.parquet')
    factor_df = pd.read_parquet(r'E:\repo\stocks_dashborads\data\factors\momentum\lags_pct_14.parquet')

    EVAL = EVALUATION(data, factor_df)
    factor_IC = EVAL.calc_IC()
    print(factor_IC)