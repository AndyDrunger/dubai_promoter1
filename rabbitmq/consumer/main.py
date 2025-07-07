import asyncio
import pickle
from typing import Callable, Awaitable

from aio_pika.abc import AbstractIncomingMessage

from rabbitmq.main import get_channel



async def process_msg(msg: AbstractIncomingMessage, handler_func: Callable[[dict], Awaitable]):
    async with msg.process(requeue=True):
        payload = pickle.loads(msg.body)
        await handler_func(payload)

        # await msg.ack()
        # Добавить трай эксепт. При исключении вызывать нак. при успешном трайе, ак автоматом сделается



async def consume_queue(handler_func: Callable[[dict], Awaitable], queue_name: str):
    channel = await get_channel()
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for msg in queue_iter:
            asyncio.create_task(process_msg(msg, handler_func))
