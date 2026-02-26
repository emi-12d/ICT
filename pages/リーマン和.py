import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify, latex
from sympy.core.sympify import SympifyError


"""# リーマン和"""

"""___"""


user_formula = st.text_input("yを取り除いた数式を入力してください。　例）sin(x)")

x_sym = symbols('x')  # xを定義

if user_formula.strip():  
    try:
        expr = sympify(user_formula)  # 文字列をsympyの式に変換
        f = lambdify(x_sym, expr, 'numpy')  # numpy対応関数に変換

        latex_expr = latex(expr) #latex表示
        st.latex(f"f(x) = {latex_expr}")


    except SympifyError as e:
        st.error("数式が正しくありません。掛け算記号の入れ忘れに注意しましょう。")

    except Exception as e:
        st.write("エラー:", e)

method = st.radio("分割数を選んでください", ["指定する", "∞"], horizontal=True)

if method == "指定する":
    col_n,col_a,col_b = st.columns(3)
    n = col_n.number_input("分割数を入力してください", value=0, step=1)
    a = col_a.number_input("区域の始まり入力してください", value=0, step=1)
    b = col_b.number_input("区域の終わりを入力してください", value=0, step=1)
    c = n

else:
    col_a,col_b = st.columns(2)
    with col_a:
        a = st.number_input("区域の始まり入力してください", value=0, step=1)
    with col_b:
        b = st.number_input("区域の終わりを入力してください", value=0, step=1)
    n = abs(b-a) * 1000
    c = "∞"

if a > b:
    a, b = b, a

# グラフ選択
all_genre = ["右リーマン和", "左リーマン和", "中央リーマン和", "上リーマン和", "下リーマン和"]
genre = st.multiselect("表示させたいグラフの種類を選択してください。（複数選択可）",all_genre)

# 保存形式の選択
save_format = st.radio(
    "右上のカメラボタンで保存する形式を選択してください",
    ["png", "svg", "jpeg"],
    horizontal=True
)

def plot_riemann_sum(x_values, y_values, title, bar_color='rgba(200, 50, 50, 0.6)'):
    bar_x = x_values # 棒の中心
    bar_width = (b-a) / n # 棒の幅
    x_curve = np.linspace(a, b, 500) # 曲線用のx
    y_curve = f(x_curve) # 曲線用のy
    val = np.sum(y_values * bar_width)
    fig = go.Figure() # グラフの作成
    # 関数の曲線
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="y = f(x)"))
    fig.add_trace(go.Bar(
        x=bar_x, 
        y=y_values, 
        width=bar_width, 
        marker=dict(color=bar_color)))
    # 棒グラフ
    fig.update_layout(
        title=(f"{title} (f(x) = {user_formula})<br>値 = {val:.5f}"),
        xaxis_title="x",
        yaxis_title="f(x)",
        barmode='overlay',
        template="plotly_white"
    )
    return fig

def get_config(filename):
    return {
        'toImageButtonOptions': {
            'format': save_format, # ラジオボタンの値
            'filename': filename,  # ★ここで個別のファイル名を設定
            'height': None, 
            'width': None,
            'scale': 2
        }
    }

#区間・分割数
if n!=0 and a-b!=0 and genre:
    st.write("f(x) = " + user_formula)
    st.write("分割数： " + str(c))
    st.write("区間： " + str(a) + "から" + str(b))  

    bar_width = (b-a)/n  # 棒の幅
    x = np.linspace(a, b, n+1)  # n+1に均等に分ける

    config = {
        'toImageButtonOptions': {
            'format': save_format,
            'filename': 'RiemannSum',
            'height': None, 
            'width': None,
        }
    }
    
    # 右リーマン和
    if "右リーマン和" in genre:
        x_right = x[1:] - bar_width / 2 # 右端点 2番目以降を取り出す 棒の中心
        y_right = f(x[1:])
        fig = plot_riemann_sum(x_right, y_right, "右リーマン和")

    # 左リーマン和
    if "左リーマン和" in genre:           
        x_left = x[:-1]  + bar_width / 2 # 右端点 2番目以降を取り出す
        y_left = f(x[:-1])
        fig = plot_riemann_sum(x_left, y_left, "左リーマン和")
        st.plotly_chart(fig, use_container_width=True, config=get_config("LeftRiemannSum"))

    # 中央リーマン和
    if "中央リーマン和" in genre:
        x_mid = x[:-1] + bar_width / 2
        y_mid = f(x_mid)
        fig = plot_riemann_sum(x_mid, y_mid, "中央リーマン和")
        st.plotly_chart(fig, use_container_width=True, config=get_config("MidpointRiemannSum"))

    # 上リーマン和
    if "上リーマン和" in genre:
        x_mid = x[:-1] + bar_width / 2
        x_intervals = [(x[i], x[i+1]) for i in range(n)]  # 各区間 [x[i], x[i+1]]
        y_top = np.array([max(f(np.linspace(start, end, 10))) for start, end in x_intervals])  # 各区間での最大値
        fig = plot_riemann_sum(x_mid, y_top, "上リーマン和")
        st.plotly_chart(fig, use_container_width=True, config=get_config("UpperRiemannSum"))

    # 下リーマン和
    if "下リーマン和" in genre:
        x_mid = x[:-1] + bar_width / 2
        x_intervals = [(x[i], x[i+1]) for i in range(n)]
        y_bottom = np.array([min(f(np.linspace(start, end, 10))) for start, end in x_intervals])  # 各区間での最小値
        fig = plot_riemann_sum(x_mid, y_bottom, "下リーマン和")
        st.plotly_chart(fig, use_container_width=True, config=get_config("LowerRiemannSum"))
