import asyncio
import os
import pickle
import traceback

import aio_pika
from dotenv import load_dotenv


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
            asyncio.create_task(process_message(message, handler_function))


async def process_message(message, handler_function):
        try:
            print('получено новое сообщение из мёртвой очереди')
            msg = pickle.loads(message.body)

            chat = msg['chat']
            promo_script = msg['promo_script']
            await handler_function(chat, promo_script, message)
        except Exception as e:
            print(f"Ошибка при обработке сообщения: {e}")
            print(traceback.format_exc())
            await message.nack(requeue=True)