__author__ = 'zhangxa'

"""
This class is almost compatible with concurrent.futures.Future.
Differences:

result() and exception() do not take a timeout argument and raise an exception when the future isn’t done yet.
Callbacks registered with add_done_callback() are always called via the event loop’s call_soon_threadsafe().
This class is not compatible with the wait() and as_completed() functions in the concurrent.futures package.
"""
import asyncio

@asyncio.coroutine
def slow_operation(future):
    yield from asyncio.sleep(1)
    future.set_result("Future is done!")

#The function that defines a coroutine (a function definition decorated with @asyncio.coroutine).
# If disambiguation is needed we will call this a coroutine function (iscoroutinefunction() returns True).
print(asyncio.iscoroutinefunction(slow_operation))

#The object obtained by calling a coroutine function. This object represents a computation or an I/O operation (usually a combination) that will complete eventually.
# If disambiguation is needed we will call it a coroutine object (iscoroutine() returns True).
print(asyncio.iscoroutine(slow_operation))

loop = asyncio.get_event_loop()
future = asyncio.Future()

print(asyncio.iscoroutine(slow_operation(future)))
asyncio.async(slow_operation(future))
loop.run_until_complete(future) #use internally the add_done_callback() method to be notified when the future is done
print(future.result)
loop.close()