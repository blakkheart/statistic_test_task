
# 📈 Сбор статистики 📈

## Описание

Проект выполнен в качестве тестового задания в команду Trade Marketing.

Микросервис для счетчиков статистики. Сервис взаимодействует с клиентом при помощи REST API запросов.

#### API методы:

 - #### Метод сохранения статистики. Принимает на вход:
   
   -   **date**  — дата события ``str``
   -   **views**  — количество показов ``int``
   -   **clicks**  — количество кликов	``int``
   -   **cost**  — стоимость кликов (в рублях с точностью до копеек) ``float``
   
   Поля  **views**,  **clicks**  и  **cost**  — опциональные.
   
- #### Метод показа статистики. Принимает на вход:
   
   -   **from**  — дата начала периода (включительно)
   -   **to**  — дата окончания периода (включительно)
    -   **sort_by**  — сортировка по выбранному полю в ответе (опционально)
   Дата передается в формате ``YYYY-MM-DD``
  
   Отвечает статистикой, отсортированной по дате. В ответе поля:
   
   -   **date**  — дата события
   -   **views**  — количество показов
   -   **clicks**  — количество кликов
   -   **cost**  — стоимость кликов
   -   **cpc**  — cost/clicks (средняя стоимость клика)
   -   **cpm**  — cost/views * 1000 (средняя стоимость 1000 показов)
   
-  #### Метод сброса статистики
   Удаляет всю сохраненную статистику.

## Стэк технологий

-  [FastAPI](https://fastapi.tiangolo.com/)  — фреймворк.
-  [PostgreSQL](https://www.postgresql.org/)  — база данных приложения.
- [SQLAlchemy](https://www.sqlalchemy.org/)  — ORM.
- [Pydantic](https://docs.pydantic.dev/latest/)  — для сериализации.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)  — для миграций.
-  [pytest](https://docs.pytest.org/en/8.0.x/)  +  [pytest-asyncio](https://pypi.org/project/pytest-asyncio/)  — для асинхронных тестов.
- [Docker](https://www.docker.com/) — контейнеризация приложения.

## Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/blakkheart/statistic_test_task.git
```
2. Перейдите в директорию проекта:
```bash
cd statistic_test_task
```
3. Установите и активируйте виртуальное окружение:
   - Windows
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   - Linux/macOS
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Обновите [pip](https://pip.pypa.io/en/stable/):
   - Windows
   ```bash
   (venv) python -m pip install --upgrade pip
   ```
   - Linux/macOS
   ```bash
   (venv) python3 -m pip install --upgrade pip
   ```
5. Установите зависимости из файла requirements.txt:
   ```bash
   (venv) pip install -r backend/requirements.txt
   ```
Создайте и заполните файл `.env` по примеру с файлом `.env.example`, который находится в корневой директории.



## Использование  

1. Введите команду для запуска докер-контейнера:
	```bash
	docker compose up
	```
2.  Примените миграции:
	```bash
	docker compose exec backend alembic upgrade head
	```

Сервер запустится по адресу ```127.0.0.1:8000```
Вы можете посмотреть документацию по адресу ```127.0.0.1:8000/docs```




### Дополнительно
Также можно прогнать тесты с помощью команды:
```bash
	docker compose exec backend pytest
```
