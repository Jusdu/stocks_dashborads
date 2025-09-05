# 股票因子看板


## 数据
> 储存在 `data` 中，可手动加入, 也可通过掘金api获取
> 数据来源于掘金，一方面是因为可以直接开通实盘，另一方面是因为熟悉 :）  

**格式要求：**

- **price_data:**
  - `pd.MultiIndex()`
  - `index`: [`date`, `symbol`]
  - `columns`: [`open`, `high`, `low`, `close`, `volume`]
  - `values`: float
- **factor_data:**
  - `pd.MultiIndex()`
  - `index`: [`date`, `symbol`]
  - `columns`: [`factor_name`]
  - `values`: float

<br>

**项目结构：**
```
├── dashboard/ # Streamlit 前端
│
├── data/ # 本地缓存数据
│ ├── raw/ # 原始数据
│ ├── processed/ # 预处理后的数据
│ └── factors/ # 因子数据
│
├── src/ # 核心代码
│ ├── data_loader/ # 数据获取（掘金接口封装）
│ ├── factor_calc/ # 因子计算模块
│ ├── factor_eval/ # 因子评价模块
│
├── config.toml # 配置文件
├── requirements.txt # Python依赖
├── README.md # 项目说明
└── run.py # 一键启动入口（抓取 + 计算 + 更新Dashboard）
```

<br>

## TODO

1. 添加 `data\macro_factors` 的显示
2. 添加 `src\factor_eval\get_eval.py` 的 因子分组截面收益的评估
3. 添加 `data\raw` 的整理
4. 添加 `data\raw` 的数据预处理
5. 添加对 `data\factors` 下的因子显示时的前端因子预处理操作
