import pandas as pd
import numpy as np
from typing import *

import os
import yaml
import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Kline
from streamlit_echarts import st_pyecharts
from pyecharts.commons.utils import JsCode

## Local
from src.factor_eval.get_eval import EVALUATION




'''
#------------------------------------------------------------------------
func
#------------------------------------------------------------------------
'''


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


    # default data
    #-------------
    def __init_load_factor_data__(self):
        """加载默认数据
        """
        self.data = self.load_data()
        self.factor_df = self.load_factor_df()
        self.factor_desc = self.load_factor_desc()
    
    def load_data(self):
        data_path = r'.\data\raw\all.parquet'
        data = pd.read_parquet(data_path)
        return data
    
    def load_factor_df(self):
        factor_path = rf'.\data\factors\{self.factor_typeI}\{self.factor_name}.parquet'
        factor_df = pd.read_parquet(factor_path)
        return factor_df
    
    def load_factor_desc(self):
        with open(rf".\data\factor_desc.yaml", "r", encoding="utf-8") as f:
            desc_dict = yaml.safe_load(f)
        return desc_dict.get(self.factor_typeI, {}).get(self.factor_name, {})

    # factor evaluation data
    #-----------------------
    def load_factor_IC(self, IC_type:Literal['IC', 'Rank-IC']):
        return compute_factor_IC(self.data, self.factor_df, self.ret_nd, IC_type)
    
    def load_factor_grouped_ret(self, quantile:int=10, bins:int=None):
        return compute_factor_grouped_ret(self.data, self.factor_df, self.ret_nd, quantile=quantile, bins=bins)


@st.cache_data
def compute_factor_IC(data, factor_df, ret_nd, IC_type: str):
    evaluation = EVALUATION(data, factor_df, ret_nd)
    method = 'pearson' if IC_type.lower().startswith('i') else 'spearman'
    return evaluation.calc_IC(method)

@st.cache_data
def compute_factor_grouped_ret(data, factor_df, ret_nd, quantile:int=10, bins:int=None):
    evaluation = EVALUATION(data, factor_df, ret_nd)
    return evaluation.calc_grouped_ret(quantile, bins)

@st.cache_resource
def get_loader(factor_typeI:str, factor_name:str, ret_nd:List) -> DataLoader:
    return DataLoader(factor_typeI, factor_name, ret_nd)





# 2. func - plot
#--------------------------

