from confluent_kafka import Producer
from fastapi import FastAPI, Depends

from src.config import input_topic
from src.kafka import get_producer
from src.models import Message

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
