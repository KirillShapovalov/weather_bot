# weather_bot

Копируем репозиторий, внутри создаем .env файл, в котором:
- TG_TOKEN=5372114457:AAGrhSeD1eUGrKu1Ank-di5K83PWarDmPy4 - _токен нашего тг-бота_
- YA_TOKEN= - _токен для тестового тарифа API Яндекс.Погоды_

Для получения YA_TOKEN переходим по ссылке https://developer.tech.yandex.ru/services/ , оформляем тестовый доступ

Находясь в папке с проектом выполняем 
- `pip install -r requirements.txt`

для установки зависимостей

### Ngrok
Регистрируемся и выполняем установку ngrok по инструкции, получаем токен:
https://dashboard.ngrok.com/get-started/setup

В терминале выполняем:
- `./ngrok http 5000` для запуска туннеля на 5000 порте

Чтобы телеграм присылал сообщения, указываем адрес. Для этого получаем {url} — адрес вида https://32515a83.ngrok.io, который отобразился в консоли ngrok. Для создания туннеля выполняем:

- `curl --location --request POST 'https://api.telegram.org/bot5372114457:AAGrhSeD1eUGrKu1Ank-di5K83PWarDmPy4/setWebhook' --header 'Content-Type: application/json' --data-raw '{"url": {url}}'`


### Postgres
Поднимаем БД в контейнере, для этого, находясь в папке с проектом, выполняем в терминале
- `docker-compose -f postgres-compose.yml up`

Поднимается БД на 5405 порту

### Запуск

В терминале выполняем команду
- `flask run`

Запускается сервер с flask

В telegram находим нашего бота по нику @moswcovv_weather_bot и пишем ему **/start**, после чего мы получаем текущую погоду в Москве, а обратившийся пользователь добавляется в БД
