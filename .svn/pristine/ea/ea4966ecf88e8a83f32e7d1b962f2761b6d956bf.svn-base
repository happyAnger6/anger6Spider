__author__ = 'zhangxa'

from tornado.ioloop import IOLoop

from tornado.tcpclient import TCPClient
from tornado.gen import coroutine
tcpclient = TCPClient()
ioLoop = IOLoop.current()

@coroutine
def func(n):
    for i in range(n):
        print(i)

import functools
ioLoop.run_sync(functools.partial(func,10))
