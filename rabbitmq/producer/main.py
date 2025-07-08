import pickle

import aio_pika
from aio_pika.abc import AbstractRobustExchange as Exchange


# async def publish_msg(exchange: Exchange, payload: dict, routing_key: str):
#     await exchange.publish(
#         aio_pika.Message(
#             body=pickle.dumps(payload),
#             delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
#         ),
#         routing_key=routing_key
#     )


async def publish_msg(exchange: Exchange, payload: dict, routing_key: str, ttl_sec: int | None = None):

    message = aio_pika.Message(
        body=pickle.dumps(payload),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        expiration=ttl_sec
    )

    await exchange.publish(
        message,
        routing_key=routing_key
    )