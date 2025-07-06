import os

import aio_pika
from aio_pika.abc import AbstractRobustChannel as Channel


async def get_channel() -> Channel:
    conn = await aio_pika.connect_robust(
        f"amqp://{os.getenv('RABBITMQ_USER')}:{os.getenv('RABBITMQ_PASS')}@"
        f"{os.getenv('RABBITMQ_HOST')}:{os.getenv('RABBITMQ_PORT')}/"
    )
    channel = await conn.channel()
    return channel