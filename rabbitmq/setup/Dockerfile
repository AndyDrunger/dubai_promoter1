FROM python:3.11-slim

WORKDIR /app

COPY .env ./

COPY rabbitmq/ ./rabbitmq/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rabbitmq/setup/main.py ./

CMD ["python", "main.py"]