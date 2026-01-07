import streamlit as st

st.set_page_config(
    page_title="因子看板",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 页面定义
page_home_index = st.Page("views/home_index.py", title="指数走势", icon="📈")
page_single_factor_analysis = st.Page("views/single_factor_analysis_copy.py", title="单因子分析", icon="📊")
page_factors = st.Page("views/factors.py", title="多因子分析", icon="📊")


# 3. 导航
pg = st.navigation({
    "导航": [page_home_index, page_single_factor_analysis, page_factors]
})

# 4. 运行
pg.run()
