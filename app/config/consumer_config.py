import pydantic
from pydantic.v1 import BaseSettings

from app.config.base_config import dotenv_path


class KafkaConsumerConfig(BaseSettings):
    bootstrap_servers: str
    topic: str
    auto_offset_reset: str = "earliest"
    enable_auto_commit: bool = True
    key_deserializer: str = "utf-8"
    value_deserializer: str = "utf-8"

    class Config:
        env_file = dotenv_path
        env_prefix = "KAFKA_CONSUMER_"
        env_file_encoding = "utf-8"


# Create an instance of the consumer configuration
consumer_config = KafkaConsumerConfig()
