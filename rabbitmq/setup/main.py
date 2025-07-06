import asyncio
import os

import aio_pika
from aio_pika.abc import AbstractRobustChannel as Channel, AbstractRobustExchange as Exchange, \
    AbstractRobustQueue as Queue
from dotenv import load_dotenv

from rabbitmq.main import get_channel

load_dotenv()

exchange_name = os.getenv("PROMO_EXCHANGE_NAME")

queues_names = ['ask', 'response', 'reaction']


async def declare_exchange(channel: Channel, name: str, ex_type=aio_pika.ExchangeType.DIRECT) -> Exchange:
    return await channel.declare_exchange(name, ex_type, durable=True)


async def declare_queue(channel: Channel, name: str) -> Queue:
    return await channel.declare_queue(name, durable=True)


async def bind_queue(queue: Queue, exchange: Exchange, routing_key: str):
    await queue.bind(exchange, routing_key=routing_key)


async def main():
    channel = await get_channel()

    promo_exchange = await declare_exchange(channel, exchange_name)

    for queue_name in queues_names:
        queue = await declare_queue(channel, queue_name)
        await bind_queue(queue, promo_exchange, queue_name)


if __name__ == "__main__":
    asyncio.run(main())
