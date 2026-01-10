import json

import streamlit as st

from _3_widgets.ml_models.no_created_ml_models_text import (
    no_created_ml_models_text,
)
from _4_features import (
    get_created_ml_models,
    delete_ml_model,
)
from _5_entities import CreatedMLModel
from _6_shared.types import Parameters


@st.dialog(
    title="Удалить ML модель",
    width="medium",
)
def delete_ml_model_modal():
    created_ml_models: list[CreatedMLModel] = get_created_ml_models()
    created_ml_models_map: dict[str, dict[str, str | Parameters]] = {
        created_ml_model.name: {
            "type": created_ml_model.type,
            "parameters": created_ml_model.parameters,
        }
        for created_ml_model in created_ml_models
    }

    if created_ml_models_map:
        name = st.selectbox(
            label="Имя удаляемой ML модели:",
            options=created_ml_models_map.keys(),
        )

        st.markdown(
            body=f"""
            Тип удаляемой ML модели: `{created_ml_models_map[name]["type"]}`.
            """,
        )

        st.text(
            body="Параметры удаляемой ML модели:",
        )
        st.code(
            body=json.dumps(
                obj=created_ml_models_map[name]["parameters"],
                indent=2,
            ),
            language="json5",
            line_numbers=True,
            wrap_lines=True,
        )

        if st.button(
            label="Удалить выбранную ML модель навсегда",
            type="primary",
            icon=":material/delete_forever:",
            width="stretch",
        ):
            response: str | dict = delete_ml_model(
                ml_model_name=name,
            )
            if isinstance(response, str):
                st.toast(
                    body=f"ML модель {response} успешно удалена.",
                    icon=":material/check:",
                    duration="short",
                )
            else:
                st.toast(
                    body=f"Ошибка: {response}.",
                    icon=":material/error:",
                    duration="short",
                )

    else:
        no_created_ml_models_text()
