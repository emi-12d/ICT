import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify, latex
from sympy.core.sympify import SympifyError

# --- ヘッダー ---
st.title("リーマン和")
st.markdown("___")

# --- 数式入力 ---
user_formula = st.text_input("yを取り除いた数式を入力してください（例：sin(x)）")
x_sym = symbols('x')

# 数式が有効かチェック
f = None
if user_formula.strip():
    try:
        expr = sympify(user_formula)
        f = lambdify(x_sym, expr, 'numpy')
        st.latex(f"f(x) = {latex(expr)}")
    except SympifyError:
        st.error("数式が正しくありません。掛け算記号の入れ忘れに注意しましょう。")
    except Exception as e:
        st.error(f"エラー: {e}")

# --- パラメータ入力 ---
method = st.radio("分割数を選んでください", ["指定する", "∞"], horizontal=True)

a = b = n = None  # 初期化
display_n = ""

if method == "指定する":
    col_n, col_a, col_b = st.columns(3)
    n = col_n.number_input("分割数", value=10, min_value=1, step=1)
    a = col_a.number_input("区間の始まり", value=0.0)
    b = col_b.number_input("区間の終わり", value=1.0)
    display_n = n
else:
    col_a, col_b = st.columns(2)
    a = col_a.number_input("区間の始まり", value=0.0)
    b = col_b.number_input("区間の終わり", value=1.0)
    if a != b:
        n = int(abs(b - a) * 1000)
        display_n = "∞"

# 区間の並び替え
if a is not None and b is not None and a > b:
    a, b = b, a


# --- 共通関数 ---
def plot_riemann_sum(x_values, y_values, title, bar_color='rgba(200, 50, 50, 0.6)'):
    bar_x = x_values
    bar_width = (b - a) / n
    x_curve = np.linspace(a, b, 500)
    y_curve = f(x_curve)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', name="y = f(x)"))
    fig.add_trace(go.Bar(x=bar_x, y=y_values, width=bar_width, marker=dict(color=bar_color)))
    fig.update_layout(
        title=title,
        xaxis_title="x",
        yaxis_title="f(x)",
        barmode='overlay',
        template="plotly_white"
    )
    return fig, np.sum(y_values * bar_width)

# --- 結果表示 ---
if f and n > 0 and a != b:
    if st.button("結果の表示"):
        st.markdown(f"**f(x)** = `{user_formula}`")
        st.markdown(f"**分割数**: {display_n}")
        st.markdown(f"**区間**: {a} 〜 {b}")

        x = np.linspace(a, b, n+1)
        width = (b - a) / n

        # 右リーマン和
        x_right = x[1:] - width / 2
        y_right = f(x[1:])
        fig, val = plot_riemann_sum(x_right, y_right, "右リーマン和")
        st.plotly_chart(fig)
        st.write(f"右リーマン和: {val}")

        # 左リーマン和
        x_left = x[:-1] + width / 2
        y_left = f(x[:-1])
        fig, val = plot_riemann_sum(x_left, y_left, "左リーマン和")
        st.plotly_chart(fig)
        st.write(f"左リーマン和: {val}")

        # 中央リーマン和
        x_mid = (x[:-1] + x[1:]) / 2
        y_mid = f(x_mid)
        fig, val = plot_riemann_sum(x_mid, y_mid, "中央リーマン和")
        st.plotly_chart(fig)
        st.write(f"中央リーマン和: {val}")

        # 上リーマン和
        intervals = [(x[i], x[i+1]) for i in range(n)]
        y_top = np.array([max(f(np.linspace(start, end, 10))) for start, end in intervals])
        fig, val = plot_riemann_sum(x_mid, y_top, "上リーマン和")
        st.plotly_chart(fig)
        st.write(f"上リーマン和: {val}")

        # 下リーマン和
        y_bottom = np.array([min(f(np.linspace(start, end, 10))) for start, end in intervals])
        fig, val = plot_riemann_sum(x_mid, y_bottom, "下リーマン和")
        st.plotly_chart(fig)
        st.write(f"下リーマン和: {val}")


