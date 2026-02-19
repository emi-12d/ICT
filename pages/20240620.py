import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import random

st.header(":blue[2024/6/20] :sunglasses:", divider = "rainbow")
st.title("さまざまなチャートの表示")

"""
#### 1. st.area_chart
面グラフを作成する。

"""
with st.echo():
  chart_data = pd.DataFrame(
    {
      "速度": np.random.randn(20),
      "重さ": np.random.randn(20),
      "凡例": np.random.choice(["A", "B", "C"], 20),
    }
  )
  st.area_chart(chart_data, x="速度", y="重さ", color="凡例")

"""
#### 2. st.bar_chart
棒グラフや積み上げ棒グラフを表示する。:st
系列が複数存在する場合は積み上げの棒グラフしか表示できない。
"""
with st.echo():
  chart_data = pd.DataFrame(
    {
      "月": list(range(1, 13)) * 3,
      "人数": np.random.randn(36),
      "col3": ["A"] * 12 + ["B"] * 12 + ["C"] * 12,
    }
  )
  st.bar_chart(chart_data, x="月", y="人数", color="col3")

"""
#### 3. st.line_chart
折れ線グラフを表示する。
"""
with st.echo():
  st.line_chart(
    chart_data, x="月", y="人数", color="col3"
  )

"""
#### 4. st.scatter_chart
散布図を表示する。
"""
with st.echo():
  st.scatter_chart(
    chart_data, x="月", y="人数", color="col3"
  )

"""
#### 5. st.pyplot
matplotlibのpyplot図を表示する。 :st
import matplotlib.pyplot as plt　でインポートしておく。

matplotlibの書き方で作成することが可能。
"""
st.write('ヒストグラム')
with st.echo():  
  random.seed(0)
  data = np.random.randn(10 ** 5) * 10 + 50

  plt.figure(figsize = (40, 6))
  plt.hist(data, bins = 60, range = (20, 80))
  plt.title('hist')
  plt.grid(True)
  st.pyplot(plt)

st.write('二次関数のグラフ')
with st.echo():
  def my_function(x):
    return x ** 2 + 2 * x + 1
  x = np.arange(-10, 10)
  plt.figure(figsize = (20, 6))
  plt.plot(x, my_function(x))
  plt.grid(True)
  st.pyplot(plt)

"""
#### 6. st.plotly_chart
インタラクティブな可視化を可能にする、
python用のチャート作成ライブラリである。:st
拡大・縮小、クリック、投げ縄などを利用することで部分をしぼって表示させることが可能。 :st
import plotly.figure_factory as ff　を追加
"""
st.write('ヒストグラム')
import plotly.figure_factory as ff

with st.echo():
  x1 = np.random.randn(200) - 2
  x2 = np.random.randn(200)
  x3 = np.random.randn(200) + 2

  hist_data = [x1, x2, x3]

  group_labels = ['Group 1', 'Group 2', 'Group 3']

  fig = ff.create_distplot(
          hist_data, group_labels, bin_size=[.1, .25, .5])

  st.plotly_chart(fig, use_container_width=True)



