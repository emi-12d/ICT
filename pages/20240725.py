import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.header(":blue[2024/7/25] :sunglasses:", divider = "rainbow")

"""
#### 1. 棒グラフと2次関数を重ねたグラフ
それぞれプロットし、その後pyplotでグラフを表示させる。

"""
data = np.random.randn(10 ** 5) * 10 + 50
def my_function(x):
 return x ** 2 + 2 * x + 1

with st.echo():
  left = np.array([1, 2, 3, 4, 5])
  height = np.array([10, 20, 30, 40, 50])
  x_dense = np.linspace(1, 5, 5)  # データ範囲をヒストグラムと一致させる
  plt.plot(x_dense, my_function(x_dense), color='red', label='Quadratic Function')
  plt.bar(left, height)
  st.pyplot(plt)

"""
#### 2. plotlyを利用した棒グラフ
さまざまな棒グラフを表示する

参考資料 \n
https://sakizo-blog.com/800/

##### fig と plt
plt：matplotlib.pyplotモジュール
fig：グラフ全体を管理するFigureオブジェクト
"""
st.write('dfデータの中身')
with st.echo():
  df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
    "Number Eaten": [2, 1, 3, 1, 3, 2],
  })

st.write('plotlyを用いた単純な棒グラフ')
with st.echo():
  fig = px.bar(df, x="Fruit", y="Number Eaten")
st.plotly_chart(fig, use_container_width=True)

st.write('Contestantの違いによって色を変えて2層の棒グラフを作成')
with st.echo():
  fig = px.bar(df, x="Fruit", y="Number Eaten", color='Contestant')
st.plotly_chart(fig, use_container_width=True)

st.write('barmodeを指定して2つのグラフを作成')
"""
barmodeを変更することでグラフの表示形式を変更することが可能 \n
:red[barmode='group'] \n
　棒グラフを横に並べる \n
:red[barmode='relative] \n
　棒グラフを積み上げにする（通常） \n
:red[barmode='overlay'] \n
　棒グラフが重なり合う \n

"""
with st.echo():
  fig = px.bar(df, x="Fruit", y="Number Eaten", color='Contestant', barmode='group')
st.plotly_chart(fig, use_container_width=True)

"""
#### plotly.graph_objects モジュールを利用した棒グラフ
"""
with st.echo():
  # 描画領域の作成
  fig = go.Figure()

  df1 = df[df['Contestant']=='Alex']
  df2 = df[df['Contestant']=='Jordan']

  # traceの登録
  fig.add_trace(go.Bar(x=df1["Fruit"], y=df1["Number Eaten"], name='Alex'))
  fig.add_trace(go.Bar(x=df2["Fruit"], y=df2["Number Eaten"], name='Jordan'))

  # グラフの調整
  fig.update_layout(legend_title_text = "Contestant")
  fig.update_xaxes(title_text="Fruit")
  fig.update_yaxes(title_text="Number Eaten")
st.plotly_chart(fig, use_container_width=True)




