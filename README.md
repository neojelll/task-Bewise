# task-Bewise

![Coveralls](https://img.shields.io/coverallsCoverage/github/neojelll/task-Bewise?style=flat-square)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/neojelll/task-Bewise/.github%2Fworkflows%2Fintegration.yml?style=flat-square)

## Установка

1. Клонируйте репозиторий командой:
	```
	git clone https://github.com/neojelll/task-Bewise
	```

2. Создайте в корневой директории файл .env по примеру .env.example заменив на свои значения

4. Запустите `docker-compose` командой:
	```
	docker-compose up -d
	```

## Use Cases

### UC-1: Создать заявку

- Цель: Создать заявку

- Описание: Пользователь отправляет POST-запрос на '/applications' с двумя параметрами

- Пример запроса:
	```
	curl -X 'POST' \
  	'http://localhost:8000/applications' \
  	-H 'accept: application/json' \
  	-H 'Content-Type: application/json' \
  	-d '{
  	"description": "<your description>",
  	"user_name": "<your user_name>"
  	}'
	```

- Результат: Пользователь получает свою заявку с новыми полями id и created_at

### UC-2: Получить список заявок

- Цель: Получить список заявок

- Описание: Пользователь отправляет GET-запрос на '/applications', также иожно указать необязательные параметры:

	1. page - номер страницы(по умолчанию = 1)

	2. size - количество записей на (странице по умолчанию = 10)

	3. user_name - при указании будет производиться поиск записей с соответствующим user_name(по умолчанию = None) (чуствителен к регистру!)

- Пример запросов:
	1. Без параметра user_name:
		```
		curl -X 'GET' \
  		'http://localhost:8000/applications?page=<your page>&size=<your size>' \
  		-H 'accept: application/json'
		```

	2. С параметром user_name:
		```
		curl -X 'GET' \
  		'http://localhost:8000/applications?page=<your page>&size=<your size>&user_name=<your user_name filter>' \
  		-H 'accept: application/json'
		```

- Результат: Пользователь получает список заявок на основе переданных им параметров

## API документация

После запуска сервиса можно перейти к документации API по ссылке:
	[API Documentation](http://localhost:8000/docs#/)
