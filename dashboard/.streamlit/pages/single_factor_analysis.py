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

# 1. func - load data
#--------------------------
@st.cache_data(ttl=3600)  # 缓存 1 小时
def load_factor_df(factor_typeI, factor_name):
    factor_path = rf'.\data\factors\{factor_typeI}\{factor_name}.parquet'
    factor_df = pd.read_parquet(factor_path)
    return factor_df

@st.cache_data(ttl=3600)  # 缓存 1 小时
def load_data():
    data_path = r'.\data\raw\all.parquet'
    data = pd.read_parquet(data_path)
    return data

@st.cache_data(ttl=3600)
def load_factor_IC(data, factor_df, ret_nd:List, IC_type:Literal['IC', 'Rank-IC']):
    EVAL = EVALUATION(data, factor_df)
    # IC
    if IC_type.lower().startswith('i'):
        factor_IC = EVAL.calc_IC(ret_nd, method='pearson')
    # Rank - IC
    else:
        factor_IC = EVAL.calc_IC(ret_nd, method='spearman')
    return factor_IC


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
    [factor distribution](#factor-distribution)  
    """
)



# 1. main - single factor
#--------------------------
st.subheader('factor')
# 1.1 因子选择
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

## factor data
factor_df = load_factor_df(factor_typeI, factor_name)
data = load_data()
factor_IC = load_factor_IC(data, factor_df, ret_nd=[1,5,10,22], IC_type=IC_type)
## other data
factor_date_lst = factor_df.index.get_level_values(0).unique().strftime('%Y-%m-%d')

## 1.2 factor_values
with st.expander("区间因子值 - 示例", expanded=False):
    
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
Line_IC_ret_nd = st_IC_retnd_plot(factor_IC)
st_pyecharts(Line_IC_ret_nd, height="500px", width="100%")

st.text("")  # 空行
st.text("")  # 空行

# 3. main - factor distribution
#--------------------------
st.subheader('factor distribution')
