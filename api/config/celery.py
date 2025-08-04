from celery import Celery
from api.config.celery import settings

broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
backend_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'

app = Celery('config', broker=broker_url, backend=backend_url)

app.conf.update(result_expires=3600)
