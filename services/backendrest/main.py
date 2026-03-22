from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from core.clearml import setup_clearml_credentials
from routes import (
    datasets_router,
    health_router,
    ml_inference_router,
    ml_crud_router,
    ml_train_router,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_clearml_credentials()
    yield

title = "MLOps HW1"
description = """**REST API** для обучения моделей и работы с датасетами."""

app = FastAPI(
    title=title,
    description=description,
    lifespan=lifespan,
    version="0.1",
)

# === Настройка Prometheus метрик ===
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated_endpoints=True,
).instrument(app).expose(
    app,
    endpoint="/metrics",
    tags=["Monitoring"],
)
# ================================

app.include_router(health_router)
app.include_router(ml_crud_router)
app.include_router(ml_train_router)
app.include_router(ml_inference_router)
app.include_router(datasets_router)