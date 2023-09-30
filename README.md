# budget_calculator_api
Это код моего бота в ТГ. Его основная функция - удобный учет ежедневных расходов. 
Проверить его работу можно по адресу: 
https://t.me/test_your_potential_bot

# Инструкция по развёртыванию бота
#### 1) Создние .env файлов
- /bot
```shell
TOKEN="<YOUR TELEGRAM TOKEN>"
URL='api:8000'
PASSWORD="api_default_password"
```
- /compose
```shell
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)a
DB_PORT=5432 # порт для подключения к БД
```
#### 2) Развёртывание контейнеров
- в терминале перейти в папку .../budget_calculator_api/compose
- команда:
``shell
sudo docker compose up -d
 ```
- проверить, что контейнеры запущены командой:
``shell
sudo docker ps -a
 ```


# Текущие исправления по функционалу:

1. Возможность генерации или удаления пользователських категорий. Сделать это отдельным пунктом в меню. 

2. Выбор валюты

3. Скорректировать отчеты:

    - Добавить отчет за неделю

    - Переделать отчет за месяц

4. Хранить состояние пользователя в базе данных, а не в словаре 🤡

5. Выделить класс пользователя в отдельный файл

6. Создать класс Бота и переделать обработку сообщений. 

7. Поправить docker-compose 

8. Добавить напоминание пользователю о внесении расходов через Таски в Celery.
