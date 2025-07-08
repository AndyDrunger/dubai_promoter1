import asyncio
import os
import random

from aio_pika.abc import AbstractRobustExchange
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import RPCError, MessageIdInvalidError
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import Message, ReactionEmoji, Updates

from classes.acc import AccStatus
from classes.acc_chat import AccChatStatus
from classes.chat import Chat
from classes.promo_script import PromoScript
from database.crud.accs import get_accs, update_acc_status, get_acc
from database.crud.accs_chats import update_acc_chat_status
from database.crud.asks_responses import get_promo_script
from database.crud.chats import get_chat
from rabbitmq.consumer.main import consume_queue
from rabbitmq.main import get_channel
from rabbitmq.producer.main import publish_msg
from rabbitmq.setup.main import declare_exchange
from telegram.main import create_tg_client

load_dotenv()


async def startup():
    async def wrapped_main(payload: dict):
        await main(payload)

    await consume_queue(wrapped_main, queue_name=os.getenv("REACTION_QUEUE_NAME"))


async def main(payload: dict):
    chat_id, promo_script_data = parse_payload(payload)
    ask_acc_id = promo_script_data['ask_acc_id']
    response_msg_id = promo_script_data['response_msg_id']

    print(f'Chat ID: {chat_id}, Promo script: {promo_script_data}')

    acc = await get_acc(ask_acc_id)

    is_eligible = (
            acc.status == AccStatus.free
            and any(
        chat.id == chat_id and chat.status == AccChatStatus.joined
        for chat in acc.chats
    )
    )

    if not is_eligible:
        raise


    # await update_acc_status(acc_id=acc.id, status=AccStatus.working)

    chat = await load_entities(chat_id)
    client = await create_tg_client(acc)
    emoji = get_emoji()

    reaction = await send_reaction(
        client=client,
        chat=chat,
        acc_id=acc.id,
        response_msg_id=response_msg_id,
        emoji=emoji
    )

    return


def parse_payload(payload: dict) -> tuple[int, dict]:
    return payload['chat_id'], payload['promo_script']


async def load_entities(chat_id: int) -> Chat:
    chat = await get_chat(chat_id)
    return chat


async def send_reaction(client: TelegramClient, chat: Chat, acc_id: int, response_msg_id: int, emoji: str) -> Updates | None:
    try:
        await client.connect()

        reaction = await client(SendReactionRequest(
            peer='promo_SCRIPT',  # может быть ID, username или объект чата
            msg_id=response_msg_id,  # ID сообщения
            reaction=[ReactionEmoji(emoticon=emoji)],  # можно заменить на другую реакцию
        ))

    #     reaction = await client(SendReactionRequest(
    #         peer=chat.sg_id,  # может быть ID, username или объект чата
    #         msg_id=response_msg_id,  # ID сообщения
    #         reaction=[ReactionEmoji(emoticon=emoji)],  # можно заменить на другую реакцию
    #     ))
    #     await update_acc_status(acc_id=acc_id, status=AccStatus.free)
    #
    # except MessageIdInvalidError as e:
    #     # print(f'Message id invalid, acc_id: {acc_id}, chat_id: {chat.id}', e)
    #     await update_acc_status(acc_id=acc_id, status=AccStatus.free)
    #     raise

    except Exception as e:
        print(f'Cant send reaction, acc_id: {acc_id}, chat_id: {chat.id}', e)
        # await update_acc_status(acc_id=acc_id, status=AccStatus.problem)
        raise

    finally:
        await client.disconnect()

    return reaction


def get_emoji():
    emojis = ['👍', '❤', '🙏', '🫶']
    emoji = random.choice(emojis)
    return emoji


if __name__ == '__main__':
    asyncio.run(startup())