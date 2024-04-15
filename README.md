## Backend Hacker News for vk

```
Приложение разработано с Django и Django REST Framework,
в админ-панели есть возможность добавлять новые новости и комментарии,
что полностью удовлетворяет продуктовым и техническим требованиям.

p.s за основу взят текущий набор полей у API Hacker News
```

<details>
<summary>
<strong>Настройка</strong>
</summary><br/>

  #### Создание окружения (при необходимости)
```
* python3 -m venv myenv
* source myenv/bin/activate
```

  #### Установка необходимых зависимостей
```
* pip install -r requirements.txt
```

 #### Установка и настройка PostgreSQL
```
* brew install postgresql
* brew services start postgresql
* createdb vktest
* psql postgres
* CREATE USER vktest WITH PASSWORD ‘11223344’;
* GRANT ALL PRIVILEGES ON DATABASE vktest TO vktest;
* \q
```

  #### Миграция и настройка админ-панели
```
* python manage.py migrate
* python manage.py seed_db --count=1000 --depth=3
* python manage.py createsuperuser
```

  #### Запуск сервера
```
* python manage.py runserver
```

 #### API 
```
* http://127.0.0.1:8000/api/list?page={pageId} - постраничный вывод новостей
* http://127.0.0.1:8000/api/posts/{postId} - вывод основной информации новости и первых комментариев
* http://127.0.0.1:8000/api/posts/{commentId}/replies - вывод всех ответов на комментарий
* http://127.0.0.1:8000/api/posts/{postId}/update-score/ - (POST) increment/decrement рейтинга новости
```
</details>
