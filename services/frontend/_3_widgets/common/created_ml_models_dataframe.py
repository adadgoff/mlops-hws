import streamlit as st

from _5_entities import CreatedMLModel


def created_ml_models_dataframe(
    created_ml_models: list[CreatedMLModel],
):
    data = [
        created_ml_model.model_dump()  # noqa.
        for created_ml_model in created_ml_models
    ]
    st.dataframe(
        data=data,
        width="stretch",
        hide_index=True,
        column_order=(
            "name",
            "type",
            "parameters",
            "trained",
        ),
        column_config={
            "name": "Имя",
            "type": "Тип",
            "parameters": "Параметры",
            "trained": "Обучен",
        },
    )
