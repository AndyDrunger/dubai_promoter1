from dotenv import load_dotenv
from telethon import TelegramClient

from classes.acc import Acc

load_dotenv()



async def create_tg_client(acc: Acc) -> TelegramClient:
    client = TelegramClient(
        session=acc.string_session,
        api_id=acc.api_id,
        api_hash=acc.api_hash,
        proxy=acc.proxy.to_dict(),
    )

    return client

#
# async def get_connected_client(acc_id: int) -> TelegramClient | None:
#     client = await get_client(acc_id)
#
#     try:
#         await client.connect()
#     except Exception as e:
#         logger.warning(f"ACC_ID: {acc_id} - CANT CONNECT: {e}")
#         await DbWriter.update_acc_status(acc_id=acc_id, status='problem')
#         return None
#
#     auth = await client.is_user_authorized()
#     if not auth:
#         logger.warning(f"ACC_ID: {acc_id} - NO AUTH")
#         await client.disconnect()
#         await DbWriter.update_acc_status(acc_id=acc_id, status='blocked')
#         return None
#
#     return client
#







