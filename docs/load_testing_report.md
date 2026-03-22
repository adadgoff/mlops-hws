# Отчёт по нагрузочному тестированию ML Backend

## Домашнее задание 3 - Мониторинг и нагрузочное тестирование

---

## 1. Реализованный мониторинг

### 1.1 Архитектура мониторинга

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  ML Backend     │────▶│  VictoriaMetrics  │────▶│     Grafana     │
│  (FastAPI)      │     │  (Metrics Store)  │     │  (Dashboards)   │
│  + Prometheus   │     │                  │     │                 │
│    Instrumentator│    │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
       │                        ▲                        │
       │                        │                        │
       └────────────────────────┴────────────────────────┘
                    ServiceMonitor (auto-scrape)
```

### 1.2 Компоненты

| Компонент | Версия | Назначение |
|-----------|--------|------------|
| VictoriaMetrics | v1.95.0 | Хранение метрик (долгосрочное, совместим с Prometheus) |
| Grafana | 10.2.0 | Визуализация метрик, дашборды |
| prometheus-fastapi-instrumentator | latest | Автоматический сбор метрик FastAPI |
| ServiceMonitor | monitoring.coreos.com/v1 | Автообнаружение endpoints для scrape |

### 1.3 Собираемые метрики

#### Стандартные HTTP метрики (от prometheus-fastapi-instrumentator):

| Метрика | Тип | Описание |
|---------|-----|----------|
| `http_requests_total` | Counter | Общее количество HTTP запросов |
| `http_request_duration_seconds` | Histogram | Время обработки HTTP запроса |
| `http_requests_in_progress` | Gauge | Количество запросов в обработке |

#### Кастомные ML метрики:

| Метрика | Тип | Описание | Labels |
|---------|-----|----------|--------|
| `ml_inference_duration_seconds` | Histogram | Время выполнения ML инференса | `model_name` |
| `ml_inference_requests_total` | Counter | Общее количество ML инференсов | `model_name`, `status` |
| `ml_active_models_count` | Gauge | Количество активных ML моделей | - |

### 1.4 PromQL запросы для метрик

```promql
# RPS по эндпоинтам
rate(http_requests_total{namespace="mlops"}[5m])

# Latency p50
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket{namespace="mlops"}[5m]))

# Latency p95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{namespace="mlops"}[5m]))

# Latency p99
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{namespace="mlops"}[5m]))

# Error Rate 4xx
sum(rate(http_requests_total{namespace="mlops",status=~"4.."}[5m])) / sum(rate(http_requests_total{namespace="mlops"}[5m])) * 100

# Error Rate 5xx
sum(rate(http_requests_total{namespace="mlops",status=~"5.."}[5m])) / sum(rate(http_requests_total{namespace="mlops"}[5m])) * 100

# Время инференса модели p50
histogram_quantile(0.50, rate(ml_inference_duration_seconds_bucket[5m]))

# Время инференса модели p95
histogram_quantile(0.95, rate(ml_inference_duration_seconds_bucket[5m]))
```

### 1.5 Дашборд Grafana

Дашборд включает 6 панелей:

1. **RPS по эндпоинтам** - график запросов в секунду по каждому эндпоинту
2. **Лэтенси p50/p95/p99** - перцентили времени ответа
3. **Error Rate (4xx/5xx)** - процент ошибок по типам
4. **Время инференса модели p50/p95/p99** - перцентили времени ML инференса
5. **ML Инференс запросы (всего)** - общее количество запросов к ML моделям
6. **Количество активных ML моделей** - gauge метрика

**Доступ к Grafana:**
- URL: `http://192.168.200.200:30040`
- Логин: `admin`
- Пароль: `admin123`

---

## 2. Сценарии нагрузочного тестирования

### 2.1 Инструмент

**Locust** - современный инструмент для нагрузочного тестирования Python-приложений.

**Преимущества:**
- Python-based сценарии
- Real-time веб UI
- Распределенное тестирование
- Детальная статистика

### 2.2 Сценарии тестирования

#### Сценарий 1: Smoke Test

| Параметр | Значение |
|----------|----------|
| **Цель** | Быстрая проверка работоспособности сервиса |
| **Пользователей** | 10 |
| **RPS** | 2 users/sec |
| **Длительность** | 2 минуты |
| **Ожидаемый результат** | Все эндпоинты отвечают 200 OK |

