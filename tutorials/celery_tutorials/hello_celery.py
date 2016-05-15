__author__ = 'zhangxa'

from celery import Celery

app = Celery('hello',broker='redis://localhost:6379/0')

@app.task
def hello():
    return 'hello celery'
