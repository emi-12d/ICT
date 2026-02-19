import streamlit as st
import numpy as np
import pandas as pd

st.header(":blue[2024/5/23] :weary:", divider = "rainbow")
"""
##### 1. st.text
st.textとst.writeはほとんど同じで文字列を出力することが出来る。

しかし、st.writeはMarkdownやPandasのデータフレームなどを自動で解釈し、変換して表示する。
"""

with st.echo():
  data1 = [1, 2, 3, 4]
  data2 = [2, 4, 6, 8]
  df = pd.DataFrame([data1, data2])
  st.write(df)
  st.text(df)
"""
#### 2. st.data_editor
データエディターウィジェットを表示する。

データエディターウィジェットを使用すると、テーブルのようなUIでデータフレームやその他の多くのデータ構造を編集できる。

下記のプログラムだと名前と年齢を書き換えることができ、参加のチャックを変更することができる。

指定されていないインデックスは変更されない。
"""
with st.echo():
  df = pd.DataFrame(
    [
      {"名前": "藤山恵美", "年齢": 20, "参加" : True},
      {"名前": "ふじやまえみ", "年齢": 9, "参加" : False},
      {"名前": "Emi Fujiyama", "年齢": 45, "参加" : False},
    ]
  )
  df.index = df.index + 1
  edited_df = st.data_editor(df)

"""
num_rowsをdynamicに変更することで、データの追加と削除を行うことができるようになる。

num_rowsでは動的(dynamic)か静的(fixed)かを設定することができる。
##### 固定の場合（上記の例）
ユーザーは行を追加したり、削除したりすることができない。
##### 動的の場合（下記の例）
ユーザーはデータエディターで行を追加したり、削除したりすることが可能になる。  \n
しかし、列の並べ替えは無効である。
"""

df = pd.DataFrame(
  [
    {"名前": "藤山恵美", "年齢": 20, "参加" : True},
    {"名前": "ふじやまえみ", "年齢": 9, "参加" : False},
    {"名前": "Emi Fujiyama", "年齢": 45, "参加" : False},
  ]
)

df.index = df.index + 1

with st.echo():
  edited_df = st.data_editor(df, num_rows="dynamic")

"""
下記のプログラムを実行することで、成績の値が一番高い人の名前が出力される。

このプログラムで実行することで、編集されたり、追加されたりしてもその都度更新される。

locは、Pandasのデータフレームのメソッドの1つであり、ラベルを使用して行や列を選択するために利用される。

"""

df1 = pd.DataFrame(
  [
    {"名前": "藤山恵美", "成績": 40, "参加" : True},
    {"名前": "ふじやまえみ", "成績": 30, "参加" : False},
    {"名前": "Emi Fujiyama", "成績": 90, "参加" : False},
  ]
)
edited_df1 = st.data_editor(df1)
edited_df1 = st.data_editor(df1, num_rows="dynamic")

with st.echo():
  highscore = edited_df1.loc[edited_df1["成績"].idxmax()]["名前"]
  st.markdown(f"一番成績が良かった生徒は **{highscore}** です")

