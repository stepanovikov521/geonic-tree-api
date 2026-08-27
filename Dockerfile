# 1. Берем официальный легкий образ Python
FROM python:3.11-slim

# 2. Устанавливаем переменные окружения
# PYTHONDONTWRITEBYTECODE — не создавать лишние файлы .pyc
# PYTHONUNBUFFERED — выводить логи в консоль мгновенно
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Создаем рабочую директорию внутри контейнера
WORKDIR /app

# 4. Копируем файл зависимостей и устанавливаем их
# Мы делаем это отдельно, чтобы Docker мог использовать кэш (ускоряет сборку)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь остальной код проекта в контейнер
COPY . .

# 6. Указываем порт, на котором работает FastAPI
EXPOSE 8000

# 7. Команда для запуска приложения
# Мы указываем основной файл и объект app
CMD ["uvicorn", "services.main_API_async:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

