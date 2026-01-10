.PHONY:         \
	help        \
	contacts    \
	check-deps  \
	check-ip    \
 	check-ports \
	run         \
	clear       \
	status      \
	urls

help: contacts
	@echo "Доступные команды:"
	@echo "  make help   - показать эту справку;"
	@echo "  make run    - запустить MLOps систему;"
	@echo "  make status - посмотреть статус MLOps системы и minikube'а;"
	@echo "  make clear  - остановить MLOps систему и удалить использованные ресурсы."
	@echo "                Будьте осторожны, так как отработает команда minikube delete;"
	@echo "  make urls   - получить адреса сервисов в minikube."

contacts:
	@echo "/-----------------------------\\"
	@echo "| MLOps HW1 © Дадыков Артемий |"
	@echo "| Контакты:                   |"
	@echo "| tg: @artemydadykov          |"
	@echo "\\-----------------------------/"

check-deps:
	@echo "Проверка зависимостей..."
	@has_errors=0; \
	which docker   > /dev/null 2>&1 || { \
		echo "ERROR: docker не установлен."; \
		has_errors=1; \
	}; \
	which kubectl  > /dev/null 2>&1 || { \
		echo "ERROR: kubectl не установлен."; \
		has_errors=1; \
	}; \
	which minikube > /dev/null 2>&1 || { \
		echo "ERROR: minikube не установлен."; \
		has_errors=1; \
	}; \
	if [ $$has_errors -eq 0 ]; then \
		echo "Проверка зависимостей завершена успешно."; \
	else \
		echo "Проверка зависимостей завершилась с ошибкой(-ами)."; \
		echo "Установите все зависимости."; \
		exit 1; \
	fi

check-ip:
	@echo "Проверка свободности IP-адреса 192.168.200.200 для minikube'а..."
	@if ping -c 1 -W 1 192.168.200.200 > /dev/null 2>&1; then \
		echo "ERROR: IP-адрес 192.168.200.200 занят."; \
		echo "Необходимо освободить IP-адрес 192.168.200.200."; \
		exit 1; \
	else \
		echo "Проверка свободности IP-адреса 192.168.200.200 для minikube'а завершилась успешно."; \
	fi

check-ports:
	@echo "Проверка портов localhost..."
	@has_errors=0; \
	lsof -i :8000 > /dev/null 2>&1 && { \
		echo "ERROR: localhost:8000 занят."; \
		has_errors=1; \
	}; \
	lsof -i :8080 > /dev/null 2>&1 && { \
		echo "ERROR: localhost:8080 занят."; \
		has_errors=1; \
	}; \
	lsof -i :8501 > /dev/null 2>&1 && { \
		echo "ERROR: localhost:8501 занят."; \
		has_errors=1; \
	}; \
	lsof -i :9443 > /dev/null 2>&1 && { \
		echo "ERROR: localhost:9443 занят."; \
		has_errors=1; \
	}; \
	lsof -i :9999 > /dev/null 2>&1 && { \
		echo "ERROR: localhost:9999 занят."; \
		has_errors=1; \
	}; \
	if [ $$has_errors -eq 0 ]; then \
		echo "Проверка портов localhost завершена успешно."; \
	else \
		echo "Проверка портов localhost завершилась с ошибкой(-ами)."; \
		echo "Порты 8000 8080 8501 9443 9999 должны быть свободны."; \
		exit 1; \
	fi

