import asyncio
import os
import random

from aio_pika.abc import AbstractIncomingMessage
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import MessageIdInvalidError, RPCError
from telethon.tl.types import Message

from classes.database import DbBase, DbReader, DbWriter
from classes.other import PromoScript, Chat
from logger import logger
from main_app.telethon.main import get_connected_client
from rabbitmq.consumer.main import start_rabbitmq_consumer
from rabbitmq.producer.main import send_message_to_queue, get_rabbit_channel


async def main():
    load_dotenv()
    await DbBase.db_connect()
    await get_rabbit_channel()
    await start_rabbitmq_consumer(send_response, queue_name='to_response')


async def send_response(chat: Chat, promo_script: PromoScript, rabbit_msg: AbstractIncomingMessage):
    joined_acc_ids = await DbReader.get_joined_or_requested_acc_ids(chat.id)
    free_acc_ids = await DbReader.get_free_acc_ids()
    if not joined_acc_ids or not free_acc_ids:
        await asyncio.sleep(100)
        await rabbit_msg.nack()
        return

    common_ids = list(set(joined_acc_ids) & set(free_acc_ids))
    if promo_script.ask_acc_id in common_ids:
        common_ids.remove(promo_script.ask_acc_id)

    if not common_ids:
        await asyncio.sleep(100)
        await rabbit_msg.nack()
        return
    acc_id = random.choice(common_ids)

    await DbWriter.update_acc_status(acc_id=acc_id, status='working')

    client = await get_connected_client(acc_id)
    if not client:
        await DbWriter.update_acc_status(acc_id=acc_id, status='problem')
        await asyncio.sleep(100)
        await rabbit_msg.nack()
        return

    response_msg = await send_message(client=client, chat=chat, text=promo_script.response_text,
                       reply_to_msg_id=promo_script.ask_msg_id, acc_id=acc_id)
    if not response_msg:
        await asyncio.sleep(100)
        await rabbit_msg.nack()
        return

    await DbWriter.update_acc_status(acc_id=acc_id, status='free')

    promo_script.response_acc_id = acc_id
    promo_script.response_msg_id = response_msg.id
    rabbit_msg_body = {
        'chat': chat,
        'promo_script': promo_script,
    }

    ttl = random.randint(int(os.getenv('BEFORE_RESPONSE_TIMEOUT_MIN')), int(os.getenv('BEFORE_RESPONSE_TIMEOUT_MAX')))
    await send_message_to_queue(msg_body=rabbit_msg_body, routing_key='reaction', ttl=ttl)

    await rabbit_msg.ack()


async def send_message(client: TelegramClient, chat: Chat, text: str, acc_id: int, reply_to_msg_id: int) -> Message | None:
    try:
        sg_id = int(f'-100{chat.id}')
        msg = await client.send_message(sg_id, text, reply_to=reply_to_msg_id)
        await asyncio.sleep(random.randint(1, 10))
        my_chat_msg = await client.send_message(-1002637664833, get_link_on_message(chat, msg.id))
        await DbWriter.update_acc_status(acc_id=acc_id, status='free')
        await client.disconnect()
        return msg

    except MessageIdInvalidError as e:
        print(f'Message id invalid, acc_id: {acc_id}, chat_id: {chat.id}', e)
        await DbWriter.update_acc_status(acc_id=acc_id, status='free')
        msg = None

    except RPCError as e:
        if 'RPCError 403: CHAT_SEND_PLAIN_FORBIDDEN (caused by SendMessageRequest)' in str(e):
            logger.warning(f"ACC_ID: {acc_id} - CHAT_ID: {chat.id} - JOINED BUT CANT SEND MESSAGE", e)
            await DbWriter.update_acc_chats_status(acc_id=acc_id, chat_id=chat.id, status='muted')
            await DbWriter.update_acc_status(acc_id=acc_id, status='free')

        elif "You can't write in this chat (caused by SendMessageRequest)" in str(e):
            logger.warning(f"ACC_ID: {acc_id} - CHAT_ID: {chat.id} - JOIN REQUEST NOT ACCEPTED YET", e)
            await DbWriter.update_acc_status(acc_id=acc_id, status='free')

        elif 'The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it (caused by SendMessageRequest)' in str(e):
            logger.warning(f"ACC_ID: {acc_id} - CHAT_ID: {chat.id} - KICKED FROM CHAT", e)
            await DbWriter.update_acc_chats_status(acc_id=acc_id, chat_id=chat.id, status='kicked')
            await DbWriter.update_acc_status(acc_id=acc_id, status='free')

        msg = None

    except Exception as e:
        logger.error(f'Cant send answer, acc_id: {acc_id}, chat_id: {chat.id}', e)
        await DbWriter.update_acc_status(acc_id=acc_id, status='problem')
        msg = None
    finally:
        await client.disconnect()

    return msg


def get_link_on_message(chat: Chat, message_id: int):
    if chat.username:
        return f'https://t.me/{chat.username}/{message_id}'
    elif not chat.username:
        return f'https://t.me/c/{chat.id}/{message_id}'


if __name__ == '__main__':
    asyncio.run(main())