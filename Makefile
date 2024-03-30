pytest:
	pytest -x --cov;

cov-html:
	coverage html;

makemigrations:
	python manage.py makemigrations;

migrate:
	python manage.py migrate;

migrations:	makemigrations migrate;

runserver:
	python manage.py runserver;

runserver-prod:
	python manage.py runserver --settings=config.settings.production;

whitenoise:
	python manage.py runserver --nostatic;

djlint:
	djlint project/templates/

djlint-format:
	djlint project/templates/ --reformat
