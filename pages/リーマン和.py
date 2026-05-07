import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, sympify, lambdify, latex, integrate
from sympy.core.sympify import SympifyError


"""# リーマン和"""

"""___"""


user_formula = st.text_input("yを取り除いた数式を入力してください。　例）sin(x), pi * x")

x_sym = symbols('x')  # xを定義

if user_formula.strip():  
    try:
        expr = sympify(user_formula)    # 文字列をsympyの式に変換
        raw_f = lambdify(x_sym, expr, 'numpy')  # numpy対応関数に変換

        # 定数（xを含まない式）でもエラーが出ないようにする
        def f(x_array):
            y_array = raw_f(x_array)
            # もし結果がただの数字（スカラー）だったら、x_arrayと同じ長さにコピーして引き伸ばす
            if np.isscalar(y_array):
                return np.full_like(x_array, y_array, dtype=float)
            return y_array
        
        latex_expr = latex(expr) #latex表示
        st.latex(f"f(x) = {latex_expr}")


    except SympifyError as e:
        st.error("数式が正しくありません。掛け算記号の入れ忘れに注意しましょう。")

    except Exception as e:
        st.write("エラー:", e)

method = st.radio("分割数を選んでください", ["指定する", "∞"], horizontal=True)

if method == "指定する":
    col_n,col_a,col_b = st.columns(3)
    n_val = col_n.number_input("分割数を入力してください", value=0, step=1)
    a = col_a.number_input("区域の始まり入力してください", value=0, step=1)
    b = col_b.number_input("区域の終わりを入力してください", value=0, step=1)
    c = n_val

else:
    col_a,col_b = st.columns(2)
    with col_a:
        a = st.number_input("区域の始まり入力してください", value=0, step=1)
    with col_b:
        b = st.number_input("区域の終わりを入力してください", value=0, step=1)

if a > b:
    a, b = b, a

# グラフ選択
if method == '指定する':
    all_genre = ["右リーマン和", "左リーマン和", "中央リーマン和", "上リーマン和", "下リーマン和"]
    genre = st.multiselect("表示させたいグラフの種類を選択してください。（複数選択可）",all_genre)

# 保存形式の選択
save_format = st.radio(
    "右上のカメラボタンで保存する形式を選択してください",
    ["png", "svg", "jpeg"],
    horizontal=True
)
# アニメーション付きグラフの生成 
def animation_riemann(genre_type, start_n, end_n=1000):
    # 分割数のリスト （最初の分割数から1000までの間をnumだけ分割して格納）
    steps_n = np.unique(np.geomspace(start_n, end_n, num=50).astype(int))
    
    x_curve = np.linspace(a, b, 500) # 曲線用のx
    y_curve = f(x_curve) # 曲線用のy

    exact_val = integrate(expr, (x_sym, a, b)) # aからbまで定積分
    # グラフの塗りつぶす閾値の設定 0.05か面積の1%
    threshold = max(0.05,abs(exact_val) * 0.01)

    frames = []
    slider_steps = []

    for i, step_n in enumerate(steps_n):
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
            x_bar = x_split[:-1] + bar_width / 2
            samp = 5 if step_n > 100 else 20
            y_bar = np.array([np.min(f(np.linspace(s, e, samp))) for s, e in zip(x_split[:-1], x_split[1:])])

        val = np.sum(y_bar * bar_width)
        judge = abs(val - exact_val)
        frame_name = f"{genre_type}_{step_n}"

        is_last_step = (i == len(steps_n) - 1)

        # 分割されたグラフ
        if (judge > threshold or step_n < 100) and not is_last_step:
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=[a], y=[0], mode='none', fill='none', showlegend=False), # 塗りつぶした用ダミー
                    go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='blue'), name="f(x)"),
                    go.Bar(x=x_bar, y=y_bar, width=bar_width, marker=dict(color='rgba(200, 50, 50, 0.6)'), name="リーマン和")
                ],
                name=frame_name,
                layout=go.Layout(title=f"{genre_type} (f(x) = {user_formula})<br>値 = {val:.5f}")           
            ))
        # 塗りつぶされたグラフ
        else:
            frames.append(go.Frame(
                data=[
                    go.Scatter(x=x_curve, y=y_curve, fill='tozeroy', mode='none', fillcolor='rgba(200, 50, 50, 0.6)', showlegend=False),
                    go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='blue'), name="f(x)"),
                    go.Bar(x=[a], y=[0], width=0, marker=dict(color='rgba(200, 50, 50, 0.6)'), name="リーマン和") # 棒グラフダミー
                ],
                name=frame_name,
                layout=go.Layout(title=f"{genre_type} (f(x) = {user_formula})<br>値 = {exact_val:.5f}")           
            ))
            slider_steps.append({
                "method": "animate",
                "args": [[frame_name], {"mode": "immediate", "frame": {"duration": 100, "redraw": True}, "transition": {"duration": 0}}],
                "label": "∞"
            })
            break
        slider_steps.append({
            "method": "animate",
            "args": [[frame_name], {"mode": "immediate", "frame": {"duration": 100, "redraw": True}, "transition": {"duration": 0}}],
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
                    dict(label="▶", method="animate", args=[None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True, "transition": {"duration": 0}}]),
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

# 静止グラフの生成
def plot_riemann_sum():
    x_curve = np.linspace(a, b, 500) # 曲線用のx
    y_curve = f(x_curve) # 曲線用のy

    exact_val = integrate(expr, (x_sym, a, b)) # aからbまで積分
    val = float(exact_val.evalf()) # 小数に変換

    fig = go.Figure() # グラフの作成
    # 塗りつぶし
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, fill='tozeroy', mode='none', fillcolor='rgba(200, 50, 50, 0.6)', name="リーマン和"))
    # 青い曲線
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='blue'), name="y = f(x)"))
    fig.update_layout(
        title=(f"(f(x) = {user_formula})<br>値 ≈ {val:.5f}<br>区間：{str(a)}から{str(b)} "),
        xaxis_title="x", yaxis_title="f(x)", template="plotly_white", height=600
    )
    return fig

def get_config(g):
    if g == "右リーマン和":
        filename = "RightRiemannSum"
    elif g == "左リーマン和":
        filename = "LeftRiemannSum"
    elif g == "中央リーマン和":
        filename = "MidpointRiemannSum"
    elif g == "上リーマン和":
        filename = "UpperRiemannSum"
    else:
        filename = "LowerRiemannSum"
    return {
        'toImageButtonOptions': {
            'format': save_format, # ラジオボタンの値
            'filename': filename,  # ここで個別のファイル名を設定
            'height': None, 
            'width': None,
            'scale': 2
        }
    }

# ∞の場合のグラフの生成
if method == '∞' and a-b != 0:
    fig = plot_riemann_sum()
    st.plotly_chart(fig, use_container_width=True)

#区間・分割数
if method == "指定する":
    if n_val!=0 and a-b!=0 and genre:
        st.write("f(x) = " + user_formula)
        st.write("分割数： " + str(c))
        st.write("区間： " + str(a) + "から" + str(b))  

        config = {
            'toImageButtonOptions': {
                'format': save_format,
                'filename': 'RiemannSum',
                'height': None, 
                'width': None,
                'scale': 2
            }
        }

        for g in genre:
            fig = animation_riemann(g, n_val)
            st.plotly_chart(fig, use_container_width=True, config=get_config(g), key=f"anim_{g}")


