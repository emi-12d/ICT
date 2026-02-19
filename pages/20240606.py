import streamlit as st
import numpy as np
import pandas as pd

st.header(":blue[2024/6/6] :yum:", divider = "rainbow")

"""
##### 1. Colum configuration
列のカスタマイズを行うことができる。

"""
"""
##### 1-1 st.column_config.Column
st.dataFrameやst.data_editorをカスタマイズする。

パラメータとして設定することで適用可能。

columu_config={"列名": st.column_config.Column( :st
"ラベル名", :st
help="str", :st
width="str", :st
disabled=bool, :st
required=bool, :st
)
}

指定した列のカスタマイズをすることが可能。:st
helpはポインターを列名に当てると表示される :st
widthは幅の設定でsmall か medium か large :st
disabledはTrueにすると値の変更不可 :st
requiredはTrueにすると値を入れることを要求される :st
"""
with st.echo():
  df = pd.DataFrame(
  {
    "name": ["数理工センター", "教務課", "学食"],
    "where":["23号館4,5階", "1号館2階", "21号館1階"],
  }
  )
  st.data_editor(
    df, 
    column_config={
      "name": st.column_config.Column(
        "施設名",                      #ラベル名
        help="金沢工業大学の施設一覧",  #説明
        width="medium",                #幅
        required=True,                 #絶対入力
      ),
      "where": st.column_config.Column(
        "場所",
        help="施設の場所",
        width="large",
        disabled=True,                 #入力・変更不可
      )
    },
    hide_index=True, #インデックスの非表示
    num_rows="dynamic", #動的

  )

"""
##### 1-2 st.column_config.TextColumn
テキスト入力ウィジェットの編集が可能

1-1と同じようにパラメータを指定する。

defaultでテキストを追加した時の初期値を設定 :st
max_charで最大文字数を指定 :st
validateで入力できる文字を制限する

"""
with st.echo():
  df = pd.DataFrame(
    {
      "t": ["text", "take", "toll"],
    }
  )
  st.data_editor(
    df,
    column_config={
      "t": st.column_config.TextColumn(
        "tがつく単語",
        width="large",
        help="tから始まる単語で10文字以内",
        default="t",                        #初期値
        max_chars=10,                       #最大入力文字
        validate="^t[a-z_]+$",              #最初にtが付いて全て英字
      )
    },
    hide_index=True,
    num_rows="dynamic",
  )

"""
###### 1-3 st.column_config.NumberColumn
テキスト入力ウィジェットの数値の編集

stepで数値の精度を指定する。1は整数 :st
formatで入力できるフォーマットの指定（%d,%e,%fなど）

"""
with st.echo():
  df = pd.DataFrame(
    {
      "気温": [10, -35, 12, 24],
    }
  )
  st.data_editor(
    df,
    column_config={
      "気温" : st.column_config.NumberColumn(
        min_value=-50,          #最小値-50
        max_value=40,           #最大値40
        step=1,                 #整数値
        format="%d℃",          #入力フォーマット数字＋℃
      )
    },
    hide_index=True,
    num_rows="dynamic",
  )

"""
##### 1-4 st.column_config.CheckboxColumn
チェックボックス列の編集

初期値の編集が出来る。
"""
with st.echo():
  df = pd.DataFrame(
    {
      "料理":["オムライス", "メロン", "ゴーヤ"],
      "好きな食べ物は？": [True, True, False],
    }
  )
  st.data_editor(
    df,
    column_config={
      "好きな食べ物は？":st.column_config.CheckboxColumn(
        help="好きな食べ物にチェックを入れてね",
        default = False,    #初期値False
      )
    },
    disabled=["料理"],      #料理列の変更不可
    hide_index=True,
  )

"""
##### 1-5 st.column_config.SelectboxColumn
セレクトボックスの編集

optionsに格納した配列を選択することが出来る。
"""
with st.echo():
  df = pd.DataFrame(
    {
      "やることリスト" : [
        "🏊‍♂‍ 水泳",
      ],
    }
  )
  st.data_editor(
    df,
    column_config={
      "やることリスト" : st.column_config.SelectboxColumn(
        help = "今日やることを選んでください",
        width = "medium",
        options = [
        "🏊‍♂‍ 水泳",
        "🚽 トイレ掃除",
        "🧺 買物",
        "📖 勉強",
        ],
        required=True,
      )
    },
    num_rows="dynamic",
  )