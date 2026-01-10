import streamlit as st


def no_created_ml_models_for_inference_text():
    st.markdown(
        body="""
        Нет обученных ML моделей для инференса.
        Сначала создайте ML модель на
        [странице ML моделей](/)
        и обучите на
        [странице обучения](/train).
        """,
    )
