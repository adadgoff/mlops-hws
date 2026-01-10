from string import (
    ascii_letters,
    digits,
)

ALLOWED_DATASET_NAME_CHARACTERS = (
    ascii_letters  # noqa.
    + digits
    + "_"
)


def verify_dataset_name(
    dataset_name: str,
) -> bool:
    return all(
        character in ALLOWED_DATASET_NAME_CHARACTERS  # noqa.
        for character in dataset_name
    )
