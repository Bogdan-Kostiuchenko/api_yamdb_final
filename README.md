# REST API для сервиса YaMDb


**YaMDb** - собирает отзывы пользователей на произведения. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Реализованы возможности
Аутентификация по JWT-токену  

Пользователи:получение списка всех пользователей, создание пользователя, получение данных пользователя, изменение данных пользователя, удаление пользователя, получение данных своей учетной записи, изменение данных своей учетной записи

Произведения:получение списка всех произведений, добавление произведения, получение информации о произведении, обновление информации о произведении, удаление произведения

Категории произведений:получение списка всех категорий, создание категории, удаление категории

Жанры произведений: одно произведение может быть привязано к нескольким жанрам,получение списка всех жанров, создание жанра, удаление жанра

Отзывы на произведения:получение списка всех отзывов, создание отзыва, получение отзыва, обновление отзыва, удаление отзыва

Комментарии к отзывам:получение списка всех комментариев к отзыву, создание комментария для отзыва, получение комментария для отзыва, обновление комментария к отзыву, удаление комментария к отзыву


## Технологии

Python 3.9, Django 3.2, DRF, JWT

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Izyapa/api_yamdb.git
cd yatube_api
```

Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
Если у вас Linux/macOS
```
source env/bin/activate
```
Если у вас windows
```
source env/scripts/activate
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Перейти в директорию с db.sqlite3 и подключиться к ней:
```
sqlite3 db.sqlite3
```
Загрузить тестовые данные:
```
.mode csv
.separator ","
.import static/data/category.csv api_genre
.import static/data/comments.csv api_genre
.import static/data/genre_title.csv api_genre
.import static/data/genre.csv api_genre
.import static/data/review.csv api_genre
.import static/data/titles.csv api_genre
.import static/data/users.csv api_genre
```
Запустить проект:
```
python3 manage.py runserver
```

## Документация
Когда вы запустите проект, [документация для API Yatube](http://127.0.0.1:8000/redoc/) будет доступна по адресу http://127.0.0.1:8000/redoc/. В документации описано, как должен работать API. Документация представлена в формате Redoc.

## Примеры запросов:
Получение списка всех категорий
GET http://127.0.0.1:8000/api/v1/categories/


Ответ:

```json
[
  {
    "count": 1,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
Добавление комментария к отзыву, доступно аутентифицированным пользователям.
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/

```json
{
  "text": "string"
}
```
Ответ:
```json
{
  "id": 1,
  "text": "string",
  "author": "string",
  "pub_date": "2024-08-24T14:120:22Z"
}
```

## Об авторах

[Молодцова Светлана Павловна](https://github.com/SMolodtsova13)
[Асалиев Ислам](https://github.com/Izyapa)
[Костюченко Богдан](https://github.com/Bogdan-Kostiuchenko)
