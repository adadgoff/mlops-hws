import streamlit as st


def no_created_ml_models_for_train_text():
    st.markdown(
        body="""
        Нет созданных ML моделей для обучения.
        Сначала создайте ML модель на
        [странице ML моделей](/).
        """,
    )
