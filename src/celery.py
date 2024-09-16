from celery import Celery

celery_app = Celery(
    'notifications_celery',
    broker='redis://redis_broker:6379/0',
    backend='redis://redis_broker:6379/0'
)


celery_app.conf.update(
    imports=['src.tasks']
)