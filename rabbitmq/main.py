import os

import aio_pika
from aio_pika.abc import AbstractRobustChannel
from dotenv import load_dotenv


async def get_rabbit_channel() -> AbstractRobustChannel:
    load_dotenv()

    connection = await aio_pika.connect_robust(
        f"amqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASS')}@"
        f"{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}/"
    )
    channel = await connection.channel()
    return channel