"""Streamlit UI: upload a CSV and ask questions in plain English."""
import pandas as pd
import streamlit as st

from analyst_agent.agent import answer_question, result_to_text

st.set_page_config(page_title="NL Data Analyst Agent", page_icon="📊")
st.title("📊 Natural-Language Data Analyst Agent")

file = st.file_uploader("Upload a CSV file", type="csv")
if file:
    df = pd.read_csv(file)
    st.write(f"Loaded **{len(df)} rows**, **{len(df.columns)} columns**")
    st.dataframe(df.head())

    question = st.text_input("Ask a question about your data")
    if st.button("Ask") and question:
        with st.spinner("Thinking..."):
            res = answer_question(df, question)

        if res.success:
            st.success(res.explanation)
            st.subheader("Raw result")
            st.text(result_to_text(res.result))
        else:
            st.error(res.explanation)

        with st.expander(f"Show generated code ({len(res.attempts)} attempt(s))"):
            for a in res.attempts:
                st.markdown(f"**Attempt {a['attempt']}**")
                st.code(a["code"], language="python")
                if a["error"]:
                    st.warning(a["error"])
