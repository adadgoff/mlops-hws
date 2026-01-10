import streamlit as st

from _5_entities import Dataset


def datasets_dataframe(
    datasets: list[Dataset],
):
    data = [
        dataset.model_dump()  # noqa.
        for dataset in datasets
    ]
    st.dataframe(
        data=data,
        width="stretch",
        hide_index=True,
        column_order=(
            "name",
            "size",
        ),
        column_config={
            "name": "Имя",
            "size": "Размер",
        },
    )
