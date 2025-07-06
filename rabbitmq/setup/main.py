import os
import aio_pika
import asyncio
from dotenv import load_dotenv


async def setup_rabbitmq():
    await asyncio.sleep(3)
    load_dotenv()

    connection = await aio_pika.connect_robust(
        f"amqp://{os.getenv('RABBIT_USER')}:{os.getenv('RABBIT_PASS')}@"
        f"{os.getenv('RABBIT_HOST')}:{os.getenv('RABBIT_PORT')}/"
    )

    async with connection:
        channel = await connection.channel()

        # Основной обменник
        exchange = await channel.declare_exchange(
            "promo_dubai",
            aio_pika.ExchangeType.DIRECT,
            durable=True
        )

        # 1. Очередь для входящих сообщений (to_ask)
        to_ask_queue = await channel.declare_queue(
            "to_ask",
            durable=True
        )
        await to_ask_queue.bind(exchange, routing_key="to_ask")

        # 2. Очередь с TTL и DLX (ask)
        ask_queue = await channel.declare_queue(
            "ask",
            durable=True,
            arguments={
                "x-dead-letter-exchange": "ttl.dlx",
                "x-dead-letter-routing-key": "to_response"  # Важно добавить!
            }
        )
        await ask_queue.bind(exchange, routing_key="ask")

        # 3. Dead-letter exchange
        dlx_exchange = await channel.declare_exchange(
            "ttl.dlx",
            aio_pika.ExchangeType.DIRECT,  # Изменено с FANOUT на DIRECT
            durable=True
        )

        # 4. Очередь для сообщений после TTL (to_response)
        to_response_queue = await channel.declare_queue(
            "to_response",
            durable=True
        )
        await to_response_queue.bind(dlx_exchange, routing_key="to_response")

        # 5. Очередь с TTL и DLX (reaction)
        reaction_queue = await channel.declare_queue(
            "reaction",
            durable=True,
            arguments={
                "x-dead-letter-exchange": "ttl.dlx",
                "x-dead-letter-routing-key": "to_reaction"  # Важно добавить!
            }
        )
        await reaction_queue.bind(exchange, routing_key="reaction")

        # 4. Очередь для сообщений после TTL (to_response)
        to_reaction_queue = await channel.declare_queue(
            "to_reaction",
            durable=True
        )
        await to_reaction_queue.bind(dlx_exchange, routing_key="to_reaction")

        print("RabbitMQ setup completed successfully")

if __name__ == "__main__":
    asyncio.run(setup_rabbitmq())
    # Keep the container running
    # import time
    # print("Setup complete, keeping container alive...")
    # while True:
    #     time.sleep(60)