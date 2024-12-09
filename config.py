import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Config(BaseSettings):
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic_name: str = os.environ['KAFKA_TOPIC_NAME']
    product_id: str = os.environ['PRODUCT_ID']


config = Config()
