export DJANGO_SETTINGS_MODULE=config.settings.product

python manage.py migrate && \
echo yes | python manage.py collectstatic && \
gunicorn --log-level=DEBUG --bind 0.0.0.0:8000 config.wsgi.product:application