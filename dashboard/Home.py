import streamlit as st
import importlib.util
import os

# streamlit run 'D:\Coding\repo\stocks_dashborads\dashboard\Home.py'


# 全局参数加载
st.set_page_config(
    page_title="因子看板",
    layout="wide",  # ✅ 全局宽屏
    initial_sidebar_state="expanded"
)


# 动态加载和执行策略页面
def load_page(page_name):
    page_path = os.path.join(r"dashboard\.streamlit\pages", f"{page_name}.py")
    if os.path.exists(page_path):
        # 使用 importlib 动态加载
        spec = importlib.util.spec_from_file_location(page_name, page_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        st.error(f"页面 '{page_name}' 未找到！")


with st.sidebar:
    st.sidebar.title("🧭 导航栏")  # 左侧栏标题
    selected_page = st.radio(
        label="页面选择", 
        options=["主页", "Single Factor Analysis", "factors"],
        label_visibility="collapsed"  # 隐藏标签但不触发警告
    )


# 根据选择的页面输出内容
if selected_page == "主页":
    st.title("主页")
    # st.write("使用左侧导航栏切换页面。")
elif selected_page == "Single Factor Analysis":
    load_page("single_factor_analysis")
elif selected_page == "factors":
    load_page("factors")



