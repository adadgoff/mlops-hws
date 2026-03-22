from typing import Dict, Any
from prometheus_client import Counter, Histogram, Summary

# HTTP requests counter
HTTP_REQUESTS_TOTAL = Counter(
    'http_requests_total',
    'Total number of HTTP requests by endpoint',
    labelnames=['endpoint']
)

# HTTP request duration histogram
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    labelnames=['endpoint'],
    buckets=[0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# ML inference duration histogram
ML_INFERENCE_DURATION_SECONDS = Histogram(
    'ml_inference_duration_seconds',
    'Duration of ML inference in seconds',
    labelnames=['model_type'],
    buckets=[0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# HTTP errors counter
HTTP_ERRORS_TOTAL = Counter(
    'http_errors_total',
    'Total number of HTTP errors (4xx/5xx)',
    labelnames=['status_code']
)

# Function to record metrics
def record_metrics(endpoint: str, status_code: int = 200, duration: float = 0.0, model_type: str = 'unknown') -> None:
    """
    Record metrics for HTTP requests and ML inference.
    
    Args:
        endpoint: The HTTP endpoint that was called
        status_code: The HTTP status code of the response
        duration: The duration of the request in seconds
        model_type: The type of ML model used for inference
    """
    if status_code >= 400:
        HTTP_ERRORS_TOTAL.labels(status_code=status_code).inc()
    
    HTTP_REQUESTS_TOTAL.labels(endpoint=endpoint).inc()
    
    if duration > 0:
        HTTP_REQUEST_DURATION_SECONDS.labels(endpoint=endpoint).observe(duration)
    
    if model_type != 'unknown':
        ML_INFERENCE_DURATION_SECONDS.labels(model_type=model_type).observe(duration)