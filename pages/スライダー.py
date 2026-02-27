import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify, latex
from sympy.core.sympify import SympifyError
import io
import plotly.express as px

# ★修正1: value="sin(x)" を追加して初期値を設定
user_formula = st.text_input("yを取り除いた数式を入力してください。　例）sin(x)", value="sin(x)")

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
    # ★修正2: value=5 に変更
    n_val = col_n.number_input("分割数を入力してください", value=5, step=1)
    # ★修正3: 区間の初期値を 0 と 10 に設定
    a = col_a.number_input("区域の始まり入力してください", value=0, step=1)
    b = col_b.number_input("区域の終わりを入力してください", value=10, step=1)
    c = n_val

else:
    col_a,col_b = st.columns(2)
    with col_a:
        a = st.number_input("区域の始まり入力してください", value=0, step=1)
    with col_b:
        b = st.number_input("区域の終わりを入力してください", value=10, step=1)
    n_val = abs(b-a) * 1000
    c = "∞"

if a > b:
    a, b = b, a

# グラフ選択
all_genre = ["右リーマン和", "左リーマン和", "中央リーマン和", "上リーマン和", "下リーマン和"]
# ★修正4: default=["上リーマン和"] を追加
genre = st.multiselect("表示させたいグラフの種類を選択してください。（複数選択可）", all_genre, default=["上リーマン和"])

def animation_riemann(genre_type, start_n, end_n=1000):
    steps_n = np.unique(np.geomspace(start_n, end_n, num=15).astype(int))
    x_curve = np.linspace(a, b, 500) # 曲線用のx
    y_curve = f(x_curve) # 曲線用のy

    frames = []
    slider_steps = []

    for step_n in steps_n:
        bar_width = (b-a) / step_n # 棒の幅
        x_split = np.linspace(a, b, step_n + 1)  # step_n+1に均等に分ける

        if "右リーマン和" in genre_type:
            x_bar = x_split[1:] - bar_width / 2 # 右端点 2番目以降を取り出す 棒の中心
            y_bar = f(x_split[1:])
        elif "左リーマン和" in genre_type:           
            x_bar = x_split[:-1]  + bar_width / 2 # 右端点 2番目以降を取り出す
            y_bar = f(x_split[:-1])
        elif "中央リーマン和" in genre_type:
            x_bar = x_split[:-1] + bar_width / 2
            y_bar = f(x_bar)
        elif "上リーマン和" in genre_type:
            x_bar = x_split[:-1] + bar_width / 2
            samp = 5 if step_n > 100 else 20 # 100以上なら分割数は5
            y_bar = np.array([np.max(f(np.linspace(s, e, samp))) for s, e in zip(x_split[:-1], x_split[1:])])
        elif "下リーマン和" in genre_type:
            x_bar = x[:-1] + bar_width / 2
            samp = 5 if step_n > 100 else 20
            y_bar = np.array([np.min(f(np.linspace(s, e, samp))) for s, e in zip(x_split[:-1], x_split[1:])])

        val = np.sum(y_bar * bar_width)

        frame_name = f"{genre_type}_{step_n}"

        frames.append(go.Frame(
            data=[
                go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='blue'), name="f(x)"),
                go.Bar(x=x_bar, y=y_bar, width=bar_width, marker=dict(color='rgba(200, 50, 50, 0.6)'), name="リーマン和")
            ],
            name=frame_name,
            layout=go.Layout(title=f"{genre_type} (f(x) = {user_formula})<br>値 = {val:.5f}")           
        ))
        
        slider_steps.append({
            "method": "animate",
            "args": [[frame_name], {"mode": "immediate", "frame": {"duration": 300, "redraw": True}, "transition": {"duration": 0}}],
            "label": str(step_n)
        })

    initial_frame = frames[0]  # 一つ目のフレームを格納
    fig = go.Figure(
        data=initial_frame.data,  # 初期状態の設定
        layout=go.Layout(
            title=initial_frame.layout.title,
            template="plotly_white", barmode="overlay", height=600,
            # 再生と一時停止ボタン
            updatemenus=[dict(  # グラフ上にボタンの配置
                type="buttons", showactive=False, y=-0.15, x=0, xanchor="left", yanchor="top", direction="right",
                buttons=[
                    dict(label="▶", method="animate", args=[None, {"frame": {"duration": 300, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="■", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
                ]
            )],
            sliders=[dict(
                active=0, yanchor="top", xanchor="left", transition=dict(duration=0), pad=dict(b=10, t=0, l=130), len=0.9, x=0, y=-0.15, steps=slider_steps,
                currentvalue=dict(font=dict(size=16), prefix="分割数 n = ", visible=True, xanchor="right")
            )]
        ), frames=frames
    )
    return fig




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

#区間・分割数
if n_val != 0 and a-b != 0 and genre:
    st.write("f(x) = " + user_formula)
    st.write("分割数： " + str(c))
    st.write("区間： " + str(a) + "から" + str(b))  

    for g in genre:
        if method == "指定する":
            fig = animation_riemann(g, n_val)
            st.plotly_chart(fig, use_container_width=True, key=f"anim_{g}")

