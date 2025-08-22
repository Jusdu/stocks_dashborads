'''
AStockFactorBoard/
    ├── data/                  # 本地缓存的数据（如行情、财务指标、因子计算结果）
    │   ├── raw/               # 原始数据（掘金API拉取的日行情、财报等）
    │   ├── processed/         # 预处理后的数据
    │   └── factors/           # 因子值 & 打分结果
    │
    ├── src/                   # 核心代码
    │   ├── data_loader/       # 数据获取（掘金接口封装）
    │   │   └── guguquant_api.py
    │   ├── factor_calc/       # 因子计算模块
    │   │   ├── momentum.py    # 动量因子
    │   │   ├── value.py       # 估值因子
    │   │   ├── quality.py     # 盈利质量因子
    │   │   └── volatility.py  # 波动率因子
    │   ├── factor_eval/       # 因子评价模块
    │   │   ├── ic_ir.py       # IC / IR 计算
    │   │   ├── rank_ic.py     # RankIC
    │   │   ├── turnover.py    # 因子换手率
    │   │   └── factor_summary.py
    │   ├── backtest/          # 简单因子回测（可选）
    │   │   └── long_short.py
    │   ├── utils/             # 公共函数
    │   │   ├── cache.py       # 缓存管理
    │   │   ├── date_utils.py
    │   │   └── log.py
    │   └── scheduler.py       # 定时任务调度（每日跑因子）
    │
    ├── dashboard/             # Streamlit 前端
    │   ├── app.py             # 主入口（st run app.py）
    │   ├── pages/             # 多页面结构
    │   │   ├── 因子表现.py
    │   │   ├── 因子对比.py
    │   │   ├── 因子回测.py
    │   │   └── 数据概览.py
    │
    ├── config/                # 配置文件
    │   ├── settings.yaml      # API Key、因子列表、参数配置
    │   └── logging.yaml
    │
    ├── requirements.txt       # 依赖
    ├── README.md
    └── run.py                 # 一键启动入口（抓取 + 计算 + 更新Dashboard）
'''    