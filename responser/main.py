import asyncio
import os
import random

from aio_pika.abc import AbstractRobustExchange
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import RPCError
from telethon.tl.types import Message

from classes.acc import AccStatus
from classes.acc_chat import AccChatStatus
from classes.chat import Chat
from classes.promo_script import PromoScript
from database.crud.accs import get_accs, update_acc_status
from database.crud.accs_chats import update_acc_chat_status
from database.crud.asks_responses import get_promo_script
from database.crud.chats import get_chat
from my_logger import logger
from rabbitmq.consumer.main import consume_queue
from rabbitmq.main import get_channel
from rabbitmq.producer.main import publish_msg
from rabbitmq.setup.main import declare_exchange
from telegram.main import create_tg_client

load_dotenv()


async def startup():
    rabbitmq_channel = await get_channel()
    exchange_name = os.getenv("PROMO_EXCHANGE_NAME")
    exchange = await declare_exchange(rabbitmq_channel, exchange_name)

    async def wrapped_main(payload: dict):
        await main(payload, exchange)

    await consume_queue(wrapped_main, queue_name=os.getenv("RESPONSE_QUEUE_NAME"))


async def main(payload: dict, exchange: AbstractRobustExchange):
    chat_id, promo_script_data = parse_payload(payload)
    ask_acc_id = promo_script_data['ask_acc_id']

    accs = await get_accs()

    eligible_accs = [
        acc for acc in accs
        if acc.status == AccStatus.free
           and acc.id != ask_acc_id
           and any(
            chat.id == chat_id and chat.status == AccChatStatus.joined
            for chat in acc.chats
        )
    ]

    if not eligible_accs:
        raise

    acc = random.choice(eligible_accs)
    # await update_acc_status(acc_id=acc.id, status=AccStatus.working)

    chat, promo_script = await load_entities(chat_id, promo_script_data)
    client = await create_tg_client(acc)

    msg = await send_message(
        client=client,
        chat=chat,
        promo_script=promo_script,
        acc_id=acc.id
    )

    payload = {
        'chat_id': chat.id,
        'promo_script': {
            'response_msg_id': msg.id,
            'ask_acc_id': promo_script.ask_acc_id,
            'ask_msg_id': promo_script.ask_msg_id,
        },
    }

    timeout = random.randint(int(os.getenv('REACTION_TIMEOUT_MIN')), int(os.getenv('REACTION_TIMEOUT_MAX')))
    await asyncio.sleep(timeout)

    await publish_msg(
        exchange=exchange,
        payload=payload,
        routing_key=os.getenv('REACTION_QUEUE_ROUTING_KEY')
    )


def parse_payload(payload: dict) -> tuple[int, dict]:
    return payload['chat_id'], payload['promo_script']


async def load_entities(chat_id: int, promo_script_data: dict) -> tuple[Chat, PromoScript]:
    chat = await get_chat(chat_id)
    promo_script = await get_promo_script(promo_script_data['id'])
    promo_script.ask_msg_id = promo_script_data['ask_msg_id']
    promo_script.ask_acc_id = promo_script_data['ask_acc_id']
    return chat, promo_script


async def send_message(client: TelegramClient, chat: Chat, promo_script: PromoScript, acc_id: int) -> Message | None:
    try:
        await client.connect()
        msg = await client.send_message('promo_SCRIPT', reply_to=promo_script.ask_msg_id, message=promo_script.response.text)
    #     msg = await client.send_message(chat.sg_id, reply_to=promo_script.ask_msg_id, message=promo_script.response.text)
    #     await update_acc_status(acc_id=acc_id, status=AccStatus.free)
    #
    # except RPCError as e:
    #     if 'RPCError 403: CHAT_SEND_PLAIN_FORBIDDEN (caused by SendMessageRequest)' in str(e):
    #         logger.warning(f"ACC_ID: {acc_id} - CHAT_ID: {chat.id} - JOINED BUT CANT SEND MESSAGE", e)
    #         await update_acc_chat_status(acc_id=acc_id, chat_id=chat.id, status=AccChatStatus.muted)
    #         await update_acc_status(acc_id=acc_id, status=AccStatus.free)
    #
    #     elif "You can't write in this chat (caused by SendMessageRequest)" in str(e):
    #         logger.warning(f"ACC_ID: {acc_id} - CHAT_ID: {chat.id} - JOIN REQUEST NOT ACCEPTED YET", e)
    #         await update_acc_status(acc_id=acc_id, status=AccStatus.free)
    #
    #     elif 'The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it (caused by SendMessageRequest)' in str(
    #             e):
    #         logger.warning(f"ACC_ID: {acc_id} - CHAT_ID: {chat.id} - KICKED FROM CHAT", e)
    #         await update_acc_chat_status(acc_id=acc_id, chat_id=chat.id, status=AccChatStatus.kicked)
    #         await update_acc_status(acc_id=acc_id, status=AccStatus.free)
    #
    #     raise
    #
    except Exception as e:
        logger.error(f'Cant send message, acc_id: {acc_id}, chat_id: {chat.id}', e)
        # await update_acc_chat_status(acc_id=acc_id, chat_id=chat.id, status=AccChatStatus.problem)
        # await update_acc_status(acc_id=acc_id, status=AccStatus.free)
        raise

    finally:
        await client.disconnect()

    return msg


if __name__ == '__main__':
    asyncio.run(startup())