from copy import deepcopy
from functools import partial

import streamlit as st

from _4_features import (
    get_datasets,
    download_dataset,
)
from _5_entities import Dataset


@st.dialog(
    title="Скачать датасет",
    width="medium",
)
def download_dataset_modal():
    datasets: list[Dataset] = get_datasets()

    name = st.selectbox(
        label="Имя скачиваемого датасета:",
        options=(
            dataset.name  # noqa.
            for dataset in datasets
        ),
    )

    st.download_button(
        label="Скачать датасет",
        data=deepcopy(
            partial(
                download_dataset,
                name,
            ),
        ),
        icon=":material/download:",
        file_name=name,
        mime="csv",
        width="stretch",
    )
