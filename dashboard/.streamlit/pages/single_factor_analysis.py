import pandas as pd
import numpy as np
from typing import *

import os
import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Line
from streamlit_echarts import st_pyecharts

## Local
from src.factor_eval.get_eval import EVALUATION




'''
#------------------------------------------------------------------------
func
#------------------------------------------------------------------------
'''
@st.cache_data()
def load_data():
    data_path = r'.\data\raw\all.parquet'
    data = pd.read_parquet(data_path)
    return data

@st.cache_data()
def load_factor_df(factor_typeI, factor_name):
    factor_path = rf'.\data\factors\{factor_typeI}\{factor_name}.parquet'
    factor_df = pd.read_parquet(factor_path)
    return factor_df

@st.cache_data()
def st_load_factor_IC(evaluation, IC_type:Literal['IC', 'Rank-IC']):
    
    method = 'pearson' if IC_type.lower().startswith('i') else 'spearman'
    factor_IC = evaluation.calc_IC(factor_df, method)
    return factor_IC

@st.cache_data()
def st_load_factor_grouped_ret(evaluation, group_type:Literal['quantile', 'bins'], group_lens):
    
    factor_grouped_ret = evaluation.calc_grouped_ret(group_type, group_lens)
    return factor_grouped_ret


# 1. func - load data
#--------------------------
class DataLoader:
    def __init__(
            self, 
            factor_typeI: str = None, 
            factor_name: str = None,
            ret_nd: List = None,
            ):
        """
        :param factor_typeI: 因子类型一级目录 (例如 'momentum' 或 'value')
        :param factor_name: 因子文件名 (不带后缀)
        """
        self.factor_typeI = factor_typeI
        self.factor_name = factor_name
        self.ret_nd = ret_nd

        self.__init_load_factor_data__()
        # TODO 解决 eval类的缓存
        # self.__init_load_factor_evaluation__()

    
    # default data
    #-------------
    def __init_load_factor_data__(self):
        """加载默认数据
        """
        self.data = load_data()
        self.factor_df = load_factor_df(factor_typeI, factor_name)


    # # factor evaluation data
    # #-----------------------
    # def __init_load_factor_evaluation__(self):
    #     self.evaluation = EVALUATION(self.data, self.factor_df, self.ret_nd)
        
    # def load_factor_IC(self, IC_type):

    #     factor_IC = st_load_factor_IC(self.evaluation, IC_type)
    #     return factor_IC


    
@st.cache_data
def st_dataloader():
    dataloader = DataLoader(
        factor_typeI = factor_typeI,
        factor_name = factor_name,
        ret_nd = [1,5,10,22]
    )
    return dataloader


# 2. func - plot
#--------------------------
def st_IC_retnd_plot(factor_IC):
    # main Line
    line = Line(init_opts=opts.InitOpts(width="100%", height="600px"))
    line.add_xaxis(factor_IC.index.strftime("%Y-%m-%d").tolist())

    cols = factor_IC.columns
    for i, col in enumerate(cols):
        opacity_val = 0.4 if i < 3 else 1.0  # 前3列透明度0.4
        line.add_yaxis(
            series_name=col,
            y_axis=factor_IC[col].round(3).tolist(),
            is_symbol_show=False,
            linestyle_opts=opts.LineStyleOpts(width=2, opacity=opacity_val),
        )

    # 全局配置
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="", is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category", name="日期"),
        yaxis_opts=opts.AxisOpts(name="IC", is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True)),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[
            opts.DataZoomOpts(          # 缩放条
                range_start=0,          # 从0%
                range_end=100           # 到100%，即全宽
            ), opts.DataZoomOpts(type_="inside")]
    )
    return line



'''
#------------------------------------------------------------------------
main
#------------------------------------------------------------------------
'''

# 0. main - head
#--------------------------
st.title("Single Factor Analysis — 单因子分析")
st.markdown("___", unsafe_allow_html=True)
st.text("")  # 空行
st.text("")  # 空行

st.sidebar.subheader("📑 页面目录")  # 目录标题
st.sidebar.markdown(
    """
    [factor](#factor)  
    [factor IC](#factor-IC)  
    [factor grouped](#factor-grouped)  
    """
)


# 1. main - single factor
#--------------------------
st.subheader('factor')
## 1.1 因子选择
col1, col2, col3,= st.columns(3)
with col1:  
    factor_typeI_lst = os.listdir(r'data\factors')
    factor_typeI = st.selectbox("因子大类", factor_typeI_lst, index=0)  # 默认第一个板块
    factor_typeI_path = os.path.join(r'data\factors', factor_typeI)
with col2:
    factor_name_lst = [factor_name.split('.')[0] for factor_name in os.listdir(factor_typeI_path)]
    factor_name = st.selectbox("因子", factor_name_lst, index=0)
with col3:
    IC_type = st.selectbox("IC type", ['IC', 'Rank-IC'], index=0)

## 1.2 factor data
dataloader = DataLoader(
    factor_typeI,
    factor_name,
    ret_nd=[1,5,10,22]
)
factor_df, data = dataloader.factor_df, dataloader.data


## 1.3 factor_values
with st.expander("区间因子值 - 示例", expanded=False):
    factor_date_lst = factor_df.index.get_level_values(0).unique().strftime('%Y-%m-%d')
    select_s_date, select_e_date = st.select_slider(
        "_",
        options=factor_date_lst,
        value=(factor_date_lst[-16], factor_date_lst[-1]),  # 默认选最后一天
        label_visibility='collapsed'
    )
    factor_df_str = factor_df.round(4).astype(str)
    factor_df_str = factor_df_str.loc[select_s_date: select_e_date].unstack().T.droplevel(0).head(10)
    factor_df_str.columns = factor_df_str.columns.strftime('%Y-%m-%d')
    st.dataframe(
        factor_df_str.style
        .set_properties(**{'text-align': 'center'})
        .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])
    )

st.text("")  # 空行
st.text("")  # 空行


# 2. main - factor IC
#--------------------------
## IC
st.subheader('factor IC')
factor_IC = dataloader.load_factor_IC(IC_type=IC_type)
Line_IC_ret_nd = st_IC_retnd_plot(factor_IC)
st_pyecharts(Line_IC_ret_nd, height="500px", width="100%")

st.text("")  # 空行
st.text("")  # 空行

# 3. main - factor grouped
#--------------------------
st.subheader('factor grouped')
# load_factor_grouped_ret()