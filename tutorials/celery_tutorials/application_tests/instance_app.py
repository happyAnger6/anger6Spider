__author__ = 'zhangxa'

"""
在使用Celery库之前必须先实例化，这个实例被称为application（或者简称app）

application是线程安全的，多个Celery application采用不同的配置和组件，
"""
from celery import Celery

app = Celery()
print(app.conf.CELERY_TIMEZONE)
