import os
import json

from dotenv import load_dotenv
from loguru import logger
from aiokafka import AIOKafkaProducer

from .logger import configure_logger


load_dotenv()
configure_logger()


class MessageBrokerProducer(object):
    def __init__(self):
        try:
            logger.debug('Start connecting to message broker')

            self.producer = AIOKafkaProducer(
                bootstrap_servers=f'{os.environ["BROKER_HOST"]}:{os.environ["BROKER_PORT"]}',
                value_serializer=lambda x: json.dumps(x).encode('utf-8'),
            )

            logger.info('Connected to message broker successfully')
        except Exception as e:
            logger.error(f'Error when connecting to message broker: {e}')

    async def __aenter__(self):
        try:
            logger.debug('Start broker producer')

            await self.producer.start()

            logger.info('Completed start broker producer')

            return self
        except Exception as e:
            logger.error(f'Error when start broker producer: {e}')

    async def create_application(self, application: dict):
        try:
            logger.debug(f'Send application to broker, params: {repr(application)}')

            await self.producer.send_and_wait(
                os.environ['APPLICATIONS_TOPIC_NAME'], application
            )

            logger.debug(f'Successfully send application to broker: {application}')
        except Exception as e:
            logger.error(f'Error when send application to broker: {e}')

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.producer.flush()
        await self.producer.stop()
        logger.debug('Message broker producer stop successfully')
