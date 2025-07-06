import asyncio
import os
import pickle
from typing import Optional

import aio_pika
from aio_pika.abc import AbstractRobustChannel
from dotenv import load_dotenv

channel: Optional[AbstractRobustChannel] = None


async def send_message_to_queue(msg_body: dict, routing_key: str, ttl: Optional[int] = None):
    exchange = await channel.get_exchange('promo_dubai')

    await exchange.publish(
        aio_pika.Message(
            body=pickle.dumps(msg_body),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            expiration=ttl
        ),
        routing_key=routing_key
    )


async def start_rabbitmq_consumer(handler_function, queue_name):
    load_dotenv()

    connection = await aio_pika.connect_robust(
        f"amqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASS')}@{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}/",
        heartbeat=600
    )
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            asyncio.create_task(handler_function(message))


async def get_rabbit_channel() -> AbstractRobustChannel:
    global channel  # чтобы присвоить глобальной переменной
    load_dotenv()

    connection = await aio_pika.connect_robust(
        f"amqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASS')}@"
        f"{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}/"
    )
    channel = await connection.channel()
    return channel