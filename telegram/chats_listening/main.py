# Код здесь заходит в акк-мамку и хендлит все сообщения в чатах. На каждое сообщение вызывает фуннкцию из продюссер.мейн и отправляет в очередь
import asyncio
import pickle
from collections import defaultdict

from dotenv import load_dotenv

from classes.database import DbBase
from rabbitmq.consumer.main import start_rabbitmq_consumer
from rabbitmq.producer.main import send_message_to_queue

registry = defaultdict(set)

async def main():
    load_dotenv()
    await DbBase.db_connect()

    asyncio.create_task(start_rabbitmq_consumer(handler_function=add_rk_in_registry,
                                  queue_name='dubai_acc_captcha_registry_commands'))

    await listen_chats()



async def add_rk_in_registry(msg):
    unpacked_msg = pickle.loads(msg.body)

    rk = unpacked_msg['rk']
    chat_id = unpacked_msg['chat_id']

    registry[chat_id].add(rk)


async def listen_chats():
    # код который ставит хендлер на телеграм клиента, и когда хендлер срабатывает (в чате появляется новое сообщение) запускается функция

    msg = None # получили сообщение из телеграмма
    chat_id = msg.from_id
    for rk in registry[chat_id]:
        msg_body = {
            'chat_id': chat_id,
            'msg': msg,
        }
        await send_message_to_queue(msg_body=msg_body, routing_key=rk)