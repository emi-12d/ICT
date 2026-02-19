import streamlit as st
import pandas as pd

"""
  活動記録
"""

from module import col

if st.button("九九"):
  st.write_stream(col.kake)