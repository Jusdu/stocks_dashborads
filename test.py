import pandas as pd
import streamlit as st
from pyecharts.charts import Bar, Kline, Line
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts


def st_describe_chart(df: pd.DataFrame, height: int = 600):
    """
    展示 df.describe() 的可视化：
    - count: 柱状图 (左轴)
    - 分位数(min, 25%, 75%, max): 蜡烛图 (右轴)
    - mean: 红色折线 (右轴)
    - std: 阴影区间 mean ± std (右轴)
    """
    desc = df.describe().T

    # -------------------
    # 1. X轴
    x_axis = desc.index.tolist()

    # -------------------
    # 2. 柱状图 (count)
    bar = Bar()
    bar.add_xaxis(x_axis)
    bar.add_yaxis(
        "count",
        desc["count"].tolist(),
        yaxis_index=0,
        label_opts=opts.LabelOpts(is_show=False),
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
    kline.add_yaxis("分位数", kline_data, yaxis_index=1)


    # -------------------
    # 6. 配置双轴 + 合并
    bar.extend_axis(
        yaxis=opts.AxisOpts(
            name="分位数/均值/标准差",
            type_="value",
            position="right",
        )
    )
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="df.describe() 可视化"),
        yaxis_opts=opts.AxisOpts(name="count", position="left"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        datazoom_opts=[opts.DataZoomOpts()],
    )

    # -------------------
    # 7. 叠加
    bar.overlap(kline)

    # -------------------
    # 8. 展示
    st_pyecharts(bar, height=height)


# -------------------
# 📊 示例
if __name__ == "__main__":
    df = pd.DataFrame({
        "A": range(1, 11),
        "B": [x**2 for x in range(1, 11)],
        "C": [3, 5, 2, 6, 7, 8, 2, 1, 9, 5]
    })

    st_describe_chart(df)
