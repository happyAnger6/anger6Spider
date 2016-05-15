__author__ = 'zhangxa'

from celery import Celery

app = Celery()
print(app.conf.CELERY_TIMEZONE)
app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='Europe/London',
)

print(app.conf.CELERY_TIMEZONE)
