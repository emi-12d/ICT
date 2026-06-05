import streamlit as st

st.set_page_config(page_title="ICT教材バンク")

# サイドバーに表示する項目
home = st.Page("exp/home.py", title="ホーム", default=True)
calc_hub = st.Page("exp/test.py", title="自動計算アプリ")
image_app = st.Page("exp/test1.py", title="画像アプリ")

# 自動計算アプリの項目
riemann = st.Page("pages/リーマン和.py", title="リーマン和")
regression = st.Page("pages/重回帰分析.py", title="回帰分析")

# サイドバーに表示させたくない項目
pg = st.navigation(
    [home, calc_hub, image_app, riemann, regression],
    position="hidden"
)

# サイドバーに表示したい項目
with st.sidebar:
    st.write("### メニュー")
    st.page_link(home)
    st.page_link(calc_hub)
    st.page_link(image_app)

pg.run()