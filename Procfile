release: cd project && python manage.py migrate
web: cd project && gunicorn project.wsgi:application --bind 0.0.0.0:8000