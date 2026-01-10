import streamlit as st

from _3_widgets import (
    created_ml_models_dataframe,
    datasets_dataframe,
    no_created_ml_models_for_train_text,
    no_datasets_for_train_text,
)
from _4_features import (
    get_created_ml_models,
    get_datasets,
    train_ml_model,
)
from _5_entities import (
    CreatedMLModel,
    Dataset,
)
from _6_shared.api import OK_STATUS


train_page = st.Page(
    "_2_pages/train.py",
    title="Обучение ML моделей",
    icon="💪",
    url_path="/train",
    default=False,
)


if __name__ == "__main__":
    st.title("💪 Обучение ML моделей")

    st.markdown(
        body="""
        > ***Обучение ML модели*** - настройка
        внутренних параметров на основе входных
        данных.
        """,
    )

    created_ml_models: list[CreatedMLModel] = get_created_ml_models()
    if created_ml_models:
        created_ml_model_name = st.selectbox(
            label="Выберите ML модель для обучения:",
            options=(
                created_ml_model.name  # noqa.
                for created_ml_model in created_ml_models
            ),
        )
        with st.expander(
            label="Подробнее о созданных ML моделях.",
        ):
            created_ml_models_dataframe(
                created_ml_models=created_ml_models,
            )
    else:
        no_created_ml_models_for_train_text()

    datasets: list[Dataset] = get_datasets()
    if datasets:
        dataset_name = st.selectbox(
            label="Выберите датасет для обучения:",
            options=(
                dataset.name  # noqa.
                for dataset in datasets
            ),
        )
        with st.expander(
            label="Подробнее о загруженных датасетах.",
        ):
            datasets_dataframe(
                datasets=datasets,
            )
    else:
        no_datasets_for_train_text()

    if st.button(
        label="Обучить",
        icon=":material/publish:",
        width="stretch",
        disabled=(
            len(created_ml_models) == 0  # noqa.
            or len(datasets) == 0
        ),
    ):
        response = train_ml_model(
            ml_model_name=created_ml_model_name,
            dataset_name=dataset_name,
        )
        if response.status_code == OK_STATUS:
            st.toast(
                body=f"""
                    ML модель {created_ml_model_name} успешно
                    обучилась на датасете {dataset_name}.
                """,
                icon=":material/check:",
                duration="short",
            )
        else:
            st.toast(
                body=f"Ошибка: {response.json()}.",
                icon=":material/error:",
                duration="short",
            )
