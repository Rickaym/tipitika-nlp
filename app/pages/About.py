import streamlit as st

st.set_page_config(page_title="About Project", page_icon="📈")

with open("../README.md", "r", encoding="utf-8") as f:
    info = f.read()

st.markdown("# About Project")
st.markdown(info.split("<!-- Body -->")[-1])
