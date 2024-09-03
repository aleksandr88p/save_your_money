# Expense Tracker API

[In English](#project-description-in-english) | [На русском](#описание-проекта-на-русском)

---

## Project Description in English

Expense Tracker API is an API for managing and tracking your expenses. The API allows you to record, analyze, and
retrieve information about your spending using natural language or audio files. The project uses modern language models
and libraries for processing requests, as well as a PostgreSQL database for storing data.

### Installation and Setup

#### 1. Clone the repository

```bash
git clone https://github.com/your-repo.git
cd your-repo
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate  # for Windows
pip install -r requirements.txt
```

### 3. Set up environment variables

#### Create a .env file in the root directory and add the following variables:

```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_URL=localhost
POSTGRES_PORT=5432
OPEN_AI_TOKEN=your_openai_token
API_HEADER_TOKEN=your_api_token
```

### 4. Create the database

#### Use the provided script to create the database tables:

```bash
python ai_api/models/create_db.py
```

## Running the Project

### 1. Start the server

#### Use uvicorn to start the project:

```bash
uvicorn ai_api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Run in the background using screen

#### If you want to run the project in the background:

```bash
screen -S expense_tracker
uvicorn ai_api.main:app --host 0.0.0.0 --port 8000 --reload
# Press Ctrl+A, then D to detach from the screen
```

## API Usage

### Main Endpoints

1. **/audio-to-text/** (POST): Converts an audio file to text.
    - **Description**: This endpoint accepts an audio file and returns the recognized text.
    - **Parameters**:
        - `user_telegram_id` (str): Telegram user ID.
        - `file` (UploadFile): The audio file to be converted.

2. **/confirm-text/** (POST): Confirms the text after conversion.
    - **Description**: Used to confirm the text after processing an audio file or manual input.
    - **Parameters**:
        - `user_telegram_id` (str): Telegram user ID.
        - `confirmation` (bool): Confirmation (True/False).

3. **/query-expenses/** (POST): Queries expense information.
    - **Description**: This endpoint accepts a text query and returns expense information.
    - **Parameters**:
        - `user_telegram_id` (str): Telegram user ID.
        - `query` (str): Natural language query.

4. **/get-temp-text/** (GET): Retrieves temporary text.
    - **Description**: Returns temporarily stored text for the specified user.
    - **Parameters**:
        - `user_telegram_id` (str): Telegram user ID.

5. **/submit-text/** (POST): Submits text for analysis and storage.
    - **Description**: This endpoint accepts text, analyzes it, and stores the data in the database.
    - **Parameters**:
        - `user_telegram_id` (str): Telegram user ID.
        - `text` (str): Text to be analyzed and stored.

### Available in Telegram Bot

API functions will be available via a Telegram bot. The bot link will be added here after development is complete.

## Technical Details

### The project is built on FastAPI and includes the following components:

- FastAPI: Web framework for creating APIs.
- SQLAlchemy: ORM for working with a PostgreSQL database.
- OpenAI: Used for natural language processing.
- Whisper: Used for converting audio to text.

All project settings are centralized in the config.py file, which makes it easy to configure and change parameters.

## Roadmap

### Future plans include:

- Optimizing API performance.
- Adding new expense analysis features.
- Implementing Docker for easier deployment.
- Expanding tests to cover all possible scenarios.

## Contacts

### If you have any questions or suggestions, contact me:

Email: [aleksandr88p@gmail.com](mailto:aleksandr88p@gmail.com)

Telegram: [@alex_pylaev](https://t.me/alex_pylaev)


---

## Описание проекта на русском

Expense Tracker API — это API для управления и отслеживания ваших расходов. API позволяет записывать, анализировать и
получать информацию о ваших тратах с использованием естественного языка или аудиофайлов. Проект использует современные
языковые модели и библиотеки для обработки запросов, а также базу данных PostgreSQL для хранения данных.

## Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-репозиторий.git
cd ваш-репозиторий
```

### 2. Создание виртуального окружения и установка зависимостей

```bash
python3 -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

#### Создайте файл .env в корне проекта и добавьте следующие переменные:

```
POSTGRES_USER=ваш_пользователь
POSTGRES_PASSWORD=ваш_пароль
POSTGRES_DB=ваша_база_данных
POSTGRES_URL=localhost
POSTGRES_PORT=5432
OPEN_AI_TOKEN=ваш_openai_token
API_HEADER_TOKEN=ваш_api_token
```

### 4. Создание базы данных

#### Используйте предоставленный скрипт для создания таблиц в базе данных:

```bash
python ai_api/models/create_db.py
```

## Запуск проекта

### 1. Запуск сервера

#### Для запуска проекта используйте uvicorn:

```bash
uvicorn ai_api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Запуск в фоновом режиме через screen

#### Если вы хотите запустить проект в фоновом режиме:

```bash
screen -S expense_tracker
uvicorn ai_api.main:app --host 0.0.0.0 --port 8000 --reload
# Нажмите Ctrl+A, затем D, чтобы отсоединиться от screen
```

## Использование API

### Основные эндпоинты

1. **/audio-to-text/** (POST): Преобразование аудиофайла в текст.
   - **Описание**: Этот эндпоинт принимает аудиофайл и возвращает распознанный текст.
   - **Параметры**:
     - `user_telegram_id` (str): Telegram ID пользователя.
     - `file` (UploadFile): Аудиофайл для преобразования.

2. **/confirm-text/** (POST): Подтверждение текста после преобразования.
   - **Описание**: Используется для подтверждения текста после обработки аудиофайла или ручного ввода.
   - **Параметры**:
     - `user_telegram_id` (str): Telegram ID пользователя.
     - `confirmation` (bool): Подтверждение (True/False).

3. **/query-expenses/** (POST): Запрос информации о расходах.
   - **Описание**: Этот эндпоинт принимает текстовый запрос и возвращает информацию о расходах.
   - **Параметры**:
     - `user_telegram_id` (str): Telegram ID пользователя.
     - `query` (str): Текстовый запрос на естественном языке.

4. **/get-temp-text/** (GET): Получение временного текста.
   - **Описание**: Возвращает временно сохраненный текст для указанного пользователя.
   - **Параметры**:
     - `user_telegram_id` (str): Telegram ID пользователя.

5. **/submit-text/** (POST): Отправка текста для анализа и сохранения.
   - **Описание**: Этот эндпоинт принимает текст, анализирует его и сохраняет данные в базе.
   - **Параметры**:
     - `user_telegram_id` (str): Telegram ID пользователя.
     - `text` (str): Текст для анализа и сохранения.

### Будет доступно в Telegram боте

Функции API будут доступны через Telegram бота. Ссылка на бота будет добавлена сюда после завершения разработки.

## Технические детали

### Проект построен на основе FastAPI и включает в себя следующие компоненты:

- FastAPI: Веб-фреймворк для создания API.
- SQLAlchemy: ORM для работы с базой данных PostgreSQL.
- OpenAI: Используется для обработки естественного языка.
- Whisper: Используется для преобразования аудио в текст.

Все настройки проекта централизованы в файле config.py, что обеспечивает легкость настройки и изменения параметров.

## Роадмап

### В будущем планируется:

- Оптимизация производительности API.
- Добавление новых возможностей анализа расходов.
- Внедрение Docker для упрощения деплоя.
- Расширение тестов для покрытия всех возможных сценариев.

## Контакты

### Если у вас есть вопросы или предложения, свяжитесь со мной:

Email: [aleksandr88p@gmail.com](mailto:aleksandr88p@gmail.com)

Telegram: [@alex_pylaev](https://t.me/alex_pylaev)


