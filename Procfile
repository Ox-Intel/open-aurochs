release: python manage.py migrate && python manage.py clear_cache && python manage.py warm_cache
web: uvicorn aurochs.asgi:application --host 0.0.0.0 --port $PORT --workers=2
worker: celery  --app aurochs worker --beat -c 2 -Q celery
# beat: celery --app aurochs beat 
