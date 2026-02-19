import streamlit as st
from pages import colc
from module import col
from PIL import Image
import pandas as pd


st.header(":blue[2024/6/19] :sunglasses:", divider = "rainbow")

"""
#### 1. 別ファイルから関数の利用
別のファイルにある関数を利用する場合はその関数があるファイルをインポートする必要がある。

※もし、うまく実行できない場合はstreamlitを実行しなおすと解決する場合がある。
"""
"""
### ディレクトリ構成
"""
img = Image.open('pages./images./del.png')
st.image(img,use_column_width=True)

code = '''from pages import colc
from module import col'''
st.code(code, language = 'python')

"""
colc.py

半径を引数として円の面積を出力する
"""
code='''def calc_area(r):
  return r ** 2 * 3.14'''
st.code(code, language = 'python')

"""
col.py

九九の表を作成する
"""
code = '''def kake():
  col = []
  ind = []
  for i in range(1,10):
    for j in range(1,10):
      col.append(i * j)
    ind.append(copy.copy(col))
    col.clear()
  df = pd.DataFrame(ind)
  df.index = [i for i in range(1, 10)]
  df.columns = [i for i in range(1, 10)]
  yield df'''
st.code(code, language = 'python')

"""
このプログラムで実行させる方法

"""
with st.echo():
  st.write(colc.calc_area(3))
  st.write_stream(col.kake)

"""
#### 2. 画像を表示させる
上記でディレクトリ構成を表示させた方法 :st
pythonの画像処理ライブラリPollowを利用 :st

まず、Pillowインポートする :st
環境によってはpipでインストールする必要がある
"""
code = '''from PIL import img'''
st.code(code, language = 'python')

"""
画像を置ているディレクトリを考えながら、画像を読み込む。 :st
st.imageを用いてstreamlitで表示させる。 :st
今回はimages内のrose.jpgを表示
"""
with st.echo():
  img = Image.open('pages./images./rose.jpg')
  st.image(img,use_column_width=True)

"""
#### 3. st.column_config.AreaChartColumn
面グラフの列を表示する. :st
面グラフとは、要素を折れ線グラフで表示し、X軸に向かった領域を色やハッチングなどで塗りつぶしたグラフのこと。 :st
推移や差などを視覚的に把握できる。

##### st.column_config.AreaChartColumnを変更することで、折れ線グラフ、棒グラフなどの列にすることも可能。
"""
with st.echo():
  df = pd.DataFrame(
    {
      "name": [
        "ファミリーマート",
        "ローソン",
        "セブンイレブン",
      ],
      "num": [
        [0, 6, 7.6, 10, 15],
        [7, 7.5, 10, 13, 13.6],
        [10, 12, 16, 20, 21],
      ],
    }
  )
  st.data_editor(
    df,
    column_config={
      "num": st.column_config.AreaChartColumn(
        "5年ごとのコンビニの店舗数の推移(千)",
        y_min = 0,
        y_max = 25,
      ),
      "name": st.column_config.Column(
        "コンビニ名"
      )
    },
    hide_index = True,
  )

"""
#### 4. st.metric
指標を表示する。 :st
delta_colorはnormalで正のとき緑、負のとき赤 :st
inverseはその逆の色で表示される。 :st
offは灰色で表示される。

単位を付けても読み取りに問題なし。
"""
with st.echo():
  st.metric(label=":green[部屋の温度]", value="26℃", delta="4℃",
            delta_color="inverse")
  st.metric(label=":green[部屋の温度]", value="26℃", delta="-4℃",
            delta_color="inverse")