run: contacts check-deps check-ip
	@echo "Запуск MLOps системы..."


	@echo "Этап 1. Запуск minikube..."
	@minikube start --driver=docker --cpus=2 --memory=4096 --static-ip=192.168.200.200 || { \
		echo "ERROR: minikube start --driver=docker --cpus=2 --memory=4096 --static-ip=192.168.200.200 не смог запуститься"; \
		exit 1; \
	}
	@echo "Этап 1. minikube успешно запустился."


	@echo "Этап 2. Сборка локальных docker образов..."
	@minikube image build services/backendrest \
	                      -f Dockerfile        \
						  -t backendrest || {  \
		echo "ERROR: Образ services/backendrest/Dockerfile не смог собраться"; \
		exit 1; \
	}
	@minikube image build services/frontend \
	                      -f Dockerfile     \
						  -t frontend || {  \
		echo "ERROR: Образ services/frontend/Dockerfile не смог собраться"; \
		exit 1; \
	}
	@minikube image build services/miniobucketsinitializer \
	                      -f Dockerfile                    \
						  -t bucketsinitializer || {  \
		echo "ERROR: Образ services/frontend/Dockerfile не смог собраться"; \
		exit 1; \
	}
	@echo "Этап 2. Локальные docker образы успешно запустились."


	@echo "Этап 3. Применение Kubernetes манифестов..."
	@kubectl apply -f kubernetes/common/namespace.yaml || { \
		echo "ERROR: kubernetes/common/namespace.yaml не смог примениться."; \
		exit 1; \
	}

	@echo "Этап 3.1. Ожидание готовности minio pod'ов..."
	@kubectl apply -f kubernetes/minio/aistor-operator.yaml || { \
		echo "ERROR: kubernetes/minio/aistor-operator.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl apply -f kubernetes/minio/aistor-objectstore.yaml || { \
		echo "ERROR: kubernetes/minio/aistor-objectstore.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl wait objectstore/minio                             \
	              --for=jsonpath='{.status.healthStatus}'=green \
				  --namespace=mlops                             \
				  --timeout=600s || {                           \
		echo "ERROR: minio pod'ы не смогли запуститься (timeout ожидания)."; \
		exit 1; \
	}
	@kubectl apply -f kubernetes/minio/bucketsinitializer.yaml || { \
		echo "ERROR: kubernetes/minio/bucketsinitializer.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl wait job/bucketsinitializer   \
	              --for=condition=complete \
				  --namespace=mlops        \
				  --timeout=600s || {      \
		echo "ERROR: minio bucket'ы не смогли создаться (timeout ожидания)."; \
		exit 1; \
	}
	@echo "Этап 3.1. minio pod'ы готовы к работе."

	@echo "Этап 3.2. Ожидание готовности clearml pod'ов."
	@kubectl apply -f kubernetes/clearml/clearml-configs.yaml || { \
		echo "ERROR: kubernetes/clearml/clearml-configs.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl apply -f kubernetes/clearml/clearml.yaml || { \
		echo "ERROR: kubernetes/clearml/clearml.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl wait deployment/clearml-webserver \
				  --for=condition=available    \
				  --namespace=mlops            \
				  --timeout=600s || {          \
		echo "ERROR: clearml pod'ы не смогли запуститься (timeout ожидания)."; \
		exit 1; \
	}
	@echo "Этап 3.2. clearml pod'ы готовы к работе."

	@echo "Этап 3.3. Ожидание готовности backendrest pod'а..."
	@kubectl apply -f kubernetes/backendrest/backendrest.yaml || { \
		echo "ERROR: kubernetes/backendrest/backendrest.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl wait deployment/backendrest    \
				  --for=condition=available \
				  --namespace=mlops         \
				  --timeout=600s || {       \
		echo "ERROR: backendrest pod не смог запуститься (timeout ожидания)."; \
		exit 1; \
	}
	@echo "Этап 3.3. backendrest pod готов к работе..."

	@echo "Этап 3.4. Ожидание готовности frontend pod'а..."
	@kubectl apply -f kubernetes/frontend/frontend.yaml || { \
		echo "ERROR: kubernetes/frontend/frontend.yaml не смог примениться."; \
		exit 1; \
	}
	@kubectl wait deployment/frontend       \
				  --for=condition=available \
				  --namespace=mlops         \
				  --timeout=600s || {       \
		echo "ERROR: frontend pod не смог запуститься (timeout ожидания)."; \
		exit 1; \
	}
	@echo "Этап 3.4. frontend pod готов к работе..."
	
	@echo "Этап 3. Kubernetes манифесты успешно применились."

	@echo "MLOps система успешно запустилась."
	
	@make urls --no-print-directory

	@minikube service frontend --namespace=mlops > /dev/null 2>&1

status:
	@echo "Статус minikube'а:"
	@minikube status

	@echo "Запущенные pod'ы:"
	@kubectl get pod --namespace=mlops
	@echo

	@echo "Запущенные сервисы:"
	@kubectl get services --namespace=mlops

clear:
	@echo "Остановка MLOps системы..."
	@minikube stop
	@echo "MLOps система успешно остановлена."

	@echo "Удаление использованных ресурсов..."
	@minikube delete
	@echo "Использованные ресурсы успешно удалены."

urls:
	@echo "Доступные адреса:"
	@echo "http://192.168.200.200:30000      - Frontend;"
	@echo "http://192.168.200.200:30010/docs - Backend REST;"
	@echo "http://192.168.200.200:30011      - Backend gRPC *Разрабатывается*;"
	@echo "http://192.168.200.200:30020      - ClearML Web Server (Frontend)"
	@echo "                                    Логин: \"clearml\""
	@echo "                                    Пароль: \"clearml123\";"
	@echo "http://192.168.200.200:30021      - ClearML API Server;"
	@echo "http://192.168.200.200:30022      - ClearML File Server;"
	@echo "http://192.168.200.200:30030      - Minio Console (Frontend)"
	@echo "                                    Логин: \"minio\""
	@echo "                                    Пароль: \"minio123\";"
	@echo "http://192.168.200.200:30031      - Minio API."