def st_IC_retNd_plot(factor_IC):
    # ---------------- 计算 cumIC ----------------
    factor_cumIC = factor_IC.cumsum().round(3).astype(float)
    factor_cumIC.columns = ['Cum' + col for col in factor_cumIC.columns]

    # ---------------- 主柱状图 ----------------
    bar = Bar(init_opts=opts.InitOpts(width="100%", height="600px"))
    bar.add_xaxis(factor_IC.index.strftime("%Y-%m-%d").tolist())

    LegendSelected = {}
    cols = factor_IC.columns
    for i, col in enumerate(cols):
        is_default_selected = False if i < len(cols) - 1 else True
        LegendSelected[col] = is_default_selected

        opacity_val = 0.6 if i < len(cols) - 1 else 1.0
        bar.add_yaxis(
            series_name=col,
            y_axis=factor_IC[col].round(3).tolist(),
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(opacity=opacity_val),
            # bar_width="100%",  # 这里控制柱子宽度，默认是 "60%" 左右
        )

    # ---------------- 右轴累计IC折线 ----------------
    bar.extend_axis(
        yaxis=opts.AxisOpts(
            name="cum_IC",
            type_="value",
            position="right",
            # split_number=5,
            axisline_opts=opts.AxisLineOpts(),
            axislabel_opts=opts.LabelOpts(),
            splitline_opts=opts.SplitLineOpts(is_show=False),  # 只保留左边网格线
        )
    )

    line = Line()
    line.add_xaxis(factor_IC.index.strftime("%Y-%m-%d").tolist())
    for i, col in enumerate(factor_cumIC):
        is_default_selected = False if i < len(cols) - 1 else True
        LegendSelected[col] = is_default_selected

        opacity_val = 0.6 if i < len(cols) - 1 else 1.0
        line.add_yaxis(
            series_name=col,
            y_axis=(factor_cumIC[col]).tolist(),  # 映射后的值
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(opacity=opacity_val),
            yaxis_index=1  # 指定右轴
        )

    # ---------------- 组合 ----------------
    bar.overlap(line)
    bar.set_series_opts(z=1)
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="因子时序 IC", is_show=True),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axislabel_opts=opts.LabelOpts(
                rotate=0,
                formatter=JsCode("function (value, index) {return value.substr(0,7);}"),
            ),
        ),
        yaxis_opts=opts.AxisOpts(
            name="IC",
            is_scale=True,
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        datazoom_opts=[
            opts.DataZoomOpts(range_start=0, range_end=100),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(selected_map=LegendSelected)
    )

    return bar



def st_factor_distribution_plot(factor_distribution):

    desc = factor_distribution.copy()
    desc = desc[['count', 'min', '25%', '75%', 'max']]
    # count 转整数
    desc['count'] = desc['count'].astype(int)
    # min/25%/50%/75%/max 保留两位小数并转字符串
    for col in ['min', '25%', '75%', 'max']:
        desc[col] = desc[col].round(2).astype(str)


    # -------------------
    # 1. X轴
    x_axis = desc.index.tolist()
    # print(desc)

    # -------------------
    # 2. 柱状图 (count)
    bar = Bar()
    bar.add_xaxis(x_axis)
    bar.add_yaxis(
        "频次个数",
        desc["count"].tolist(),
        yaxis_index=0,
        label_opts=opts.LabelOpts(is_show=False),
        bar_width="50%",  # 这里控制柱子宽度，默认是 "60%" 左右
        # color="#87CEEB",
        itemstyle_opts=opts.ItemStyleOpts(opacity=0.9),
    )

    # -------------------
    # 3. 蜡烛图 (分位数)
    # 格式 [open, close, low, high] => [25%, 75%, min, max]
    kline_data = []
    for _, row in desc.iterrows():
        kline_data.append([
            row["25%"],  # open
            row["75%"],  # close
            row["min"],  # low
            row["max"],  # high
        ])

    kline = Kline()
    kline.add_xaxis(x_axis)
    kline.add_yaxis(
        "因子分位线", 
        kline_data, 
        yaxis_index=1,
        bar_width="30%",  # 这里控制柱子宽度，默认是 "60%" 左右
        # itemstyle_opts=opts.ItemStyleOpts(
        #     color="#FF98AA",       # 收盘 > 开盘，蜡烛填充色（淡蓝）
        #     color0="#FF98AA",      # 收盘 <= 开盘，蜡烛填充色（淡蓝）
        #     border_color="#FF98AA",  # 上影线/下影线颜色
        #     border_color0="#FF98AA"
        # )
        itemstyle_opts=opts.ItemStyleOpts(opacity=0.8),
    )


    # -------------------
    # 4. 叠加
    bar.overlap(kline)

    # -------------------
    # 5. 配置双轴 + 合并
    bar.extend_axis(
        yaxis=opts.AxisOpts(
            name="因子值",
            type_="value",
            position="right",
            splitline_opts=opts.SplitLineOpts(is_show=False),  # 只保留左边网格线
            # axislabel_opts=opts.LabelOpts(
            #     formatter="{value}%"  # 右轴刻度后面加 %
            # ),
        )
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="因子分组频次分布"),
        xaxis_opts=opts.AxisOpts(
            name="组别", 
            name_location="middle",
            name_gap=25,              # 距离轴线的距离，调整上下间距
            ),
        yaxis_opts=opts.AxisOpts(name="频次个数", position="left"),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",
            formatter=JsCode(
                """
                function (params) {
                    let res = '<b>' + '组别:' + params[0].axisValue + '</b><br/>';
                    for (let i = 0; i < params.length; i++) {
                        let p = params[i];
                        if (p.seriesType === 'candlestick') {
                            res += p.marker + p.seriesName + '<br/>' +
                                'min: ' + p.data[3] + '<br/>' +
                                '25%: ' + p.data[1] + '<br/>' +
                                '75%: ' + p.data[2] + '<br/>' +
                                'max: ' + p.data[4] + '<br/>';
                        } else {
                            res += p.marker + p.seriesName + ': ' + p.data + '<br/>';
                        }
                    }
                    return res;
                }
                """
            )
        ),
    )

    # -------------------
    # 6. 展示
    st_pyecharts(bar, height='400px')


