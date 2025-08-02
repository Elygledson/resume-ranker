import logging

from celery_app import app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.task
def analyze_resume() -> None:
    pass
