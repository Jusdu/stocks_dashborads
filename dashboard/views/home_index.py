import os
import numpy as np
import pandas as pd

import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Kline, Line
from streamlit_echarts import st_pyecharts




# 1. func - load data
#--------------------------
@st.cache_resource
def load_index_data(index_name:str):
    """加载指数数据
    """
    index_data = pd.read_parquet(rf'data\index\{index_name}.parquet')
    return index_data






# 2. func - plot
#--------------------------
@st.cache_data()
def st_index_plot_01(index_data):
    '''指数ohlc可视化'''
    index_data = index_data.droplevel(1)
    kline = (
        Kline(
            init_opts=opts.InitOpts(width="100%", height="1000px")
        ).add_xaxis(
            index_data.index.strftime('%Y-%m-%d').tolist()
        ).add_yaxis(
            series_name="上证指数",
            y_axis=index_data[['open','close','low','high']].values.tolist(), # 必须是[open, close, low, high]
            itemstyle_opts=opts.ItemStyleOpts(
                color="#ef232a",       # 上涨红色
                color0="#14b143",      # 下跌绿色
                border_color="#ef232a",
                border_color0="#14b143",
            )
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="", is_show=False),
            legend_opts=opts.LegendOpts(pos_top="20px", pos_left="center"),
            xaxis_opts=opts.AxisOpts(type_="category", name="日期"),
            yaxis_opts=opts.AxisOpts(is_scale=True),
            # yaxis_opts=opts.AxisOpts(is_scale=True, min_="dataMin", max_="dataMax"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            datazoom_opts=[
                opts.DataZoomOpts(          # 缩放条
                    range_start=0,          # 从0%
                    range_end=100           # 到100%，即全宽
                ), opts.DataZoomOpts(type_="inside")
            ]
        )
    )
    return kline



# 0. main - head
#--------------------------
st.title("Home Page — 主页")
st.markdown("___", unsafe_allow_html=True)
# st.text("")  # 空行
# st.text("")  # 空行

# st.sidebar.subheader("📑 页面目录")
# st.sidebar.markdown(
#     """
#     [Factor](#factor)  
#     [Factor IC](#factor-ic)  
#     [Factor Grouped](#factor-grouped)  
#     """
# )

col1 = st.columns(9)[0]
with col1:
    index_file_lst = os.listdir(r'data\index')
    index_lst = [index_file.split('.')[0] for index_file in index_file_lst]
    select_index_name = st.selectbox("指数列表", index_lst, index=index_lst.index('上证指数'))  # 默认第一个指数
index_data = load_index_data(select_index_name)
kline = st_index_plot_01(index_data)
st_pyecharts(kline, height="500px")
