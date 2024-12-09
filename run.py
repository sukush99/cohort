import signal
import sys

from loguru import logger
from quixstreams import Application

from config import config
from src.kraken_api import KarkenWebSocketTradeAPI


def signal_handler(sig, frame):
    logger.info('Exiting gracefully and closing all connections')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def produce_trades(
    kafka_broker_address: str,
    kafka_topic_name: str,
    product_id: str = config.product_id,
) -> None:
    """
    It reads trades from the karken websocket API and saces them inmto a kafka topic

    Args:
        kafka_broker_address (str): The address of the kafka broker
        kafka_topic_name (str): The name of the kafka topic
        product_id (str): The product id to get trades for

    Returns:
        None
    """
    app = Application(broker_address=kafka_broker_address)

    topic = app.topic(name=kafka_topic_name, value_serializer='json')

    karken_api = KarkenWebSocketTradeAPI(product_id=product_id)

    logger.info(f'Producing trades to {kafka_topic_name} topic')

    with app.get_producer() as producer:
        while True:
            # get trades from the karken api
            trades = karken_api.get_trades()

            for trade in trades:
                # serialize an event using the defined topic
                message = topic.serialize(
                    key=trade.product_id,
                    value={
                        'product_id': trade.product_id,
                        'price': trade.price,
                        'quantity': trade.quantity,
                        'timestamp_ms': trade.timestamp_ms,
                    },
                )

                # produce a message into the kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(
                    f'Produced trade {trade.product_id} | {trade.price} | {trade.quantity} | {trade.timestamp_ms}'
                )
            from time import sleep

            sleep(1)


if __name__ == '__main__':
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        product_id=config.product_id,
    )
