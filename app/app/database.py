import os

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .logger import configure_logger
from .models import Application
from .schemas import ApplicationsListGet, ApplicationCreate


load_dotenv()
configure_logger()


class DataBase(object):
    def __init__(self):  # pragma: no cover
        try:
            logger.info('Initializing database session')

            database_url = (
                f'postgresql+asyncpg://'
                f'{os.environ["DB_USERNAME"]}:'
                f'{os.environ["DB_PASSWORD"]}@'
                f'{os.environ["DB_HOST"]}:'
                f'{os.environ["DB_PORT"]}/'
                f'{os.environ["DB_NAME"]}'
            )

            self.async_engine = create_async_engine(
                database_url, echo=True, future=True
            )
            self.async_session = async_sessionmaker(
                bind=self.async_engine, class_=AsyncSession, expire_on_commit=False
            )()

            logger.info('Database session initialized successfully.')
        except Exception as e:
            logger.error(
                f'Error when initializing database session: {e}, database_url: {database_url}'
            )
            raise

    async def __aenter__(self):  # pragma: no cover
        return self

    async def create_application(self, application: ApplicationCreate) -> dict | None:
        try:
            logger.debug(
                f'Start create application in database with params: {application}'
            )

            user_name = application.user_name
            description = application.description

            new_application = Application(user_name=user_name, description=description)

            self.async_session.add(new_application)
            await self.async_session.commit()
            await self.async_session.refresh(new_application)

            logger.info('Application in database created Successfully')

            return {
                'id': new_application.id,
                'user_name': user_name,
                'description': description,
                'created_at': new_application.created_at.isoformat(),
            }
        except Exception as e:
            logger.error(f'Error when create application in database: {e}')

    async def get_applications(
        self, pagin_and_filter_params: ApplicationsListGet
    ) -> dict | None:
        try:
            logger.debug(
                f'Start get_applications with params: {pagin_and_filter_params}'
            )

            page, size = pagin_and_filter_params.page, pagin_and_filter_params.size

            total_result = await self.async_session.execute(
                select(func.count()).select_from(Application)
            )
            total_items = total_result.scalar()

            query = select(Application)

            if pagin_and_filter_params.user_name:
                query = query.where(
                    Application.user_name == pagin_and_filter_params.user_name
                )

            query = query.offset((page - 1) * size).limit(size)
            result = await self.async_session.execute(query)
            applications = result.scalars().all()

            logger.info('completed get_applications')

            return {
                'page': page,
                'size': size,
                'total': total_items,
                'applications': applications,
            }
        except Exception as e:
            logger.error(f'Error when try get applications: {e}')

    async def __aexit__(self, exc_type, exc_value, traceback):  # pragma: no cover
        await self.async_session.aclose()
        logger.debug('Database session closed successfully.')
