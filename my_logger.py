import logging
#
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
# )
#
# logger = logging.getLogger(__name__)

# Настройка только вашего логгера
logger = logging.getLogger("my_app")  # замените на своё имя, если у вас другой логгер
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False  # отключаем проброс вверх, чтобы избежать дублирования

# Глушим сторонние библиотеки
for noisy_logger in [
    "httpx",
    "uvicorn",
    "telethon",
    "asyncio",
    "urllib3",
    "httpcore",
]:
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)