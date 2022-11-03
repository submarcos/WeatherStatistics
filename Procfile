web: /opt/venv/bin/gunicorn project.wsgi:application -w 1 --bind 0.0.0.0:8000
worker: /opt/venv/bin/celery -A project worker -c 1 -l info
beat: /opt/venv/bin/celery -A project beat -l info
release: /opt/venv/bin/python ./manage.py migrate --noinput
