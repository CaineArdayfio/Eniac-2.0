celery -A app worker -l INFO --detach
celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler --detach
