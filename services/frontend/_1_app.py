import streamlit as st

from _2_pages import (
    datasets_page,
    inference_page,
    train_page,
    ml_models_page,
)
from _3_widgets import sidebar


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
    )

    sidebar()

    pg = st.navigation(
        [
            ml_models_page,
            datasets_page,
            train_page,
            inference_page,
        ],
        position="top",
        expanded=True,
    )
    pg.run()
