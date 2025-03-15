import os
from datetime import datetime
import time
import json


def get_metrics():
    # Получение метрик из различных источников
    
    # Метрика: Загрузка процессора
    with open('/proc/loadavg') as f:
        load_avg = f.read().strip()
    metric_1 = float(load_avg.split()[0])
    
    # Метрики: Использование памяти
    with open('/proc/meminfo') as f:
        meminfo = f.read().splitlines()
    total_memory = int(meminfo[0].split()[-2]) // 1024
    free_memory = int(meminfo[1].split()[-2]) // 1024
    used_memory = total_memory - free_memory
    metric_2 = used_memory / total_memory * 100
    
    # Метрика: Количество запущенных процессов
    processes = len(os.listdir('/proc'))
        
    return {
        'timestamp': int(time.time()),
        'load_average': metric_1,
        'total_memory': total_memory,
        'free_memory': free_memory,
        'used_memory': used_memory,
        'used_memory%': metric_2,
        'processes': processes
    }


def write_log(data):
    # Формирование имени файла на основе текущей даты
    now = datetime.now()
    log_file_name = f"/var/log/{now.strftime('%Y-%m-%d')}-awesome-monitoring.log"
    
    # Открытие файла для записи
    with open(log_file_name, 'a+') as f:
        f.write(json.dumps(data) + '\n')


if __name__ == "__main__":
    metrics_data = get_metrics()
    write_log(metrics_data)