import asyncio
import os
import random
from asyncio import Task

from aio_pika import Exchange
from aio_pika.abc import AbstractRobustExchange as Exchange
from dotenv import load_dotenv

from classes.chat import Chat
from classes.promo_script import PromoScript
from database.crud.asks_responses import get_promo_scripts
from database.crud.chats import get_chats
from rabbitmq.main import get_channel
from rabbitmq.producer.main import publish_msg
from rabbitmq.setup.main import declare_exchange

load_dotenv()



async def main():
    rabbitmq_channel = await get_channel()
    exchange_name = os.getenv("PROMO_EXCHANGE_NAME")
    exchange = await declare_exchange(rabbitmq_channel, exchange_name)


    chats = await get_chats()

    tasks = []
    for chat in chats:
        task = asyncio.create_task(schedule(chat.id, exchange))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def schedule(chat_id: int, exchange: Exchange):
    while True:
        min = int(os.getenv('SCHEDULER_TIMEOUT_MIN'))
        max = int(os.getenv('SCHEDULER_TIMEOUT_MAX'))
        timeout = random.randint(min, max)
        print(f'Timeout {timeout} sec for chat {chat_id}')
        await asyncio.sleep(timeout)

        promo_scrips = await get_promo_scripts()
        random_promo_script = random.choice(promo_scrips)

        payload = {
            'chat_id': chat_id,
            'promo_script_id': random_promo_script.id,
        }

        await publish_msg(payload=payload, routing_key=os.getenv('ASK_QUEUE_ROUTING_KEY'), exchange=exchange)

        return


if __name__ == '__main__':
    asyncio.run(main())