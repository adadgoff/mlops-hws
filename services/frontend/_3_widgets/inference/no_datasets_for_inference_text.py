import streamlit as st


def no_datasets_for_inference_text():
    st.markdown(
        body="""
        Нет загруженных датасетов для инференса.
        Сначала загрузите датасет на
        [странице датасетов](/datasets).
        """,
    )
