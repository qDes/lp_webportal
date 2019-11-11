# Дипломный проект Learn Python 
http://159.69.1.71/

Проект - веб-сайт с автоматическим сбором контента из групп vk.com.

## Требования

1. python 3.7+
2. MongoDB


## Установка

```bash
pip install -r requirements.txt
```

## Запуск
В папку app проекта необходимо добавить конфигурационный файл сonfig.py с адресом базы данных (MONGO_URI).
Для работы парсера vk.com в файл .env необходимо добавить логин/пароль vk_login='login', vk_password = 'password'.
Для локального запуска проекта
```bash
./run_server.sh
```

Для запуска проекта на VPS (требуется настройка nginx,celery,redis,systemd)

```bash
./restart_serv.sh
```
