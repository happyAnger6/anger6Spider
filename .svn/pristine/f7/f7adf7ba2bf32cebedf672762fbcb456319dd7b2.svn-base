__author__ = 'zhangxa'

from tornado import gen
from tornado.ioloop import IOLoop

@gen.coroutine
def cor(n,str):
    for i in range(n):
       print(str,n)
       yield gen.sleep(1)
    return str

@gen.coroutine
def main():
     a = cor(3,"first")
     b = cor(3,"second")
     print(a,b)

IOLoop.instance().run_sync(main)

