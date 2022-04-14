.listen(process.env.PORT || 5000)
web: gunicorn --pythonpath main.wsgi --preload -b 0.0.0.0:8000
python manage.py runserver --settings=main.settings.production
worker: python manage.py collectstatic --noinput
web: python manage.py runserver 0.0.0.0:$PORT --noreload