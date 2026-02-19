import streamlit as st

st.header(":blue[2024/4/25] :sunglasses:", divider = "rainbow")
"""
##### 1. コード表示
"""
code = '''def hello():
    print("Hello World!")'''
st.code(code, language = 'python')

"""
##### 2. セントエコー

  withブロックでアプリ上にコードを描画し、実行する
"""

with st.echo():
  st.write('Hello World')


"""
##### 3. ヘッダー
  :red[テキストの色付け]
"""

code = ''':color[テキスト]'''
st.code(code, language = 'python')
"""
  絵文字 :sunglasses:

  https://qiita.com/yamadashy/items/ae673f2bae8f1525b6af

  絵文字一覧

  ※絵文字は環境に依存するため利用するのは注意が必要
"""
code = """:sunglasses:"""
st.code(code, language = 'python')

"""
#### 4. 入力ウィジェット
  ボタン
"""
st.button('reset')