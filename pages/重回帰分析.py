import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import math
import statsmodels.api as sm
from chardet import detect



"""# 重回帰分析＆単回帰分析"""
tub_dict = {"デモデータによる分析体験":0,"ユーザーデータによる分析":1}
selected_cbox = st.radio(label="選択", options = tub_dict.keys(),horizontal=True)
"""___"""


###  デモデータによる分析体験
tub_counta = 0
tub_title = list(tub_dict.keys())[tub_counta]
if tub_dict[selected_cbox] == 0 :
    f"""### {tub_title }"""
    """
    ### 1. 分析データの選択
    """
    select_data_dict = {"デモデータ１：正規分布に従うデータ":0}
    
    # 分析データの選択
    select_str = st.selectbox("分析に使用するデータを選択してください．",select_data_dict.keys(),key="mselect 01")
    
    # データの読み込み
    if select_data_dict[select_str] == 0:
        read_data_df = pd.read_csv("pages\sample_datas\SLRA.csv",encoding='utf-8')

    else :
        st.stop()

    """___"""
    # 目的変数の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("目的変数の選択",keys_list)
    
    disp_col = st.columns([1,4])
    with disp_col[0]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        elif len(index_str) > 1:
            """"""
            st.error("2つ以上選択されています．")
            st.stop()
        else :
            """"""
            st.success(f'準備完了', icon="✅")
            purpose_data_df = read_data_df[index_str]
            data_len = purpose_data_df.shape[0]
    with disp_col[1]:
        if st.checkbox("データの確認",key="cbox 01"):
            df = pd.DataFrame(purpose_data_df)
            df.index = df.index + 1
            st.dataframe(df)


    # 説明変数の選択
    keys_list = list(read_data_df.keys())

    keys_list.remove(index_str[0])

    input_col = st.columns([1,1])
    with input_col[0]:
        explanation_df = keys_list
        index_str = st.multiselect("説明変数の選択",keys_list)
    with input_col[1]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else :
            """"""
            st.success(f'準備完了', icon="✅")
            explanation_data_df = read_data_df[index_str]
            data_len = explanation_data_df.shape[0]
    if st.checkbox("データの確認",key="cbox 02"):
        df = pd.DataFrame(explanation_data_df)
        df.index = df.index + 1
        st.dataframe(df)

    """___"""
    
    # 回帰分析の題名
    if len(index_str) == 1:
        """
        ### 2. 単回帰分析
        """
    else:
        """
        ### 2. 重回帰分析
        """      

    if st.button("計算の実行",key="button 01"):
        # 回帰分析の計算
        X = explanation_data_df # 説明変数
        y = purpose_data_df # 目的変数

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

        model = LinearRegression()
        model.fit(X_train, y_train)




        x_add_const = sm.add_constant(X)
        model_sm = sm.OLS(y, x_add_const).fit()
        # st.write(model_sm.summary())


        # 回帰統計

        st.write('回帰統計')

        X1 = sm.add_constant(X)
        m = sm.OLS(y, X1)
        result = m.fit()

        R2 = model.score(X, y)
        R = math.sqrt(R2)
        adjusted_R2 = result.rsquared_adj

        standard_error = np.sqrt(model_sm.mse_resid)
        s_xx = np.var(X)


        N = len(X)
        standard_error = format(standard_error)
        data1 = [R, R2, adjusted_R2, standard_error, N]
        index1 = ["重相関係数R", "決定係数R2", "自由度調整済みR2", "標準誤差", "観測数"]
        df = pd.DataFrame(data = data1, index = index1, columns=['回帰統計'])
        st.write(df)

        # 分散分析表

        st.write('分散分析表')
        # 自由度
        regression_free = len(X.columns)
        residual_free = N - regression_free - 1
        total_free = N - 1

        # 変動
        y_mean = np.mean(y)  # 目的変数の平均
        y_pred = model_sm.fittedvalues  # 予測値（モデルの計算）
        regression_variation = np.sum((y_pred - y_mean) ** 2)  # 回帰変動
        residual_variation = np.sum(model_sm.resid ** 2)       # 残差変動
        total_variation = regression_variation + residual_variation       # 合計変動

        # 分散
        regression_spread = regression_variation / regression_free
        residual_spread = residual_variation / residual_free

        # 観測された分散比
        f_statistic = model_sm.fvalue  # 観測された分散比
        prob_f_statistic = model_sm.f_pvalue # 有意F


        residual_variation = format(residual_variation)
        regression_spread = format(regression_spread)
        residual_spread = format(residual_spread)
        f_statistic = format(f_statistic)

        data2 = {
        '自由度':[regression_free, residual_free, total_free],
        '変動':[regression_variation, residual_variation, total_variation],
        '分散':[regression_spread, residual_spread, None],
        '観測された分散比':[f_statistic, None, None],
        '有意F':[prob_f_statistic, None, None]
        }
        index2 = ["回帰", "残差", "合計"]
        df = pd.DataFrame(data = data2, index = index2)
        st.write(df)


        # 切片とデータの結果
        df = pd.DataFrame(model_sm.summary().tables[1])

        df = df[1:]
        df.columns = ['0','係数', '標準偏差', 't', 'P-値', '下限95%', '上限95%']
        df.at[1, '0'] = '切片'
        df.index = df['0']
        df = df.drop('0', axis=1)
        st.dataframe(df)
        


