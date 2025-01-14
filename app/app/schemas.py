from datetime import datetime
from typing import List
from pydantic import BaseModel


class ApplicationCreate(BaseModel):
	user_name: str
	description: str

	class Config(object):
		json_schema_extra = {
			'example': {
				'user_name': 'John',
				'description': 'Hello, I am John. This is my example description.',
			}
		}


class ApplicationResponse(BaseModel):
	id: str
	user_name: str
	description: str
	created_at: datetime

	class Config(object):
		json_schema_extra = {
			'example': {
				'id': '123e4567-e89b-12d3-a456-426655440000',
				'user_name': 'John',
				'description': 'Hello, I am John. This is my example description.',
				'created_at': '2025-01-14T22:00:00'
			}
		}


class ApplicationsListGet(BaseModel):
	page: int 
	size: int

	class Config(object):
		json_schema_extra = {
			'example': {
				'page': 1,
				'size': 10,
			}
		}


class ApplicationsListResponse(BaseModel):
	page: int
	size: int
	total: int
	applications: List[ApplicationResponse]

	class Config(object):
		json_schema_extra = {
			'example': {
				'page': 1,
				'size': 10,
				'total': 2,
				'applications': [
					{
                        'id': '123e4567-e89b-12d3-a456-426655440000',
                        'user_name': 'John',
                        'description': 'Hello, I am John. This is my example description.',
                        'created_at': '2025-01-14T22:00:00',
                    },
                    {
                        'id': '593j4757-y89g-12d3-m456-499855440157',
                        'user_name': 'Jane',
                        'description': 'Hi, I am Jane. This is my example description.',
                        'created_at': '2025-01-14T23:00:00',
                    },
				]
			}
		}
