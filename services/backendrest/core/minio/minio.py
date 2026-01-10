from minio import Minio

from core.config import settings


MINIO_ML_MODELS_BUCKET: str = "mlmodels"


client = Minio(
    endpoint=settings.MINIO_CONSOLE,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)
