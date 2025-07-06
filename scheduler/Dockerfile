FROM python:3.11-slim

WORKDIR /app

COPY .env ./

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY rabbitmq/main.py ./rabbitmq/
COPY scheduler/main.py ./

COPY classes/ ./classes/
COPY my_logger.py/ ./
COPY database/ ./database/

CMD ["python", "main.py"]