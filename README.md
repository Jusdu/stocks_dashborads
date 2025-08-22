# 股票因子看板


## 数据
> 储存在 `data` 中，可手动加入, 也可通过掘金api获取
> 数据来源于掘金，一方面是因为可以直接开通实盘，另一方面是因为熟悉 :）  

**格式要求：**
- `pd.MultiIndex()`
- `index`: [`date`, `symbol`]
- `columns`: [`open`, `high`, `low`, `close`]




## TODO

1. 项目结构
    ```
    ├── data/ # 本地缓存数据
    │ ├── raw/ # 原始数据（掘金API拉取）
    │ ├── processed/ # 预处理后的数据
    │ └── factors/ # 因子值 & 评价结果
    │
    ├── src/ # 核心代码
    │ ├── data_loader/ # 数据获取（掘金接口封装）
    │ │ └── guguquant_api.py
    │ ├── factor_calc/ # 因子计算模块
    │ │ ├── momentum.py # 动量因子
    │ │ ├── value.py # 估值因子
    │ │ ├── quality.py # 盈利质量因子
    │ │ └── volatility.py # 波动率因子
    │ ├── factor_eval/ # 因子评价模块
    │ │ ├── ic_ir.py # IC / IR 计算
    │ │ ├── rank_ic.py # RankIC
    │ │ ├── turnover.py # 因子换手率
    │ │ └── factor_summary.py
    │ ├── backtest/ # 简单因子回测（可选）
    │ │ └── long_short.py
    │ ├── utils/ # 工具函数
    │ │ ├── cache.py # 缓存管理
    │ │ ├── date_utils.py
    │ │ └── log.py
    │ └── scheduler.py # 定时任务调度
    │
    ├── dashboard/ # Streamlit 前端
    │ ├── app.py # 主入口（streamlit run app.py）
    │ ├── pages/ # 多页面结构
    │ │ ├── 因子表现.py
    │ │ ├── 因子对比.py
    │ │ ├── 因子回测.py
    │ │ └── 数据概览.py
    │
    ├── config/ # 配置文件
    │ ├── settings.yaml # API Key、因子列表、参数配置
    │ └── logging.yaml
    │
    ├── requirements.txt # Python依赖
    ├── README.md # 项目说明
    └── run.py # 一键启动入口（抓取 + 计算 + 更新Dashboard） -->

    ```