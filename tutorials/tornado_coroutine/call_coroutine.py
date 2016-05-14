__author__ = 'zhangxa'

from tornado import gen
from tornado.ioloop import IOLoop

@gen.coroutine
def divide(x, y):
    return x / y

def bad_call():
    # This should raise a ZeroDivisionError, but it won't because
    # the coroutine is called incorrectly.
    divide(1, 0)

bad_call()