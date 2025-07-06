FROM python:3.11-slim

WORKDIR /app

# 1. Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 2. Копируем основной код
COPY .env ./
COPY main_app/response/main.py ./
COPY classes/ ./classes/
COPY rabbitmq/ ./rabbitmq/
COPY main_app/telethon/main.py ./main_app/telethon/main.py
COPY logger.py/ ./


RUN mkdir -p /app/main_app/telethon/sessions && \
    chmod -R 777 /app/main_app/telethon

#3. Копируем ВСЮ папку prisma (включая сгенерированный клиент)
COPY prisma/ ./prisma/

RUN prisma generate

# 5. Запуск приложения
CMD ["python", "-u", "main.py"]