# Variables
# --------------------------------------------------------------------
ENVIRONMENT=development
APP_NAME=
COMMAND=

# Rules
# --------------------------------------------------------------------

execute:
	python manage.py $(COMMAND) --settings=config.settings.$(ENVIRONMENT)

startapp:
	python manage.py startapp $(APP_NAME)

makemigrations:
	python manage.py makemigrations --settings=config.settings.$(ENVIRONMENT);

migrate:
	python manage.py migrate --settings=config.settings.$(ENVIRONMENT);

migrations:	makemigrations migrate;

runserver:
	python manage.py runserver --settings=config.settings.$(ENVIRONMENT);

nostatic:
	python manage.py runserver --settings=config.settings.$(ENVIRONMENT) --nostatic;

pytest:
	pytest -x --cov;

cov-html:
	coverage html;

djlint:
	djlint project/templates/

djlint-format:
	djlint project/templates/ --reformat
