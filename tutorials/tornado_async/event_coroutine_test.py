__author__ = 'zhangxa'

from tornado.locks import Event
from tornado.ioloop import IOLoop
from tornado import gen

event = Event()

@gen.coroutine
def getter():
    for _ in range(10):
        print("event wait!")
        yield event.wait()

@gen.coroutine
def setter():
    print("event setter")
    event.set()

@gen.coroutine
def runner():
    yield [getter(), setter()]

IOLoop.current().run_sync(runner)

