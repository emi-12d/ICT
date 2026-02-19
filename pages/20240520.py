import streamlit as st
import time
import numpy as np
import pandas as pd
import copy

st.header(":blue[2024/5/20] :heart_eyes:", divider = "rainbow")
"""
##### 1. st.write_stream
ジェネレーター、反復可能、またはストリームのようなシーケンスをアプリにストリーミングする。 \n

for文を回す処理を実行することができる

yieldを用いることで表示させることができる

※returnでは実行されない

作成したモノ：for文を用いた九九の表
"""

y_text = """
##### yieldとは
関数を一時的に実行停止させることが出来る機能を持つ文のこと
return文はそのままの値を返すがそれではたくさんのメモリを一度に消費してしまう可能性がある。
yieldを使うことで、膨大な量の戻り値を小分けにして返すことができる。
基本的に関数の中で使われる。
"""
def yield_text():
  for word in y_text.split("\n"):
    yield word + "\n" * 2
    time.sleep(0.05)

if st.button("yieldとは？"):
  st.write_stream(yield_text)


col = []
ind = []

def multi():
  for i in range(1,10):
    for j in range(1,10):
      col.append(i * j)
    ind.append(copy.copy(col))
    col.clear()
  df = pd.DataFrame(ind)
  df.index = [i for i in range(1, 10)]
  df.columns = [i for i in range(1, 10)]
  yield df


if st.button("九九"):
  st.write_stream(multi)

"""
##### 1. st.download_button

ダウンロードボタンウィジェットを表示する
"""
text_contets = '''
col = []
ind = []
def multi():
  for i in range(1,10):
    for j in range(1,10):
      col.append(i * j)
    ind.append(copy.copy(col))
    col.clear()
  df = pd.DataFrame(ind)
  df.index = [i for i in range(1, 10)]
  df.columns = [i for i in range(1, 10)]
  yield df


if st.button("九九"):
  st.write_stream(multi)
'''
st.download_button("九九のプログラム", text_contets, file_name='Multiplication.txt')

