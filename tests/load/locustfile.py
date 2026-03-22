from locust import HttpUser, task, between, events
import random
import time

class MLBackendUser(HttpUser):
    wait_time = between(1, 3)
    
    test_datasets = ["dataset_1.csv", "dataset_2.csv", "dataset_3.csv"]
    test_models = ["model_regression", "model_classification"]
    
    def on_start(self):
        self.token = None
    
    @task(3)
    def health_check(self):
        """Проверка здоровья сервиса (30% нагрузки)"""
        with self.client.get("/ping", catch_response=True) as response:
            if response.status_code == 200 and response.text == "pong":
                response.success()
            else:
                response.failure("Health check failed")
    
    @task(2)
    def get_datasets(self):
        """Получение списка датасетов (20% нагрузки)"""
        self.client.get("/api/v1/datasets", catch_response=True)
    
    @task(5)
    def ml_inference(self):
        """ML инференс - основная нагрузка (50%)"""
        model_name = random.choice(self.test_models)
        dataset_name = random.choice(self.test_datasets)
        
        start_time = time.time()
        with self.client.get(
            f"/api/v1/inference/{model_name}",
            params={"dataset_name": dataset_name},
            catch_response=True,
            name="/api/v1/inference/[model_name]"
        ) as response:
            inference_time = time.time() - start_time
            
            if response.status_code == 200:
                response.success()
                events.request.fire(
                    request_type="ML_INFERENCE",
                    name="inference_duration",
                    response_time=inference_time * 1000,
                    response_length=0,
                    exception=None
                )
            elif response.status_code == 404:
                response.success()
            else:
                response.failure(f"Unexpected status: {response.status_code}")
    
    @task(1)
    def download_dataset(self):
        """Скачивание датасета (10% нагрузки)"""
        dataset_name = random.choice(self.test_datasets)
        self.client.get(
            f"/api/v1/datasets/download/{dataset_name}",
            catch_response=True,
            name="/api/v1/datasets/download/[name]"
        )
    
    @task(1)
    def get_metrics(self):
        """Получение метрик Prometheus (10% нагрузки)"""
        self.client.get("/metrics", catch_response=True)