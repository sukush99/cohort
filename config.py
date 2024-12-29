import os
import json
from typing import List
from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())

class Config(BaseSettings):
    kafka_broker_address: str = os.environ['KAFKA_BROKER_ADDRESS']
    kafka_topic_name: str = os.environ['KAFKA_TOPIC_NAME']
    product_id: List[str] = json.loads(os.environ['PRODUCT_ID'])  # Parse the JSON string to list

config = Config()