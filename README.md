# Начало работы

### 1. Установка зависимостей

`sudo apt update`

`sudo apt install git python3 docker docker-compose curl -y`

### 2. Клонируем репозиторий

`git clone https://github.com/Sergey2677/app-grafana-prometheus.git`

### 3. Запускаем проект

`docker-compose up -d --build`

`python3 ./init-grafana.py`