'''
#------------------------------------------------------------------------
main
#------------------------------------------------------------------------
'''

# 0. main - head
#--------------------------
st.title("Single Factor Analysis — 单因子分析")
st.markdown("___", unsafe_allow_html=True)
# st.text("")  # 空行
# st.text("")  # 空行

st.sidebar.subheader("📑 页面目录")
st.sidebar.markdown(
    """
    [Factor](#factor)  
    [Factor IC](#factor-ic)  
    [Factor Grouped](#factor-grouped)  
    """
)



# 1. main - single factor
#--------------------------
# 添加加锚点 id
st.markdown('<a id="factor"></a>', unsafe_allow_html=True)
st.markdown("## 🔹Factor")
## 1.1 因子选择
col1, col2 = st.columns([2,2,1,1,1,1,1,1,1,1,1])[0:2]
with col1:  
    factor_typeI_lst = os.listdir(r'data\factors')
    factor_typeI = st.selectbox("因子大类", factor_typeI_lst, index=0)  # 默认第一个板块
    factor_typeI_path = os.path.join(r'data\factors', factor_typeI)
with col2:
    factor_name_lst = [factor_name.split('.')[0] for factor_name in os.listdir(factor_typeI_path)]
    factor_name = st.selectbox("因子", factor_name_lst, index=0)
dataloader = get_loader(
    factor_typeI, 
    factor_name, 
    ret_nd=[1,5,10,22]
)
factor_df, data = dataloader.factor_df, dataloader.data


## 1.2 因子描述
factor_desc = dataloader.factor_desc
if factor_desc:
    st.markdown(f"#### {factor_desc.get('name', factor_name)}")
    st.write("**类别**：", factor_desc.get('category', '暂无说明'))
    st.write("**说明**：", factor_desc.get('description', '暂无说明'))

    # 如果有公式就渲染 LaTeX
    formula = factor_desc.get('formula', '')
    if formula:
        st.write("**公式**：")
        st.latex(formula)  # LaTeX 渲染

    # 参考文献
    reference = factor_desc.get('reference', '')
    if reference:
        st.write("**参考**：", reference)
else:
    st.info("暂无该因子的说明。")
st.text("")  # 空行


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
st.text("")  # 空行
# st.markdown('<hr style="border:2px solid #1abc9c">', unsafe_allow_html=True)
# st.markdown('<hr style="width:50%; border:0.5px solid #808080;">', unsafe_allow_html=True)
# st.markdown('<hr style="width:50%; border:0.1px solid #1abc9c; margin-left:auto; margin-right:auto;">', unsafe_allow_html=True)

# 2. main - factor IC
#--------------------------
## IC
st.markdown('<a id="factor-ic"></a>', unsafe_allow_html=True)
st.markdown("## 🔹Factor IC")
col1 = st.columns(9)[0]
with col1:
    IC_type = st.selectbox("IC type", ['IC', 'Rank-IC'], index=0)
    st.text("")  # 空行
    st.text("")  # 空行
factor_IC = dataloader.load_factor_IC(IC_type=IC_type)
Line_IC_ret_nd = st_IC_retNd_plot(factor_IC)
st_pyecharts(Line_IC_ret_nd, height="500px", width="100%")


st.text("")  # 空行
st.text("")  # 空行
st.text("")  # 空行


    

# 3. main - factor grouped
#--------------------------
st.markdown('<a id="factor-grouped"></a>', unsafe_allow_html=True)
st.markdown("## 🔹Factor Grouped")

## 3.1 因子频次分布
col1, col2 = st.columns(9)[:2]
with col1:
    grouped_nums = st.number_input(min_value=1, max_value=100, value=10, step=1, format="%d", label="grouped nums", label_visibility='visible')
with col2:
    grouped_type = st.selectbox("grouped type", ['quantile', 'bins'], index=0)
    if grouped_type == 'quantile':
        params = {'quantile': grouped_nums, 'bins': None}
    else:
        params = {'quantile': None, 'bins': grouped_nums}
st.text("")  # 空行
st.text("")  # 空行
factor_distribution = dataloader.load_factor_grouped_ret(**params)
st_factor_distribution_plot(factor_distribution)
# st_pyecharts(bar)

## 3.2 因子
