from celery import Celery

celery_broker_url = 'redis://redis_broker:6379/0'
celery_backend_result = 'redis://redis_broker:6379/0'

celery_app = Celery(
    'worker',
    broker=celery_broker_url,
    backend=celery_backend_result,
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

celery_app.autodiscover_tasks(['src.crm.tasks'])