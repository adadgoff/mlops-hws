# PLAN.md

## Фаза 1: Мониторинг (ДЗ 3)

1. **Добавить prometheus-client в зависимости backendrest**

   - Файл: `services/backendrest/pyproject.toml`
   - Пример конфигурации:
     ```toml
     [tool.poetry.dependencies]
     prometheus_client = "^0.14.0"
     ```
   - Команда проверки: `pip install prometheus_client`

2. **Создать эндпоинт /metrics для Prometheus**

   - Файл: `services/backendrest/routes/ml/inference/router.py`
   - Пример кода:

     ```python
     from fastapi import APIRouter
     from prometheus_client import Counter, Histogram

     router = APIRouter()

     http_requests_total = Counter("http_requests_total", "Total number of HTTP requests")
     http_request_duration_seconds = Histogram("http_request_duration_seconds", "HTTP request duration in seconds")
     ml_inference_duration_seconds = Histogram("ml_inference_duration_seconds", "ML inference duration in seconds")
     http_errors_total = Counter("http_errors_total", "Total HTTP errors")

     @router.get("/metrics")
     def metrics():
         return {
             "http_requests_total": http_requests_total,
             "http_request_duration_seconds": http_request_duration_seconds,
             "ml_inference_duration_seconds": ml_inference_duration_seconds,
             "http_errors_total": http_errors_total
         }
     ```

   - Команда проверки: `uvicorn services/backendrest/main:app --reload`

3. **Добавить метрики:**

   - Файл: `services/backendrest/core/prometheus.py`
   - Пример конфигурации:

     ```python
     from prometheus_client import Counter, Histogram

     http_requests_total = Counter("http_requests_total", "Total number of HTTP requests")
     http_request_duration_seconds = Histogram("http_request_duration_seconds", "HTTP request duration in seconds")
     ml_inference_duration_seconds = Histogram("ml_inference_duration_seconds", "ML inference duration in seconds")
     http_errors_total = Counter("http_errors_total", "Total HTTP errors")
     ```

   - Команда проверки: `python -m prometheus_client`

4. **Добавить VictoriaMetrics в kubernetes манифесты**

   - Файл: `kubernetes/minio/victoriametrics.yaml`
   - Пример конфигурации:
     ```yaml
     apiVersion: v1
     kind: Service
     metadata:
       name: victoriametrics
     spec:
       ports:
         - port: 9090
           targetPort: 9090
     ```
   - Команда проверки: `kubectl apply -f kubernetes/minio/victoriametrics.yaml`

5. **Добавить Grafana в kubernetes манифесты**

   - Файл: `kubernetes/grafana/grafana.yaml`
   - Пример конфигурации:
     ```yaml
     apiVersion: apps/v1
     kind: Deployment
     metadata:
       name: grafana
     spec:
       replicas: 1
       template:
         spec:
           containers:
             - name: grafana
               image: grafana/grafana:latest
               ports:
                 - containerPort: 3000
     ```
   - Команда проверки: `kubectl apply -f kubernetes/grafana/grafana.yaml`

6. **Настроить дашборд в Grafana с метриками**
   - Файл: `kubernetes/grafana/dashboards.yaml`
   - Пример конфигурации:
     ```yaml
     - name: "MLOps Metrics Dashboard"
       panels:
         - type: "graph"
           title: "HTTP Requests"
           targets:
             - expr: "http_requests_total"
     ```
   - Команда проверки: `kubectl apply -f kubernetes/grafana/dashboards.yaml`

## Фаза 2: Нагрузочное тестирование (ДЗ 3)

7. **Добавить locust в зависимости**

   - Файл: `services/backendrest/pyproject.toml`
   - Пример конфигурации:
     ```toml
     [tool.poetry.dependencies]
     locust = "^2.15.0"
     ```
   - Команда проверки: `pip install locust`

8. **Создать сценарии нагрузочного тестирования:**

   - Файл: `services/backendrest/tests/load_tests.py`
   - Пример кода:

     ```python
     from locust import User, task, between

     class HealthCheckUser(User):
         wait_time = between(1, 5)

         @task
         def health_check(self):
             pass

     class InferenceUser(User):
         wait_time = between(1, 5)

         @task
         def inference(self):
             pass

     class UploadUser(User):
         wait_time = between(1, 5)

         @task
         def upload(self):
             pass
     ```

   - Команда проверки: `locust -f services/backendrest/tests/load_tests.py`

9. **Написать скрипт запуска нагрузочного тестирования**

   - Файл: `services/backendrest/scripts/run_load_test.sh`
   - Пример скрипта:
     ```bash
     #!/bin/bash
     locust -f services/backendrest/tests/load_tests.py --host=http://localhost:8000
     ```
   - Команда проверки: `chmod +x services/backendrest/scripts/run_load_test.sh`

10. **Создать отчёт по нагрузочному тестированию**
    - Файл: `services/backendrest/reports/load_test_report.md`
    - Пример отчёта:
      ```markdown
      # Результаты нагрузочного тестирования

      - Тестирование прошло успешно
      - Среднее время запроса: 250 ms
      - Максимальная нагрузка: 1000 пользователей
      ```
    - Команда проверки: `cat services/backendrest/reports/load_test_report.md`

## Фаза 3: Документация (ДЗ 2)

11. **Создать CHANGELOG.md с историей изменений**

    - Файл: `CHANGELOG.md`
    - Пример содержимого:
      ```markdown
      # CHANGELOG

      ## 0.1.0

      - Добавлен мониторинг с Prometheus
      - Добавлены нагрузочные тесты с Locust
      ```
    - Команда проверки: `git add CHANGELOG.md`

12. **Создать API.md с описанием API**

    - Файл: `API.md`
    - Пример содержимого:
      ```markdown
      # API

      ## Новые эндпоинты

      - `/metrics` — возвращает метрики для Prometheus
      ```
    - Команда проверки: `git add API.md`

13. **Обновить README.md**
    - Файл: `README.md`
    - Пример содержимого:
      ```markdown
      # MLOps System

      ## Мониторинг

      - Добавлены метрики для Prometheus
      ```
    - Команда проверки: `git add README.md`

## Фаза 4: Тестирование и линтеры (ДЗ 2)

14. **Запустить ruff check и ruff format**

    - Команда проверки: `ruff check services/backendrest/`

15. **Запустить pytest (если есть тесты)**

    - Команда проверки: `pytest services/backendrest/tests/`

16. **Исправить все замечания линтера**
    - Команда проверки: `ruff fix services/backendrest/`
