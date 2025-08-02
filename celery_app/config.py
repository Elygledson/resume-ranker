from celery import Celery
from config import settings

broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
backend_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'

app = Celery(
    'celery_app',
    broker=broker_url,
    backend=backend_url,
    include=['celery_app.tasks']
)

app.conf.update(
    result_expires=3600,
)
