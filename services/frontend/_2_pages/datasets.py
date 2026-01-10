import streamlit as st

from _3_widgets import (
    datasets_dataframe,
    download_dataset_modal,
    delete_dataset_modal,
    no_datasets_text,
    upload_dataset_modal,
)
from _4_features import get_datasets
from _5_entities import Dataset


datasets_page = st.Page(
    "_2_pages/datasets.py",
    title="Датасеты",
    icon="📁",
    url_path="/datasets",
    default=False,
)


if __name__ == "__main__":
    st.title("📁 Датасеты")

    st.markdown(
        body="""
        > ***Датасет (Dataset)*** - набор данных
        для [обучения](/train)
        или [инференса](/inference)
        [ML моделей](/).
        """,
    )

    st.header("Загруженные датасеты")

    datasets: list[Dataset] = get_datasets()
    if datasets:
        datasets_dataframe(
            datasets=datasets,
        )
    else:
        no_datasets_text()

    control_buttons = st.container(
        width="stretch",
        horizontal=True,
        horizontal_alignment="center",
    )

    if control_buttons.button(
        label="Загрузить датасет",
        icon=":material/upload:",
        width="stretch",
    ):
        upload_dataset_modal()

    if control_buttons.button(
        label="Скачать датасет",
        icon=":material/download:",
        width="stretch",
        help=(
            "Нет загруженных датасетов."  # noqa.
            if len(datasets) == 0
            else None
        ),
        disabled=len(datasets) == 0,
    ):
        download_dataset_modal()

    if control_buttons.button(
        label="Удалить датасет",
        icon=":material/delete_forever:",
        width="stretch",
        help=(
            "Нет загруженных датасетов."  # noqa.
            if len(datasets) == 0
            else None
        ),
        disabled=len(datasets) == 0,
    ):
        delete_dataset_modal()
