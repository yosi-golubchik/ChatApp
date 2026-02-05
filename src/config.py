kafka_basic_conf = {
    'bootstrap.servers': 'localhost:9092'
}
kafka_consumer_conf = {
    **kafka_basic_conf,
    "group.id": "chat_saver_group",
    "auto.offset.reset": "earliest"
}

redis_conf = {
    'host': 'localhost',
    'port': 6379
}

input_topic = 'chat-messages'