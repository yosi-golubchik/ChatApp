import json

from src.kafka import get_consumer
from src.models import Message
from src.redis import get_redis_client

if __name__ == '__main__':
    kafka_consumer = get_consumer()
    redis_client = get_redis_client()

    print("Worker started. Waiting for messages...")

    try:
        while True:
            msg = kafka_consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            try:
                parsed_message = Message(**json.loads(msg.value().decode("utf-8")))

                key = f"room_history:{parsed_message.room_id}"
                fields = {"user": parsed_message.sender_id, "msg": parsed_message.content}

                redis_client.xadd(key, fields)

                print(f"Saved to {parsed_message.room_id}: {parsed_message.content}")
            except Exception as e:
                print(f"Error processing message: {e}")
    except KeyboardInterrupt:
        print("Stopping worker...")
        kafka_consumer.close()
