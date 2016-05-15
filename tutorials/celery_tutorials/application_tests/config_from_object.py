__author__ = 'zhangxa'

from celery import Celery

import celeryconfig

app = Celery()

"""
Using the name of a module is recomended as this means that the module doesn¡¯t need to be serialized when the prefork pool is used.
If you¡¯re experiencing configuration pickle errors then please try using the name of a module instead.
"""
#app.config_from_object('celeryconfig')
app.config_from_object(celeryconfig)

print(app.conf.CELERY_TIMEZONE)