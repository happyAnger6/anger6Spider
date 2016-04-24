__author__ = 'zhangxa'

"""
Example of coroutine displaying the current date every second during 5 seconds using the sleep() function
"""

import asyncio
import datetime

@asyncio.coroutine
def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if(loop.time() + 1.0) >= end_time:
            break
        yield from asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(display_date(loop))
loop.close()