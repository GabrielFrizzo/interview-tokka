from celery import Celery
from celery.schedules import crontab

celery_app = Celery("worker", broker="redis://redis:6379/0")

celery_app.conf.beat_schedule = {
    "periodical_process_batch_imports": {
        "task": "background.tasks.periodical_process_batch_imports",
        "schedule": crontab(minute="*/2"),
    },
    "periodical_batch_job_creation": {
        "task": "background.tasks.periodical_batch_job_creation",
        "schedule": crontab(minute="*/1"),
    },
}

celery_app.autodiscover_tasks(["background.tasks"], force=True)
