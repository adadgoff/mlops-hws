import os
import subprocess

from contextlib import (
    contextmanager,
    asynccontextmanager,
)
from functools import partial
from pathlib import Path

# from threading import Timer
from typing import (
    AsyncGenerator,
    Generator,
    NamedTuple,
)

from dvc.api import DVCFileSystem
from dvc.repo import Repo
from fastapi import UploadFile


CHUNK_SIZE = 8192

DVC_FOLDER = Path("data")
DVC_TEMP_FOLDER = DVC_FOLDER / "temp"


_dvc = partial(
    subprocess.run,
    capture_output=True,
    check=True,
    cwd=DVC_FOLDER,
    shell=False,
    text=True,
)


class DVCException(Exception):
    pass


class Dataset(NamedTuple):
    name: str
    size: str


class DVCFileSystemOnSteroids(DVCFileSystem):
    def exists(
        self,
        dataset_name: str,
    ) -> bool:
        datasets_names = {
            dataset.name  # noqa.
            for dataset in self.ls()
        }
        return dataset_name in datasets_names

    def ls(
        self,
    ) -> list[Dataset]:
        result = _dvc(
            args=[
                "dvc",
                "ls",
                ".",
                "--dvc-only",
                "--size",
            ],
        )
        strings = list(
            filter(
                bool,
                result.stdout.strip().split(),
            )
        )
        if len(strings) % 2 != 0:
            raise DVCException(
                "dvc ls вернуло нечетное количество элементов.",
            )
        datasets = [
            Dataset(
                name=name.strip(),
                size=size.strip(),
            )
            for size, name in zip(
                strings[::2],
                strings[1::2],
            )
        ]
        return datasets

    def put_file(
        self,
        lpath: str,
    ) -> None:
        self.repo.add(lpath)
        self.repo.push()

    def rm(
        self,
        path: str,
    ) -> None:
        path += ".dvc"
        self.repo.remove(path)
        self.repo.push()
        self.repo.gc(
            workspace=True,
            cloud=True,
        )


dvc_file_system = DVCFileSystemOnSteroids(
    repo=Repo(root_dir=DVC_FOLDER),
)


@contextmanager
def dvc_temp_from_remote_manager(
    dataset_name: str,
) -> Generator[str, None, None]:
    temp_dataset_filepath = DVC_TEMP_FOLDER / dataset_name
    # Создание файла в локальное временное хранилище.
    dvc_file_system.get_file(
        rpath=dataset_name,
        lpath=temp_dataset_filepath,
    )

    try:
        yield temp_dataset_filepath
    finally:
        os.remove(temp_dataset_filepath)
        # Timer(
        #     interval=2,
        #     function=lambda: os.remove(temp_dataset_filepath),
        # ).start()


@asynccontextmanager
async def dvc_temp_from_local_manager(
    dataset_name: str,
    dataset_file: UploadFile,
) -> AsyncGenerator[str, None]:
    dataset_filepath = DVC_FOLDER / dataset_name
    # Создание файла в локальное временное хранилище.
    await dataset_file.seek(0)
    with open(
        dataset_filepath,
        mode="w",
    ) as temp_dataset_file:
        while chunk := await dataset_file.read(
            size=CHUNK_SIZE,
        ):
            temp_dataset_file.write(
                chunk.decode(),
            )

    try:
        yield dataset_filepath
    finally:
        os.remove(
            path=dataset_filepath,
        )
        # Timer(
        #     interval=2,
        #     function=lambda: os.remove(
        #         path=dataset_filepath,
        #     ),
        # ).start()
