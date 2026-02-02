# 1. Берем готовый образ с Python
FROM python:3.10-slim

# 2. Внутри контейнера создаем папку для нашего кода
WORKDIR /app

# 3. Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем всё остальное из папки catalog-service в контейнер
COPY . .

EXPOSE 5000
# 5. Команда, которая запустит твой сервер при старте контейнера
CMD ["python", "server.py"]