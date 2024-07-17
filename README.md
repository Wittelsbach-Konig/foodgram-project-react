![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
<br>

# Продуктовый помощник - FoodGram
### Описание проекта
FoodGram - это универсальный продуктовый помощник с базой всевозможных ингредиентов и рецептов. 
Позволяет публиковать рецепты, сохранять в избранное, подписываться на авторов других рецептов и скачивать список покупок в pdf-формате.
Работающий проект развернут на удалённом сервере [Yandex.cloud](https://myfoodgram.ddns.net/recipes).
Документация API [API-docs](https://myfoodgram.ddns.net/api/docs/).

Функциональность проекта:

1. Для неавторизованных пользователей просматривать готовые рецепты.
2. Для авторизованных пользователей создавать, редактировать свои рецепты, подписываться на авторов, добавлять в избранное и список покупок рецепты, скачивать в формате pdf. 
3. Для администраторов добавление запрещённых слов, полные права пользователя, изменение пароля у других пользователей, блокировка пользователей и удаление рецептов, добавление и удаление рецептов/тегов.

<details close>
<summary><h2 style="display: inline"> Инфологическая Схема базы данных </h2></summary>
Для генерации введите в виртуальном окружении следующее:

```bash
python manage.py graph_models -a > erd.dot
python manage.py graph_models -a -g -o erd.png
```

![image](https://github.com/Wittelsbach-Konig/foodgram-project-react/assets/59288516/b278d465-bc4b-4810-b712-d93975dc8dac)

</details>

## Установка

1. Клонируйте репозиторий на свой компьютер:

    ```bash
    git clone git@github.com:Wittelsbach-Konig/foodgram-project-react.git
    ```
    ```bash
    cd foodgram-project-react
    ```
2. Создайте файл .env и заполните его своими данными. Перечень данных указан в корневой директории проекта в файле .env.example.

3. Установка виртуального оркужения:
    - Перейдите в директорию backend:
    ```bash
        cd backend/
    ```
    - Выполните команды:
    ```bash
        poetry install
    ```
    ```bash
        poetry shell
    ```
    Или:
    ```bash
        python -m venv venv
    ```
    ```bash
        pip install -r requirements.txt
    ```
    ```bash
        source venv/bin/activate
    ```

### Создание Docker-образов

1.  Замените username на ваш логин на DockerHub:

    ```bash
    cd frontend
    docker build -t username/foodgram_frontend .
    cd ../backend
    docker build -t username/foodgram_backend . 
    ```

2. Загрузите образы на DockerHub:

    ```bash
    docker push username/foodgram_frontend
    docker push username/foodgram_backend
    docker push username/foodgram_gateway
    ```

### Деплой на сервере

1. Подключитесь к удаленному серверу

    ```bash
    ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера 
    ```

2. Создайте на сервере директорию foodgram через терминал

    ```bash
    mkdir foodgram
    ```

3. Установка docker compose на сервер:

    ```bash
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin
    ```

4. В директорию foodgram/ скопируйте файлы docker-compose.production.yml и .env:

    ```bash
    scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
    * path_to_SSH — путь к файлу с SSH-ключом;
    * SSH_name — имя файла с SSH-ключом (без расширения);
    * username — ваше имя пользователя на сервере;
    * server_ip — IP вашего сервера.
    ```

5. Запустите docker compose в режиме демона:

    ```bash
    sudo docker compose -f docker-compose.production.yml up -d
    ```

6. Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/:
    А также импортируйте теги и ингредиенты.

    ```bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /static/
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py csv_import
    ```

7. На сервере в редакторе nano откройте конфиг Nginx:

    ```bash
    sudo nano /etc/nginx/sites-enabled/default
    ```

8. Измените настройки location в секции server:

    ```bash
    location / {

        proxy_pass http://127.0.0.1:8000;
    }
    ```

9. Проверьте работоспособность конфига Nginx:

    ```bash
    sudo nginx -t
    ```
    Если ответ в терминале такой, значит, ошибок нет:
    ```bash
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    ```

10. Перезапускаем Nginx
    ```bash
    sudo service nginx reload
    ```

### Настройка CI/CD

1. Файл workflow уже написан. Он находится в директории

    ```bash
    foodgram-project-react/.github/workflows/main.yml
    ```

2. Для адаптации его на своем сервере добавьте секреты в GitHub Actions:

    ```bash
    DOCKER_USERNAME                # имя пользователя в DockerHub
    DOCKER_PASSWORD                # пароль пользователя в DockerHub
    HOST                           # ip_address сервера
    USER                           # имя пользователя
    SSH_KEY                        # приватный ssh-ключ (cat ~/.ssh/id_rsa)
    SSH_PASSPHRASE                 # кодовая фраза (пароль) для ssh-ключа

    TELEGRAM_TO                    # id телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
    TELEGRAM_TOKEN                 # токен бота (получить токен можно у @BotFather, /token, имя бота)
    ```

### Проверка backend с помощью postman

В директории postman-collection подробно описаны шаги к проверки логики работы api.

### Примеры некоторых запросов API

Регистрация пользователя:

```bash
   POST /api/users/
```

Получение данных своей учетной записи:

```bash
   GET /api/users/me/ 
```

Добавление подписки:

```bash
   POST /api/users/id/subscribe/
```

Обновление рецепта:
  
```bash
   PATCH /api/recipes/id/
```

Удаление рецепта из избранного:

```bash
   DELETE /api/recipes/id/favorite/
```

Получение списка ингредиентов:

```bash
   GET /api/ingredients/
```

Скачать список покупок:

```bash
   GET /api/recipes/download_shopping_cart/
```
