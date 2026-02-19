import streamlit as st
import pandas as pd

def calc_area(r):
  return r ** 2 * 3.14

"""
#### 重回帰分析
"""
df = pd.read_csv("pages/sample_datas/scatter_data01.csv",encoding='shift_jis')
df.head()


from sklearn.model_selection import train_test_split

X, y = df.drop('data 1', axis=1), df['data 1']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)

coefficient_df = pd.Series(model.coef_,index = X.columns)


st.write('回帰係数')
st.dataframe(coefficient_df)
st.write('切片{}'.format(model.intercept_))

st.write('決定係数(train):{:.3f}'.format(model.score(X_train, y_train)))
st.write('決定係数(test):{:.3f}'.format(model.score(X_test,y_test)))