import pandas as pd
import streamlit as st

st.set_page_config(page_title="Associated Data", page_icon="📈")

st.markdown("# Associated Data")
st.sidebar.header("Associated Data")


abhidamma = pd.read_csv('./data/sc-data-abhidhamma.csv')
st.dataframe(abhidamma)
