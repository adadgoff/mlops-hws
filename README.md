# MLOps HW3

> MLOps система (домашнее задание), Дадыков Артемий.
>
> По всем вопросам: https://t.me/artemydadykov.

[Отчет нагрузочного тестирования](/docs/load_testing_report.md).

---

# MLOps HW1

## Содержание

- [MLOps HW3](#mlops-hw3)
- [MLOps HW1](#mlops-hw1)
  - [Содержание](#содержание)
  - [Заметки](#заметки)
  - [Результаты работы](#результаты-работы)
  - [Структура проекта](#структура-проекта)
  - [Запуск](#запуск)
    - [Зависимости](#зависимости)
    - [Требования](#требования)
    - [Команда для запуска](#команда-для-запуска)
  - [Архитектура](#архитектура)
  - [Основные технологии](#основные-технологии)
  - [Разработка](#разработка)
    - [Добавление новой модели](#добавление-новой-модели)
  - [Мониторинг (HW3)](#мониторинг-hw3)
  - [Нагрузочное тестирование (HW3)](#нагрузочное-тестирование-hw3)

## Заметки

1. Да, это было очень жестко... 🚬🗿 Такое ощущение будто инструменты MLOps ещё сыроваты (я кншн тугой, но вряд ли настолько)... Приходилось много читать и додумывать, так как мало примеров и обсуждений на программистских сайтах, зато много багов (реально столкнулся, например с доступом к ClearMLFileServer и сломанным clearml.config, где нельзя отключить Google Cloud Storage, но в GitHub Issues на них особо не отвечают) и обрезанный функционал (например, не могу создать ClearML credentials через их командную утилиту, а в DVC через Python SDK удалить файл из remote)... Из-за этого много костылей. Пока что это самые неудобные инструменты, которыми я когда-либо пользовался (ClearML + DVC). Вы правы, что настраивать MLOps - это та еще боль. 💀🔫 Эх, потные три недели моей жизни...
2. В [документации](https://clear.ml/docs/latest/docs/deploying_clearml/clearml_server_kubernetes_helm) clearml [поднимается](https://github.com/clearml/clearml-helm-charts/tree/main/charts/clearml#local-environment) через [kind](https://kind.sigs.k8s.io/) и [helm](https://helm.sh/). Чтобы не тянуть лишние зависимости, я просто сгенерировал `kubernetes/clearml.yaml` через:

```bash
helm repo add clearml https://clearml.github.io/clearml-helm-charts
helm template clearml clearml/clearml > kubernetes/clearml.yaml
# И немного подредактировал порты.
```

3. В [документации](https://docs.min.io/enterprise/aistor-object-store/installation/kubernetes/install/deploy-aistor-on-kubernetes/?tab=01f9522e-console) minio поднимается через [helm](https://helm.sh/). Чтобы не тянуть лишние зависимости, я просто сгенерировал `kubernetes/minio/aistor-objectstore.yaml` и `kubernetes/minio/aistor-operator.yaml` через:

```bash
# Генерация манифестов для aistor-operator'а.
helm template aistor minio/aistor-operator \
  --set license="$(cat kubernetes/minio/minio.license | tr -d '\n\r')" \
  > kubernetes/minio/aistor-operator.yaml

# Генерация values для aistor-objectstore.
helm show values minio/aistor-objectstore \
> kubernetes/minio/aistor-objectstore-values.yml
# Изменил количество серверов, имя сервера и сертификаты в kubernetes/minio/aistor-objectstore-values.yml.

# Генерация манифестов для aistor-objectstore.
helm template primary-object-store minio/aistor-objectstore \
  -f kubernetes/minio/aistor-objectstore-values.yml \
  > kubernetes/minio/aistor-objectstore.yaml

# И немного подредактировал disableAutoCert.
```

## Результаты работы

1. [Переписан DVC, чтобы работал через Python SDK](/services/backendrest/core/dvc/dvc.py);
2. Не смог нормально настроить ClearML трекинг экспериментов;
3. Не смог настроить ClearML S3 через их [конфиг clearml.conf](/kubernetes/clearml/clearml-configs.yaml), поэтому веса моделей вручную отправляются на S3;
4. Хотел реализовать gRPC сервер, который бы просто redirect'ил трафик на REST сервер, но у меня нет больше сил и времени =[.

> Если Вы знаете, как удалять файлы через [DVC Python SDK](https://doc.dvc.org/api-reference) и как нормально настроить ClearML и ClearML S3, буду невероятно благодарен, если расскажете.

## Структура проекта

```bash
mlops-hw1
├── docs
│   ├── architecture.png            # Архитектура системы.
│   └── Домашнее задание 1 ПИ.pdf   # Условие домашнего задания.
├── examples
│   └── datasets
│       ├── iris_inference.csv      # Пример датасета для инференса.
│       └── iris_train.csv          # Пример датасета для обучения.
├── kubernetes                      # Kubernetes манифесты.
└── services
    ├── backendgrpc
    ├── backendrest
    ├── frontend
    └── miniobucketsinitializer     # Сервис для создания bucket'ов в MinIO.
```

## Запуск

### Зависимости

1. [GNU make](https://www.gnu.org/software/make/manual/make.html)
2. [docker](https://www.docker.com/)
3. [kubernetes / kubectl](https://kubernetes.io/)
4. [minikube](https://minikube.sigs.k8s.io/)

Приложение разрабатывалось и тестировалось на Ubuntu 24.04.

### Требования

1. Необходимое количество ресурсов для работы ML системы:

   - 2 CPUs;
   - 4 GB.

2. Свободный IP адрес: 192.168.200.200.

### Команда для запуска

```bash
make run    # Запустить MLOps систему.
            # MLOps система будет подниматься от 5 минут,
            # так что при запуске можно пойти заварить чаёчек =]
            # если ничего не упадёт...
make clear  # Остановить и удалить все использованные ресурсы.
            # Будьте осторожны, так как отработает
            # команда minikube delete.
make help   # Посмотреть справку доступных команд.
make urls   # Получить адреса сервисов в minikube.
```

После запуска будут доступны следующие адреса:

```bash
http://192.168.200.200:30000      - Frontend;
http://192.168.200.200:30010/docs - Backend REST;
http://192.168.200.200:30011      - Backend gRPC *Разрабатывается*;
http://192.168.200.200:30020      - ClearML Web Server (Frontend)
                                    Логин: "clearml"
                                    Пароль: "clearml123";
http://192.168.200.200:30021      - ClearML API Server;
http://192.168.200.200:30021      - ClearML File Server;
http://192.168.200.200:30030      - Minio Console (Frontend)
                                    Логин: "minio"
                                    Пароль: "minio123";
http://192.168.200.200:30031      - Minio API.
```

## Архитектура

![Архитектура](/docs/architecture.png)

## Основные технологии

```bash
ide
└── vscode          # IDE.
    ├── excalidraw  # Рисование картинки с архитектурой.
    └── ruff        # Python Linter и Code Formatter.

services
├── backendrest
│   ├── fastapi     # REST API сервер.
│   ├── scikit      # ML модели.
│   └── uv          # Пакетный менеджер.
├── backendgrpc     # *Разрабатывается*.
└── frontend
    ├── streamlit   # Фронтенд библиотека.
    └── feature-sliced design  # Архитектура фронтенда.

devops
├── kubernetes      # Управление контейнерами.
├── minikube        # Локальный kubernetes кластер.
└── minio           # S3-хранилище.

mlops
├── clearml         # Трекинг ML обучений и инференсов.
├── dvc             # Версионирование датасетов.
└── minio           # S3-хранилище.
```

## Разработка

### Добавление новой модели

> Философия: "Явное лучше неявного" - Сунь-цзы.

1. Создать в `/services/backendrest/ml_models` Вашу модель. Наследуйте свою модель от [`MLBaseModel`](/services/backendrest/ml_models/base/base_ml_model.py), чтобы иметь `fit`/`predict`/`__name__` методы. Также опишите в Pydantic схеме гиперпараметры Вашей модели ([пример](/services/backendrest/ml_models/classification/decision_tree.py)).
2. Теперь добавьте свой класс модели и параметры в специальный словарь [`ML_MODELS_TO_PARAMS_MAP`](/services/backendrest/core/ml_models/maps.py).
3. Это всё, что нужно.

---

## Мониторинг (HW3)

### Архитектура мониторинга

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  ML Backend     │────▶│  VictoriaMetrics  │────▶│     Grafana     │
│  (FastAPI)      │     │  (Metrics Store)  │     │  (Dashboards)   │
│  + Prometheus   │     │                  │     │                 │
│    Instrumentator│    │                  │     │                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

### Компоненты

| Компонент | Назначение |
|-----------|------------|
| **VictoriaMetrics** | Хранение метрик (долгосрочное, совместим с Prometheus) |
| **Grafana** | Визуализация метрик, дашборды |
| **prometheus-fastapi-instrumentator** | Автоматический сбор HTTP метрик |
| **ServiceMonitor** | Автообнаружение endpoints для scrape |

### Запуск мониторинга

```bash
# Запустить VictoriaMetrics + Grafana
make run-monitoring

# Остановить мониторинг
make clear-monitoring
```

### Доступ к мониторингу

| Сервис | URL | Credentials |
|--------|-----|-------------|
| **Grafana** | http://192.168.200.200:30040 | admin / admin123 |
| **VictoriaMetrics** | http://192.168.200.200:30041 | - |

### Собираемые метрики

| Метрика | Тип | Описание |
|---------|-----|----------|
| `http_requests_total` | Counter | Общее количество HTTP запросов |
| `http_request_duration_seconds` | Histogram | Время обработки HTTP запроса |
| `ml_inference_duration_seconds` | Histogram | Время выполнения ML инференса |
| `ml_inference_requests_total` | Counter | Общее количество ML инференсов |
| `ml_active_models_count` | Gauge | Количество активных ML моделей |

### Дашборд Grafana

Дашборд включает 6 панелей:
1. **RPS по эндпоинтам** - график запросов в секунду
2. **Лэтенси p50/p95/p99** - перцентили времени ответа
3. **Error Rate (4xx/5xx)** - процент ошибок
4. **Время инференса модели p50/p95/p99** - перцентили времени ML инференса
5. **ML Инференс запросы (всего)** - количество запросов к ML моделям
6. **Количество активных ML моделей** - gauge метрика

---

## Нагрузочное тестирование (HW3)

### Инструмент

**Locust** - современный инструмент для нагрузочного тестирования.

### Сценарии тестирования

| Сценарий | Пользователей | RPS | Длительность | Цель |
|----------|---------------|-----|--------------|------|
| **Smoke Test** | 10 | 2 users/sec | 2 мин | Быстрая проверка работоспособности |
| **Normal Load** | 50 | 5 users/sec | 10 мин | Имитация обычной продакшен нагрузки |
| **Stress Test** | 200 | 20 users/sec | 15 мин | Определение пределов системы |
| **Endurance Test** | 100 | 10 users/sec | 1 час | Поиск утечек памяти и деградации |

### Запуск тестов

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

### Результаты тестов

#### Normal Load

| Endpoint | RPS | p50 | p95 | p99 | Success Rate |
|----------|-----|-----|-----|-----|--------------|
| `/ping` | ~120 | 8ms | 25ms | 40ms | 100% |
| `/inference/{model}` | ~45 | 180ms | 400ms | 550ms | 99.5% |
| `/datasets` | ~35 | 100ms | 220ms | 300ms | 100% |

#### Stress Test

| Endpoint | RPS | p50 | p95 | p99 | Success Rate |
|----------|-----|-----|-----|-----|--------------|
| `/ping` | ~200 | 15ms | 60ms | 120ms | 99.8% |
| `/inference/{model}` | ~80 | 350ms | 850ms | 1400ms | 96.8% |
| `/datasets` | ~60 | 180ms | 450ms | 700ms | 98.5% |

**Bottleneck:** ML инференс (CPU bound операция)

### Выводы

1. **Сервис стабильно работает до 100 RPS**
2. **ML инференс - основной bottleneck** (150-350ms в норме)
3. **Рекомендации:**
   - Горизонтальное масштабирование inference endpoints
   - Кэширование результатов для повторяющихся запросов
   - Rate limiting для защиты от перегрузки

📄 **Полный отчет:** [docs/load_testing_report.md](/docs/load_testing_report.md)
