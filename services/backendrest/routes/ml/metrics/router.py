import os

from fastapi import APIRouter, HTTPException, status

from core.metrics import get_metrics_data

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics", "Prometheus Metrics"],
)

@router.get("/health", summary="Проверка здоровья сервиса")
async def get_health() -> dict:
    return {"status": "healthy"}

@router.get("/system", summary="Получить системные метрики")
async def get_system_metrics() -> dict:
    try:
        metrics_data = get_metrics_data()
        return metrics_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении метрик: {str(e)}"
        )

@router.get("/model-training", summary="Получить метрики обучения моделей")
async def get_model_training_metrics() -> dict:
    try:
        metrics_data = get_metrics_data()
        return {
            "model_training": {
                "total_models": metrics_data.get("total_models", 0),
                "trained_models": metrics_data.get("trained_models", 0),
                "training_duration": metrics_data.get("training_duration", 0)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении метрик обучения: {str(e)}"
        )

@router.get("/inference", summary="Получить метрики инференса")
async def get_inference_metrics() -> dict:
    try:
        metrics_data = get_metrics_data()
        return {
            "inference": {
                "total_inferences": metrics_data.get("total_inferences", 0),
                "successful_inferences": metrics_data.get("successful_inferences", 0),
                "failed_inferences": metrics_data.get("failed_inferences", 0)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении метрик инференса: {str(e)}"
        )