import streamlit as st

from _4_features import (
    delete_dataset,
    get_datasets,
)
from _5_entities import Dataset


@st.dialog(
    title="Удалить датасет",
    width="medium",
)
def delete_dataset_modal():
    datasets: list[Dataset] = get_datasets()

    name = st.selectbox(
        label="Имя удаляемого датасета:",
        options=(
            dataset.name  # noqa.
            for dataset in datasets
        ),
    )

    if st.button(
        label="Удалить выбранный датасет навсегда",
        type="primary",
        icon=":material/delete_forever:",
        width="stretch",
    ):
        response: str | dict = delete_dataset(
            dataset_name=name,
        )
        if isinstance(response, str):
            st.toast(
                body=f"Датасет {response} успешно удален.",
                icon=":material/check:",
                duration="short",
            )
        else:
            st.toast(
                body=f"Ошибка: {response}.",
                icon=":material/error:",
                duration="short",
            )
