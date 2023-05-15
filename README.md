# Начало работы

### 1. Установка зависимостей

`sudo apt update`

`sudo apt install git python3 docker docker-compose curl -y`

### 2. Вносим пользователя в группу sudo

`sudo groupadd -f docker`

`sudo usermod -aG docker $USER`

`newgrp docker`

### 3. Клонируем репозиторий

`git clone https://github.com/Sergey2677/app-grafana-prometheus.git`

### 4. Запускаем проект

`cd app-grafana-prometheus`

`docker-compose up -d --build`

`python3 ./init-grafana.py`
