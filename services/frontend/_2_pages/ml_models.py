import streamlit as st

from _3_widgets import (
    create_ml_model_modal,
    created_ml_models_dataframe,
    delete_ml_model_modal,
    no_created_ml_models_text,
)
from _4_features import get_created_ml_models
from _5_entities import CreatedMLModel


ml_models_page = st.Page(
    "_2_pages/ml_models.py",
    title="ML Модели",
    icon="⚙️",
    url_path="/",
    default=True,
)


if __name__ == "__main__":
    st.title("⚙️ ML Модели")

    st.markdown(
        body="""
        > ***ML (Machine Learning) модель*** - модель
        машинного обучения.
        """,
    )

    st.header("Созданные ML модели")

    created_ml_models: list[CreatedMLModel] = get_created_ml_models()
    if created_ml_models:
        created_ml_models_dataframe(
            created_ml_models=created_ml_models,
        )
    else:
        no_created_ml_models_text()

    control_buttons = st.container(
        width="stretch",
        horizontal=True,
        horizontal_alignment="center",
    )

    if control_buttons.button(
        label="Создать ML модель",
        icon=":material/add:",
        width="stretch",
    ):
        create_ml_model_modal()

    if control_buttons.button(
        label="Удалить ML модель",
        icon=":material/delete_forever:",
        width="stretch",
        help=(
            "Нет созданных ML моделей."  # noqa.
            if len(created_ml_models) == 0
            else None
        ),
        disabled=len(created_ml_models) == 0,
    ):
        delete_ml_model_modal()
