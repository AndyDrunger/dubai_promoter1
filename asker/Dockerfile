FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env ./

COPY my_logger.py ./
COPY classes/ ./classes/
COPY database/ ./database/
COPY rabbitmq/ ./rabbitmq/
COPY telegram/ ./telegram/

COPY asker/main.py ./

# 5. Запуск приложения
CMD ["python", "-u", "main.py"]