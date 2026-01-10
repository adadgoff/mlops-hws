from core import settings

from minio import Minio


BUCKETS_NAMES = [
    "datasets",
    "mlmodels",
]


def setup_minio_buckets() -> None:
    client = Minio(
        endpoint=settings.MINIO_CONSOLE,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False,
    )
    for bucket_name in BUCKETS_NAMES:
        if not client.bucket_exists(
            bucket_name=bucket_name,
        ):
            client.make_bucket(
                bucket_name=bucket_name,
            )


if __name__ == "__main__":
    setup_minio_buckets()
