import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sympy import *
import random

st.header(":blue[2024/7/31] :sunglasses:", divider = "rainbow")
"""
- h

1. h
1. r
1. 4
"""

"""
#### 1. 積分
sympyを用いた積分計算
"""
x = Symbol('x')
f = x ** 2
a = integrate(f, x)

st.latex(r'''
  \int x^{2}
  ''')
st.write(a)
"""
#### 2. ランダムに問題を作成する
"""
"""
##### レベル1
"""
st.latex(r'''
  \int ax^{b}
  ''')
"""
aとbは1から10までの整数値がランダムで代入される
"""

#ランダムで取得した値の保持
if 'a' not in st.session_state:
    st.session_state.a = random.randint(1, 10)
    st.session_state.b = random.randint(1, 10)

# aとbの値を取得する関数
def new_problem():
    st.session_state.a = random.randint(1, 10)
    st.session_state.b = random.randint(1, 10)

C = Symbol('C')
f = st.session_state.a * x ** st.session_state.b
ans = integrate(f, x) + C

# 問題の表示
st.write(Integral(f, x))

#ヒントの表示
if st.button("ヒント"):
  st.latex(r'''
  \int cf(x) dx = c \int f(x)dx
  ''')
  st.latex(r'''
  \int x^{a}dx = \frac{1}{a + 1} x^{a + 1} + C
  ''')
# 答えの表示
if st.button("答え"):
  st.write(ans)
    

# 新しい問題の作成
if st.button("新しい問題"):
    new_problem()
    st.rerun() #再実行

"""
##### レベル2

"""