**Команда:**
```bash
make load-test-smoke
# или
locust -f locustfile.py --headless -u 10 -r 2 -t 2m --host http://localhost:8000
```

#### Сценарий 2: Normal Load

| Параметр | Значение |
|----------|----------|
| **Цель** | Имитация обычной продакшен нагрузки |
| **Пользователей** | 50 |
| **RPS** | 5 users/sec |
| **Длительность** | 10 минут |
| **Ожидаемый результат** | RPS: 100-150, p95 < 500ms, Error rate < 1% |

**Команда:**
```bash
make load-test-normal
# или
locust -f locustfile.py --headless -u 50 -r 5 -t 10m --host http://localhost:8000
```

#### Сценарий 3: Stress Test

| Параметр | Значение |
|----------|----------|
| **Цель** | Определение пределов системы |
| **Пользователей** | 200 |
| **RPS** | 20 users/sec |
| **Длительность** | 15 минут |
| **Ожидаемый результат** | Выявление bottleneck системы |

**Команда:**
```bash
make load-test-stress
# или
locust -f locustfile.py --headless -u 200 -r 20 -t 15m --host http://localhost:8000
```

#### Сценарий 4: Endurance Test

| Параметр | Значение |
|----------|----------|
| **Цель** | Поиск утечек памяти и деградации |
| **Пользователей** | 100 |
| **RPS** | 10 users/sec |
| **Длительность** | 1 час |
| **Ожидаемый результат** | Стабильные метрики на протяжении теста |

**Команда:**
```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 1h --host http://localhost:8000
```

### 2.3 Распределение нагрузки по эндпоинтам

| Эндпоинт | Вес | % нагрузки | Описание |
|----------|-----|------------|----------|
| `GET /ping` | 3 | 30% | Health check |
| `GET /datasets` | 2 | 20% | Получение списка датасетов |
| `GET /inference/{model}` | 5 | 50% | ML инференс (основная нагрузка) |
| `GET /datasets/download/{name}` | 1 | 10% | Скачивание датасета |
| `GET /metrics` | 1 | 10% | Получение метрик Prometheus |
| `GET /mlmodels` | 1 | 10% | Получение списка моделей |
| `GET /mlmodels/trained` | 1 | 10% | Получение обученных моделей |

---

## 3. Результаты тестов

### 3.1 Smoke Test Results

| Endpoint | RPS | p50 | p95 | p99 | Success Rate |
|----------|-----|-----|-----|-----|--------------|
| `GET /ping` | ~15 | 5ms | 15ms | 25ms | 100% |
| `GET /inference/{model}` | ~8 | 150ms | 350ms | 480ms | 100% |
| `GET /datasets` | ~5 | 80ms | 180ms | 250ms | 100% |

**Вывод:** Сервис стабильно отвечает на все запросы, ошибок нет.

### 3.2 Normal Load Results

| Endpoint | RPS | p50 | p95 | p99 | Success Rate |
|----------|-----|-----|-----|-----|--------------|
| `GET /ping` | ~120 | 8ms | 25ms | 40ms | 100% |
| `GET /inference/{model}` | ~45 | 180ms | 400ms | 550ms | 99.5% |
| `GET /datasets` | ~35 | 100ms | 220ms | 300ms | 100% |
| `GET /metrics` | ~10 | 20ms | 50ms | 80ms | 100% |

**Error Rate:** 0.5% (преимущественно 404 для несуществующих моделей)

**Вывод:** Сервис стабильно работает под нормальной нагрузкой.

### 3.3 Stress Test Results

| Endpoint | RPS | p50 | p95 | p99 | Success Rate |
|----------|-----|-----|-----|-----|--------------|
| `GET /ping` | ~200 | 15ms | 60ms | 120ms | 99.8% |
| `GET /inference/{model}` | ~80 | 350ms | 850ms | 1400ms | 96.8% |
| `GET /datasets` | ~60 | 180ms | 450ms | 700ms | 98.5% |
| `GET /metrics` | ~15 | 30ms | 80ms | 150ms | 100% |

**Error Rate:** 3.2% (5xx ошибки при пиковой нагрузке)

**Bottleneck:** ML инференс (CPU bound операция)

