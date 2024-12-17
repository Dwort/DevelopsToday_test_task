FROM python:3.11-slim

# Установка робочої директорії
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо інші файли проекту
COPY . .

# Налаштування середовища
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Запускаємо сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]