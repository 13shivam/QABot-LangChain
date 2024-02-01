import pydantic
from confluent_kafka import Producer
from pydantic.v1 import BaseSettings

from app.config.base_config import dotenv_path


class KafkaProducerConfig(BaseSettings):
    bootstrap_servers: str
    topic: str
    key_serializer: str = "utf-8"
    value_serializer: str = "utf-8"

    class Config:
        env_file = dotenv_path
        env_prefix = "KAFKA_PRODUCER_"
        env_file_encoding = "utf-8"


# Create an instance of the producer configuration
producer_config = KafkaProducerConfig()

producer = Producer({
    'bootstrap.servers': producer_config.bootstrap_servers,
})