#===============================================================================================
###  ユーザーデータによる分析体験
elif tub_dict[selected_cbox] == 1 :
    tub_counta += 1
    tub_title = list(tub_dict.keys())[tub_counta]
    f"""### {tub_title }"""
    """
    ### 1. 分析データのアップロード
    """
    uploaded_files = st.file_uploader("CSVファイルをアップロードしてください．")    
    if not uploaded_files:
        st.error('データがアップロードされていません', icon="⚠️")
        st.stop()
    else:        
        binary_data = uploaded_files.read()
        encode_data = detect(binary_data)  # エンコーディングを検出
        uploaded_files.seek(0) # ポインタを初期位置に戻し再度読み取り可能にする

        st.write(f"検出されたエンコーディング: {encode_data['encoding']}") # 確認用

        read_data_df = pd.read_csv(uploaded_files, encoding=encode_data['encoding'])



    """___"""

    # 目的変数の選択
    keys_list = list(read_data_df.keys())
    input_col = st.columns([1,1])
    with input_col[0]:
        index_str = st.multiselect("目的変数の選択",keys_list)
    
    disp_col = st.columns([1,4])
    with disp_col[0]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        elif len(index_str) > 1:
            """"""
            st.error("2つ以上選択されています．")
            st.stop()
        else :
            """"""
            st.success(f'準備完了', icon="✅")
            purpose_data_df = read_data_df[index_str]
            data_len = purpose_data_df.shape[0]
    with disp_col[1]:
        if st.checkbox("データの確認",key="cbox 01"):
            df = pd.DataFrame(purpose_data_df)
            df.index = df.index + 1
            st.dataframe(df)

    # 説明変数の選択
    keys_list = list(read_data_df.keys())

    keys_list.remove(index_str[0])

    input_col = st.columns([1,1])
    with input_col[0]:
        explanation_df = keys_list
        index_str = st.multiselect("説明変数の選択",keys_list)
    with input_col[1]:
        if not index_str:
            """"""
            st.error("データを選択してください")
            st.stop()
        else :
            """"""
            st.success(f'準備完了', icon="✅")
            explanation_data_df = read_data_df[index_str]
            data_len = explanation_data_df.shape[0]
    if st.checkbox("データの確認",key="cbox 02"):
        df = pd.DataFrame(explanation_data_df)
        df.index = df.index + 1
        st.dataframe(df)

    """___"""

    # 回帰分析の題名 
    if len(index_str) == 1: # 追加する
        """
        ### 2. 単回帰分析
        """
    else:
        """
        ### 2. 重回帰分析
        """      
    
    if st.button("計算の実行",key="button 01"):
        # 回帰分析の計算
        X = explanation_data_df # 説明変数
        y = purpose_data_df # 目的変数

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

        model = LinearRegression()
        model.fit(X_train, y_train)




        x_add_const = sm.add_constant(X)
        model_sm = sm.OLS(y, x_add_const).fit()
        # st.write(model_sm.summary())


        # 回帰統計

        st.write('回帰統計')

        X1 = sm.add_constant(X)
        m = sm.OLS(y, X1)
        result = m.fit()

        R2 = model.score(X, y)
        R = math.sqrt(R2)
        adjusted_R2 = result.rsquared_adj

        standard_error = np.sqrt(model_sm.mse_resid)
        s_xx = np.var(X)


        N = len(X)
        standard_error = format(standard_error)
        data1 = [R, R2, adjusted_R2, standard_error, N]
        index1 = ["重相関係数R", "決定係数R2", "自由度調整済みR2", "標準誤差", "観測数"]
        df = pd.DataFrame(data = data1, index = index1, columns=['回帰統計'])
        st.write(df)

        # 分散分析表

        st.write('分散分析表')
        # 自由度
        regression_free = len(X.columns)
        residual_free = N - regression_free - 1
        total_free = N - 1

        # 変動
        y_mean = np.mean(y)  # 目的変数の平均
        y_pred = model_sm.fittedvalues  # 予測値（モデルの計算）
        regression_variation = np.sum((y_pred - y_mean) ** 2)  # 回帰変動
        residual_variation = np.sum(model_sm.resid ** 2)       # 残差変動
        total_variation = regression_variation + residual_variation       # 合計変動

        # 分散
        regression_spread = regression_variation / regression_free
        residual_spread = residual_variation / residual_free

        # 観測された分散比
        f_statistic = model_sm.fvalue  # 観測された分散比
        prob_f_statistic = model_sm.f_pvalue # 有意F


        residual_variation = format(residual_variation)
        regression_spread = format(regression_spread)
        residual_spread = format(residual_spread)
        f_statistic = format(f_statistic)

        data2 = {
        '自由度':[regression_free, residual_free, total_free],
        '変動':[regression_variation, residual_variation, total_variation],
        '分散':[regression_spread, residual_spread, None],
        '観測された分散比':[f_statistic, None, None],
        '有意F':[prob_f_statistic, None, None]
        }
        index2 = ["回帰", "残差", "合計"]
        df = pd.DataFrame(data = data2, index = index2)
        st.write(df)


        # 切片とデータの結果
        df = pd.DataFrame(model_sm.summary().tables[1])

        df = df[1:]
        df.columns = ['0','係数', '標準偏差', 't', 'P-値', '下限95%', '上限95%']
        df.at[1, '0'] = '切片'
        df.index = df['0']
        df = df.drop('0', axis=1)
        st.dataframe(df)