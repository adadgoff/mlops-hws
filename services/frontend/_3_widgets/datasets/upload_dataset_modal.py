import streamlit as st

from _4_features import upload_dataset


@st.dialog(
    title="Загрузить датасет",
    width="medium",
)
def upload_dataset_modal():
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
        label="Имя загружаемого датасета:",
        placeholder="bestname",
        icon=":material/label:",
    )
    if not name:
        st.error(
            body="Имя не может быть пустым.",
            icon=":material/error:",
        )

    st.info(
        body="""
        Датасет должен:
        1. Иметь только численные столбцы (целые и дробные числа);
        2. Иметь столбец `target` для обучения;
        3. Не иметь столбец `target` для инференса;
        4. Иметь запятую в качестве разделителя.
        """,
        icon=":material/info:",
    )
    st.markdown(
        body="""
        <style>
        div[data-testid="stFileUploaderDropzoneInstructions"]
        >div
        >span:first-child {
            visibility: hidden;
        }
        div[data-testid="stFileUploaderDropzoneInstructions"]
        >div
        >span:first-child::before {
            content: "Прикрепите файл здесь";
            visibility: visible;
        }

        div[data-testid="stFileUploaderDropzoneInstructions"]
        >div
        >span:last-child {
            visibility: hidden;
        }
        div[data-testid="stFileUploaderDropzoneInstructions"]
        >div
        >span:last-child::before {
            content: "Лимит размера 4 ГБ⠀•⠀CSV";
            visibility: visible;
        }

        section[data-testid="stFileUploaderDropzone"]
        >span
        >button[data-testid="stBaseButton-secondary"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    file = st.file_uploader(
        label="Выберите файл для загрузки:",
        type="csv",
        accept_multiple_files=False,
        width="stretch",
    )

    if st.button(
        label="Загрузить датасет",
        icon=":material/upload:",
        disabled=len(name) == 0 or file is None,
        width="stretch",
    ):
        response: str | dict = upload_dataset(
            dataset_name=name,
            dataset_file=file,
        )
        if isinstance(response, str):
            st.toast(
                body=f"Датасет {response} успешно загружен.",
                icon=":material/check:",
                duration="short",
            )
        else:
            st.toast(
                body=f"Ошибка: {response}.",
                icon=":material/error:",
                duration="short",
            )
