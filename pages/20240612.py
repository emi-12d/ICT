import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import time


st.header(":blue[2024/6/6] :sunny:", divider = "rainbow")

"""
##### 1.st.column_config.DatetimeColumn 
年月日、時間を選択して表示することが出来る。 :st
フォーマットを変更することで何を表示するか設定出来る。:st
下記のプログラムの"YYYY年 MM月 DD日, 　h:mm a"は、 :st
"YYYY"が西暦、"MM"と"DD"が2桁表示の月日、h:mmで時間と分、aはam・pmを表している。:st
自由度が高く、曜日やACやBCの年号も表示可能である

フォーマットの参考文献 :st
https://momentjs.com/docs/#/displaying/format/
https://atmarkit.itmedia.co.jp/ait/articles/1501/29/news016_6.html


#### from datetime import datetimeが必要
適切でない日付は入力できない。

"""
with st.echo():
  data_df = pd.DataFrame(
    {
      "appo": [
        datetime(2024, 2, 12, 13, 9),
        datetime(2023, 12, 30, 1, 5),
      ]
    }
  )
  st.data_editor(
    data_df,
    column_config = {
      "appo": st.column_config.DatetimeColumn(
        "日程",
        min_value=datetime(2023, 6, 1), #最小値
        max_value=datetime(2025, 1, 1), #最大値
        format="YYYY年 MM月 DD日, 　h:mm a", #フォーマットの指定
        step=60, #60秒間隔で選択可能
      ),
    },
    hide_index=True, #インデックスの非表示
    num_rows="dynamic", #動的
  )

"""
##### 2.st.column_config.Date & Time
日付と時間だけのカラムを作成し、それぞれ編集可能。 :st
Dateの場合のステップは日数ごと。

"""
with st.echo():
  data_df2 = pd.DataFrame(
    {
      "appodate": [
        date(2024, 6, 12),
        date(2024, 3, 1),
      ],
      "appotime": [
        time(15, 45),
        time(8, 20),
      ]
    }
  )
  st.data_editor(
    data_df2,
    column_config={
      "appodate": st.column_config.DateColumn(
        "日付",
        min_value=date(2023, 4, 1), #最小値
        max_value=date(2027, 3, 31), #最大値
        format="YYYY-MM-DD",
        step=1, #1日ごとに選択可能
      ),
      "appotime": st.column_config.TimeColumn(
        "時間",
        min_value=time(8, 0), #最小値
        max_value=time(17, 30), #最大値
        format="hh:mm a",
        step=60, #60秒ごとに選択可能
      ),
    },
    hide_index=True,
  )

"""
##### 3.st.column_config.ImageColumn
自分のファイル中の画像を表示させることが出来なった。　:st
修正中

"""
