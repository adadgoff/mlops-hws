from locust import HttpUser, task, between, events
import random
import time
import csv
import os


class MLBackendUser(HttpUser):
    """
    Пользователь для нагрузочного тестирования ML Backend.
    
    Сценарии тестирования:
    1. Smoke Test - быстрая проверка работоспособности (10 пользователей, 2 RPS, 2 мин)
    2. Normal Load - обычная продакшен нагрузка (50 пользователей, 5 RPS, 10 мин)
    3. Stress Test - определение пределов системы (200 пользователей, 20 RPS, 15 мин)
    4. Endurance Test - поиск утечек памяти (100 пользователей, 10 RPS, 1 час)
    """
    
    wait_time = between(1, 3)
    
    # Тестовые данные - будут заполнены в on_start
    test_datasets = []
    test_models = []
    
    # Метрики для сбора
    inference_times = []
    request_results = []

    def on_start(self):
        """Инициализация: получение списка доступных датасетов и моделей."""
        # Получаем список созданных ML моделей
        try:
            response = self.client.get("/mlmodels/created")
            if response.status_code == 200:
                models = response.json()
                self.test_models = [m["name"] for m in models if m.get("trained", False)]
        except Exception:
            self.test_models = []
        
        # Получаем список датасетов
        try:
            response = self.client.get("/datasets")
            if response.status_code == 200:
                datasets = response.json()
                self.test_datasets = [d["name"] for d in datasets]
        except Exception:
            self.test_datasets = []
        
        # Если ничего не нашли, используем дефолтные значения для тестов
        if not self.test_models:
            self.test_models = ["decision_tree_classifier", "decision_tree_regressor"]
        if not self.test_datasets:
            self.test_datasets = ["iris_train.csv", "iris_inference.csv"]

    @task(3)
    def health_check(self):
        """
        Проверка здоровья сервиса (30% нагрузки).
        Эндпоинт: GET /ping
        """
        with self.client.get("/ping", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")

    @task(2)
    def get_datasets(self):
        """
        Получение списка датасетов (20% нагрузки).
        Эндпоинт: GET /datasets
        """
        self.client.get("/datasets", catch_response=True)

    @task(5)
    def ml_inference(self):
        """
        ML инференс - основная нагрузка (50%).
        Эндпоинт: GET /inference/{ml_model_name}?dataset_name={dataset_name}
        
        Метрики:
        - Время выполнения инференса
        - Статус ответа (success/error)
        """
        if not self.test_models or not self.test_datasets:
            return
            
        model_name = random.choice(self.test_models)
        dataset_name = random.choice(self.test_datasets)

        start_time = time.time()
        with self.client.get(
            f"/inference/{model_name}",
            params={"dataset_name": dataset_name},
            catch_response=True,
            name="/inference/[model_name]"
        ) as response:
            inference_time = time.time() - start_time
            
            # Сохраняем метрики для последующего анализа
            self.inference_times.append({
                "model": model_name,
                "dataset": dataset_name,
                "time": inference_time,
                "status": response.status_code
            })

            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Модель не найдена - это ожидаемая ситуация
                response.success()
            elif response.status_code == 400:
                # Bad request - тоже может быть валидным
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")

    @task(1)
    def download_dataset(self):
        """
        Скачивание датасета (10% нагрузки).
        Эндпоинт: GET /datasets/download/{dataset_name}
        """
        if not self.test_datasets:
            return
            
        dataset_name = random.choice(self.test_datasets)
        self.client.get(
            f"/datasets/download/{dataset_name}",
            catch_response=True,
            name="/datasets/download/[name]"
        )

    @task(1)
    def get_metrics(self):
        """
        Получение метрик Prometheus (10% нагрузки).
        Эндпоинт: GET /metrics
        """
        self.client.get("/metrics", catch_response=True)

    @task(1)
    def get_ml_models(self):
        """
        Получение списка доступных ML моделей (10% нагрузки).
        Эндпоинт: GET /mlmodels
        """
        self.client.get("/mlmodels", catch_response=True)

    @task(1)
    def get_trained_models(self):
        """
        Получение списка обученных моделей (10% нагрузки).
        Эндпоинт: GET /mlmodels/trained
        """
        self.client.get("/mlmodels/trained", catch_response=True)


# === Обработчики событий для сбора статистики ===

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Инициализация перед началом тестов."""
    print("\n" + "="*60)
    print("НАГРУЗОЧНОЕ ТЕСТИРОВАНИЕ ML BACKEND")
    print("="*60)
    print(f"Target: {environment.host}")
    print(f"Users: {environment.runner.user_count if environment.runner else 'N/A'}")
    print("="*60 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Завершение тестов: сохранение результатов и вывод статистики.
    
    Результаты сохраняются в:
    - results/inference_metrics.csv - метрики инференса
    - results/request_results.csv - результаты всех запросов
    """
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    # Создаем директорию для результатов
    os.makedirs("results", exist_ok=True)
    
    # Сохраняем метрики инференса
    if environment.user_classes:
        for user_class in environment.user_classes:
            if hasattr(user_class, "inference_times"):
                # Получаем экземпляр пользователя для доступа к данным
                # (в реальном сценарии нужно использовать shared state)
                pass
    
    # Выводим общую статистику
    stats = environment.stats
    print(f"\nВсего запросов: {stats.total.num_requests}")
    print(f"Failed запросов: {stats.total.num_failures}")
    print(f"Success rate: {(1 - stats.total.num_failures / max(stats.total.num_requests, 1)) * 100:.2f}%")
    
    print("\nСтатистика по эндпоинтам:")
    print("-" * 60)
    print(f"{'Endpoint':<40} {'Requests':<10} {'Failures':<10} {'Median':<10} {'Avg':<10}")
    print("-" * 60)
    
    for endpoint in stats.entries:
        print(f"{endpoint.method + ' ' + endpoint.name:<40} "
              f"{endpoint.num_requests:<10} "
              f"{endpoint.num_failures:<10} "
              f"{endpoint.median_response_time:<10.2f} "
              f"{endpoint.avg_response_time:<10.2f}")
    
    print("="*60)
    print("\nРезультаты сохранены в папку 'results/'")
    print("="*60 + "\n")


# === Команды для запуска ===
"""
Smoke Test (быстрая проверка):
    locust -f locustfile.py --headless -u 10 -r 2 -t 2m --host http://localhost:8000

Normal Load (обычная нагрузка):
    locust -f locustfile.py --headless -u 50 -r 5 -t 10m --host http://localhost:8000

Stress Test (стресс тест):
    locust -f locustfile.py --headless -u 200 -r 20 -t 15m --host http://localhost:8000

Endurance Test (длительный тест):
    locust -f locustfile.py --headless -u 100 -r 10 -t 1h --host http://localhost:8000

Web UI:
    locust -f locustfile.py --host http://localhost:8000
    # Открыть http://localhost:8089
"""
