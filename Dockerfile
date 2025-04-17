# Базовый образ Python
FROM python:3.13

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:${PATH}"
ENV POETRY_VIRTUALENVS_CREATE=false

# Создание рабочей директории
WORKDIR /app

# Копирование зависимостей и установка их
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# Копирование исходного кода
COPY . .

# Создание директории для статических файлов
RUN mkdir -p /app/staticfiles

RUN python manage.py collectstatic --noinput

# Порт для Gunicorn
EXPOSE 8000

# Команда запуска Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]