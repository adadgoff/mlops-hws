import streamlit as st

from _3_widgets import (
    created_ml_models_dataframe,
    datasets_dataframe,
    no_created_ml_models_for_inference_text,
    no_datasets_for_inference_text,
)
from _4_features import (
    get_created_ml_models,
    get_datasets,
    get_trained_ml_models,
    inference_ml_model,
)
from _5_entities import (
    CreatedMLModel,
    Dataset,
    TrainedMLModel,
)


inference_page = st.Page(
    "_2_pages/inference.py",
    title="Инференс ML моделей",
    icon="🤙",
    url_path="/inference",
    default=False,
)


if __name__ == "__main__":
    st.title("🤙 Инференс ML моделей")

    st.markdown(
        body="""
        > ***Инференс (inference) ML модели*** - вывод
        предсказаний обученной ML модели на новых
        входных данных.
        """,
    )

    created_ml_models: list[CreatedMLModel] = get_created_ml_models()
    trained_ml_models: list[TrainedMLModel] = get_trained_ml_models()
    if trained_ml_models:
        trained_ml_model_name = st.selectbox(
            label="Выберите ML модель для инференса:",
            options=(
                trained_ml_model.name  # noqa.
                for trained_ml_model in trained_ml_models
            ),
        )
        with st.expander(
            label="Подробнее о созданных ML моделях.",
        ):
            created_ml_models_dataframe(
                created_ml_models=created_ml_models,
            )
    else:
        no_created_ml_models_for_inference_text()

    datasets: list[Dataset] = get_datasets()
    if datasets:
        dataset_name = st.selectbox(
            label="Выберите датасет для инференса:",
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
        no_datasets_for_inference_text()

    if st.button(
        label="Получить инференс",
        icon=":material/search:",
        width="stretch",
        disabled=(
            len(created_ml_models) == 0  # noqa.
            or len(datasets) == 0
        ),
    ):
        response = inference_ml_model(
            ml_model_name=trained_ml_model_name,
            dataset_name=dataset_name,
        )
        if isinstance(response, str):
            st.toast(
                body=f"""
                    Инференс сохранен в файл {response}.
                    Скачайте его через MinIO и посмотрите результаты.
                """,
                icon=":material/check:",
                duration="long",
            )
        else:
            st.toast(
                body=f"Ошибка: {response}.",
                icon=":material/error:",
                duration="short",
            )
