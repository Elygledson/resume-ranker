from celery import Celery

from settings import settings

broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
backend_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'

celery_worker = Celery(
    'celery_worker',
    broker=broker_url,
    backend=backend_url,
    include=['tasks']
)

celery_worker.conf.update(
    result_expires=3600,
)
