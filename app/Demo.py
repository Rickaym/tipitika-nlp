import streamlit as st
from api import process

st.set_page_config("Tipitika Recall", page_icon="🪔", layout="wide")
st.write("# 🪔 Tipitika Recall!")


def format_dict(dict):
    return "".join(f"{k}: {v}\n\n" for k, v in dict.items())


MODELS = {
    "abhidhamma-search": "Dense retrival algorithm, no new content is generated or interpreted",
    "abhidhamma-rag": "RAG algorithm, new content or interpretation is generated",
}

with st.form("query_collection"):
    col1, col2 = st.columns(2)
    with col1:
        text = st.text_input("Query")
    with col2:
        collection = st.selectbox("Model", list(MODELS.keys()))
    
    if collection:
        st.html(f"<i>{MODELS.get(collection)}</i>")
    
    submitted = st.form_submit_button("Submit")

    if submitted and collection:
        st.spinner("In progress")
        st.table(
            [
                {"metadata": format_dict(meta), "content": content}
                for meta, content in process(text, collection)
            ]
        )
