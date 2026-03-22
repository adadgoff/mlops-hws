#!/bin/bash

SCENARIO=${1:-normal_load}
HOST=${2:-http://localhost:8000}

echo "🚀 Запуск нагрузочного теста: $SCENARIO"
echo "📍 Target: $HOST"

case $SCENARIO in
    smoke_test)
        locust -f locustfile.py --headless -u 10 -r 2 --run-time 2m --host $HOST
        ;;
    normal_load)
        locust -f locustfile.py --headless -u 50 -r 5 --run-time 10m --host $HOST
        ;;
    stress_test)
        locust -f locustfile.py --headless -u 200 -r 20 --run-time 15m --host $HOST
        ;;
    endurance_test)
        locust -f locustfile.py --headless -u 100 -r 10 --run-time 1h --host $HOST
        ;;
    *)
        echo "❌ Неизвестный сценарий: $SCENARIO"
        echo "Доступные: smoke_test, normal_load, stress_test, endurance_test"
        exit 1
        ;;
esac

echo "✅ Тест завершён"