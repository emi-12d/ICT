import streamlit as st
import pandas as pd

st.header(":blue[2024/5/8] :sunglasses:", divider = "rainbow")
"""
##### 1. st.write_stream
  ジェネレーター、反復可能、またはストリームのようなシーケンスをアプリにストリーミングする。 \n
  for文を回す処理を実行することが出来る。

  修正中
"""
data = []
def two():
  for i in range(1, 11):
    i *= 2
    data.append(i)
    print(i)
  pd.DataFrame(data)
  
  
if st.button("2の段"):
  st.write_stream()


"""
#### 2. セントラテックス
 LaTex形式の数式を表示する。

 LaTexでサポータとされている関数一覧
 https://katex.org/docs/supported.html


 3倍角の公式
"""

with st.echo():
  st.latex(r'''
           sin3α = 3sinα - 4sin^3α
           ''')
"""
 Σ
"""
with st.echo():
  st.latex(r'''
           \sum_{k=1}^{n} k^3 = 1^3 + 2^3 + 3^3 + \cdots + n^3
           ''')
"""
 連立方程式
"""
with st.echo():
  st.latex(r'''
            \begin{cases}
              4x + 3y = 5 \\
              9x + 7y = 30
            \end{cases} \\
           ''')
