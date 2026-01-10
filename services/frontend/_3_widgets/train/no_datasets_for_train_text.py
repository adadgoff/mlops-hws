import streamlit as st


def no_datasets_for_train_text():
    st.markdown(
        body="""
        Нет загруженных датасетов для обучения.
        Сначала загрузите датасет на
        [странице датасетов](/datasets).
        """,
    )