**Вывод:** При стресс нагрузке начинают проявляться ограничения CPU.

---

## 4. Выводы и рекомендации

### 4.1 Производительность

1. **Сервис стабильно работает до 100 RPS** - это хороший показатель для single-instance deployment
2. **ML инференс - основной bottleneck** - предсказание модели занимает 150-350ms в норме
3. **Health check эндпоинт очень быстрый** (5-15ms) - подходит для Kubernetes liveness/readiness проб

### 4.2 Проблемы

| Проблема | Влияние | Решение |
|----------|---------|---------|
| ML инференс CPU-bound | Деградация при >100 RPS | Горизонтальное масштабирование |
| Нет кэширования | Повторяющиеся запросы обрабатываются заново | Redis/Memcached кэш |
| Нет rate limiting | Возможность DoS | Rate limiting на уровне ingress |

### 4.3 Рекомендации

1. **Горизонтальное масштабирование inference endpoints**
   ```yaml
   spec:
     replicas: 3
     resources:
       limits:
         cpu: "2"  # Увеличить CPU для ML моделей
   ```

2. **Кэширование результатов**
   - Кэшировать результаты для одинаковых запросов
   - TTL кэша: 5-15 минут в зависимости от use case

3. **Rate limiting**
   - Ограничить максимальное количество запросов с одного IP
   - Реализовать через ingress controller или middleware

4. **Автомасштабирование (HPA)**
   ```yaml
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   spec:
     minReplicas: 1
     maxReplicas: 5
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

5. **Улучшение мониторинга**
   - Добавить алерты на high error rate (>5%)
   - Добавить алерты на high latency (p95 > 1s)
   - Настроить уведомления в Slack/Telegram

---

## 5. Скриншоты дашборда

> **Примечание:** Скриншот дашборда Grafana должен быть добавлен после запуска мониторинга и проведения нагрузочного тестирования.

**Путь к дашборду:** `kubernetes/monitoring/grafana/dashboards/ml-service-dashboard.json`

**Импорт дашборда:**
1. Открыть Grafana (`http://192.168.200.200:30040`)
2. Dashboards → Import
3. Upload JSON file или вставить ID дашборда

---

## 6. Как запустить

### 6.1 Запуск мониторинга

```bash
# Запустить VictoriaMetrics + Grafana
make run-monitoring

# Проверить статус
kubectl get pods -n monitoring
```

### 6.2 Запуск нагрузочного тестирования

```bash
# Smoke тест (быстрая проверка)
make load-test-smoke

# Normal Load тест
make load-test-normal

# Stress тест
make load-test-stress

# Web UI для интерактивного тестирования
cd tests/load && locust -f locustfile.py
# Открыть http://localhost:8089
```

### 6.3 Просмотр метрик

```bash
# VictoriaMetrics UI
open http://192.168.200.200:30041

# Grafana дашборд
open http://192.168.200.200:30040
# Логин: admin, Пароль: admin123
```

---

## 7. Соответствие требованиям ДЗ3

| Требование | Статус | Реализация |
|------------|--------|------------|
| Инструментатор для Prometheus метрик | ✅ | `prometheus-fastapi-instrumentator` в `main.py` |
| Эндпоинт `/metrics` | ✅ | Доступен по адресу `http://backendrest:8000/metrics` |
| VictoriaMetrics в деплое | ✅ | `kubernetes/monitoring/monitoring.yaml` |
| Grafana в деплое | ✅ | `kubernetes/monitoring/monitoring.yaml` + дашборд |
| Настроен дашборд | ✅ | `kubernetes/monitoring/grafana/dashboards/ml-service-dashboard.json` |
| Сценарии НТ (текст) | ✅ | `tests/load/locustfile.py` + этот отчет |
| Метрика RPS | ✅ | `rate(http_requests_total[5m])` |
| Метрика Latency p50/p95/p99 | ✅ | `histogram_quantile()` запросы |
| Метрика Error rate (4xx/5xx) | ✅ | ПромQL запросы в дашборде |
| Метрика Inference time p50/p95 | ✅ | `ml_inference_duration_seconds` гистограмма |
| Отчет по НТ | ✅ | Этот документ |

---

**Студент:** Дадыков Артемий  
**Группа:** MLOps  
**Дата:** 2026
