from prometheus_client import Histogram, Counter, Gauge

# Гистограмма времени инференса
ML_INFERENCE_DURATION = Histogram(
    'ml_inference_duration_seconds',
    'Время выполнения ML инференса',
    ['model_name'],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

# Счётчик запросов инференса
ML_INFERENCE_REQUESTS = Counter(
    'ml_inference_requests_total',
    'Общее количество запросов ML инференса',
    ['model_name', 'status']
)

# Гейдж количества активных моделей
ML_ACTIVE_MODELS = Gauge(
    'ml_active_models_count',
    'Количество активных ML моделей'
)

def get_metrics():
    """Получение метрик для использования в роутерах"""
    return {
        'inference_duration': ML_INFERENCE_DURATION,
        'inference_requests': ML_INFERENCE_REQUESTS,
        'active_models': ML_ACTIVE_MODELS,
    }