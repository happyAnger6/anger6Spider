__author__ = 'zhangxa'

"""
Example of coroutine displaying "Hello World":
"""
import asyncio

@asyncio.coroutine
def hello_world():
    print("hello world!")

def no_coroutine_hello_world(loop):
    print("hello world!")
    loop.stop()
#调用一个协程不会开始执行任何代码,它仅仅是一个生成器.
#返回的协程对象仅仅是一个生成器对象，在你iterator它之前，什么事情都不会发生
#Calling a coroutine does not start its code running – it is just a generator,
# and the coroutine object returned by the call is really a generator object, which doesn’t do anything until you iterate over it.
print(hello_world())

#有两种方法开始执行一个协程对象,
#在另外一个已经运行的协程里调用yield from coroutine
#或者调度它执行通过async函数或者BaseEventLoop.create_task() 方法
#In the case of a coroutine object, there are two basic ways to start it running:
# call yield from coroutine from another coroutine (assuming the other coroutine is already running!),
# or schedule its execution using the async() function or the BaseEventLoop.create_task() method.
loop = asyncio.get_event_loop()
loop.run_until_complete(hello_world())

#通过evetloop.call_sonn来调度执行一个回调函数,然后停止eventloop.
#Example using the BaseEventLoop.call_soon() method to schedule a callback. The callback displays "Hello World" and then stops the event loop:
loop.call_soon(no_coroutine_hello_world,loop)
loop.run_forever()
loop.close()