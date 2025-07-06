import pickle

import aio_pika
from aio_pika.abc import AbstractRobustExchange as Exchange


async def publish_msg(exchange: Exchange, payload: dict, routing_key: str):
    await exchange.publish(
        aio_pika.Message(
            body=pickle.dumps(payload),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=routing_key
    )
