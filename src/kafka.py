from confluent_kafka import Producer

from src.config import kafka_conf

producer_instance = Producer(**kafka_conf)

def get_producer():
    return producer_instance