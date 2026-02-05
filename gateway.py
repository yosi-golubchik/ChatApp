from confluent_kafka import Producer
from fastapi import FastAPI, Depends

from src.config import input_topic
from src.kafka import get_producer
from src.models import Message
from src.redis import get_redis_client

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello World"}

@app.post('/send_message')
async def send_message(message: Message, producer: Producer = Depends(get_producer)):
    payload = message.model_dump_json().encode("utf-8")

    producer.produce(topic=input_topic, value=payload, key=message.room_id)
    producer.poll(0)

    return {'status': 'sent'}

@app.get("/history/{room_id}")
async def get_history(room_id: str) -> list[dict]:
    redis = get_redis_client()
    key = f"room_history:{room_id}"

    raw_messages = redis.xrange(key, min="-", max="+")

    history = []
    for msg_id, data in raw_messages:
        history.append({
            "id": msg_id,
            "sender": data.get("user"),
            "content": data.get("msg"),
            "timestamp": msg_id.split("-")[0]
        })

    return history