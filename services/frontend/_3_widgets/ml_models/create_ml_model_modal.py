import json

import streamlit as st
from code_editor import code_editor

from _4_features import (
    create_ml_model,
    get_ml_models,
)
from _5_entities import MLModel
from _6_shared.api import DOCS_URL
from _6_shared.types import Parameters


@st.dialog(
    title="Создать ML модель",
    width="medium",
)
def create_ml_model_modal():
    ml_models: list[MLModel] = get_ml_models()
    ml_models_map: dict[str, Parameters] = {
        ml_model.type: ml_model.parameters  # noqa.
        for ml_model in ml_models
    }

    st.markdown(
        body="""
        <style>
        div[data-testid="InputInstructions"]
        >span {
            visibility: hidden;
        }
        div[data-testid="InputInstructions"]
        >span::after {
            content: "Нажмите Enter для сохранения";
            visibility: visible;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    name = st.text_input(
        label="Имя создаваемой ML модели:",
        placeholder="bestname",
        icon=":material/label:",
    )
    if not name:
        st.error(
            body="Имя не может быть пустым.",
            icon=":material/error:",
        )

    type_ = st.selectbox(
        label="Тип создаваемой ML модели:",
        options=ml_models_map.keys(),
    )

    code_editor_dict = code_editor(
        # Обновление состояния редактора кода.
        key="code-editor",
        allow_reset=True,
        response_mode=["blur", "debounce"],
        focus=False,
        # Другие настройки.
        code=json.dumps(
            obj=ml_models_map[type_],
            indent=2,
        ),
        lang="json5",
        height=[10, 40],
        buttons=[
            {
                "name": "Copy",
                "feather": "Copy",
                "alwaysOn": True,
                "commands": ["copyAll"],
                "style": {
                    "top": "0.46rem",
                    "right": "0.4rem",
                },
            },
        ],
        props={
            "enableBasicAutocompletion": False,
            "enableLiveAutocompletion": False,
            "enableSnippets": False,
        },
        options={
            "showLineNumbers": True,
        },
    )
    if not code_editor_dict["id"]:
        code_editor_dict["text"] = json.dumps(ml_models_map[type_])

    st.markdown(
        body=f"""
        Узнать больше про возможные параметры и их значения
        ML модели можно в [документации API]({DOCS_URL}).
        """,
    )

    if st.button(
        label="Создать ML модель",
        icon=":material/add:",
        disabled=len(name) == 0,
        width="stretch",
    ):
        response: str | dict = create_ml_model(
            ml_model_name=name,
            ml_model_type=type_,
            parameters=json.loads(code_editor_dict["text"]),
        )
        if isinstance(response, str):
            st.toast(
                body=f"ML модель {response} успешно создана.",
                icon=":material/check:",
                duration="short",
            )
        else:
            st.toast(
                body=f"Ошибка: {response}.",
                icon=":material/error:",
                duration="short",
            )
