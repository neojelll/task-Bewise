from fastapi import FastAPI, HTTPException, status, Depends
from loguru import logger

from .logger import configure_logger
from .schemas import ApplicationCreate, ApplicationsListGet
from .database import DataBase
from .message_broker_producer import MessageBrokerProducer


configure_logger()


app = FastAPI(title='task-Bewise')


@app.post('/applications', tags=['applications'])
async def create_application(application: ApplicationCreate) -> dict:
    logger.debug(f'Start post /applications endpoint with params: {application}')

    async with DataBase() as session:
        result = await session.create_application(application)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error on the service side',
        )

    async with MessageBrokerProducer() as producer:
        await producer.create_application(result)  # type: ignore

    return result


@app.get('/applications', tags=['applications'])
async def get_applications(pagin_and_filter_params: ApplicationsListGet = Depends()):
    logger.debug(
        f'Start get /applications endpoint with params: {pagin_and_filter_params}'
    )

    async with DataBase() as session:
        result = await session.get_applications(pagin_and_filter_params)

    if result is None:
        logger.error('Get /applications returned error')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Incorrect filter or error on the service side',
        )

    logger.info('Completed get /applications endpoint')
    return result
