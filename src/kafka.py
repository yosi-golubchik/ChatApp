from confluent_kafka import Producer, Consumer

from src.config import kafka_basic_conf, input_topic, kafka_consumer_conf

producer_instance = Producer(**kafka_basic_conf)

consumer_instance = Consumer(**kafka_consumer_conf)
consumer_instance.subscribe([input_topic])


def get_producer() -> Producer:
    return producer_instance


def get_consumer() -> Consumer:
    return consumer_instance
