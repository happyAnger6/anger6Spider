__author__ = 'zhangxa'

"""
Example of how to user tornado gen.coroutine
"""
from tornado import ioloop
from tornado import gen
from asyncio import Queue,QueueEmpty
from tornado.concurrent import Future

import functools

queue = Queue()

for i in range(10):
    queue.put_nowait(i)

def queue_get():
    future = Future()
    try:
        future.set_result(queue.get_nowait())
    except QueueEmpty:
        pass
    return future

@gen.coroutine
def yield_func(n):
    print("here")
    for i in range(n):
        x = yield queue_get()
        print(x)

loop = ioloop.IOLoop.current()
loop.run_sync(functools.partial(yield_func,10))
