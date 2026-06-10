import streamlit as st

st.title("自動計算アプリ")
st.write("利用したいツールを選択して、各アプリを起動してください。")

st.markdown("___")

# 別ファイルのアプリへ遷移するボタン（リンク）を配置
st.page_link("pages/リーマン和.py", label="▶ リーマン和アプリを開く")
st.page_link("pages/重回帰分析.py", label="▶ 回帰分析アプリを開く")