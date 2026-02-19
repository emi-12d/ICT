import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy import random
import pandas as pd

st.header(":blue[2024/7/4] :sunglasses:", divider = "rainbow")

"""
#### 1. グラフの合成する
2つのグラフを重ねて表示させる。

"""
st.write('ヒストグラム')
with st.echo():  
  random.seed(0)
  data = np.random.randn(10 ** 5) * 10 + 50

  plt.figure(figsize = (20, 6))
  plt.hist(data, bins = 30, range = (20, 80))
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

with st.echo():
  # グラフの作成
  plt.figure(figsize=(20, 6))

  # ヒストグラム
  plt.hist(data, bins=30, range=(20, 80), label='Histogram')

  # 2次関数のグラフ
  x_dense = np.linspace(20, 80, 1000)  # データ範囲をヒストグラムと一致させる
  plt.plot(x_dense, my_function(x_dense), color='red', label='Quadratic Function')

  # グラフの詳細設定
  plt.title('Histogram and Quadratic Function')
  plt.grid(True)
  plt.legend()
  st.pyplot(plt)

code = '''np.linspace()'''
st.code(code, language = 'python')

'''
np.lispaceは要素数を指定する関数 \n
np.lispace(start, stop, num) \n
startに最初の値 \n
stopに最後の値 \n
numに要素数を指定する。
'''


