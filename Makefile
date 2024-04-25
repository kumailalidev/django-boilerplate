# Variables
# --------------------------------------------------------------------
APP_NAME=

# Rules
# --------------------------------------------------------------------

startapp:
	python manage.py startapp ${APP_NAME}

makemigrations:
	python manage.py makemigrations;

migrate:
	python manage.py migrate;

migrations:	makemigrations migrate;

runserver:
	python manage.py runserver;

runserver-prod:
	python manage.py runserver --settings=config.settings.production;

nostatic:
	python manage.py runserver --nostatic;

pytest:
	pytest -x --cov;

cov-html:
	coverage html;

djlint:
	djlint project/templates/

djlint-format:
	djlint project/templates/ --reformat
