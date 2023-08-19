# hs-test-work
### Тестовое задание. Реализация реферальной системы.
##### Стэк
Django, Django REST Framework, drf-spectacular, gunicorn, redis, docker, docker-compose, postgresql
##### Установка
В папке с проектом открыть терминал и запустить контейнеры командой
```sh
docker-compose up -d
```

##### Описание запросов API
По умолчанию сервером считается localhost на 80 порту.
```sh
GET http://localhost/api/docs/ - документация Redoc.
POST http://localhost/api/auth/number/ - отправить номер телефона и получить код подтверждения.
POST http://localhost/api/auth/register/ - отправить номер телефона + код подтверждения. Получить токен.
GET http://localhost/api/users/ - посмотреть список всех пользователей. Доступно только авторизованному пользователю.
PATCH http://localhost/api/users/{phone_number}/ - активировать реферальный код. Доступно только авторизованному пользователю.
GET http://localhost/api/users/me/ - посмотреть информацию о текущем авторизованном пользователе. Показывается инвайт-код.
```
Более подробную информацию о запросах можно увидеть в документации Redoc, которая была создана при помощи библиотеки drf-spectacular.
