import streamlit as st
import importlib.util
import os

st.set_page_config(
    page_title="因子看板",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_page(page_name):
    page_path = os.path.join(r"dashboard/.streamlit/pages", f"{page_name}.py")
    if os.path.exists(page_path):
        spec = importlib.util.spec_from_file_location(page_name, page_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        st.error(f"页面 '{page_name}' 未找到！")

# 所有可选页面
pages = ["Home Page", "Single Factor Analysis", "factors"]

# 从 URL 读取当前 page 参数 (st.query_params 是一个 dict-like 对象)
default_page = st.query_params.get("page", "Home Page")

# 侧边栏导航
with st.sidebar:
    st.sidebar.title("🧭 导航栏")
    selected_page = st.radio(
        "页面选择",
        options=pages,
        index=pages.index(default_page) if default_page in pages else 0,
        label_visibility="collapsed"
    )

# 每次切换更新 URL 参数
st.query_params["page"] = selected_page

# 根据选择加载页面
if selected_page == "Home Page":
    load_page("home_page")
elif selected_page == "Single Factor Analysis":
    load_page("single_factor_analysis")
elif selected_page == "factors":
    load_page("factors")
