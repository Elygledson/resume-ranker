from celery import Celery
from config import settings

broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
backend_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'

celery = Celery('config', broker=broker_url, backend=backend_url)

celery.conf.update(result_expires=3600)
