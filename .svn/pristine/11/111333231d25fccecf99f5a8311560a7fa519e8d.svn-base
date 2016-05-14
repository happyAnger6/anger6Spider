__author__ = 'zhangxa'

from tornado.locks import Event
import collections

class QueueEmpty(Exception):
    pass

class QueueDriver:
    def __init__(self,**settings):
        self.settings = settings
        self._finished = Event()
        self._getters = collections.deque([])  # Futures.
        self._putters = collections.deque([])

    def over(self):
        self._finished.set()

    def save(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def put(self):
        raise NotImplementedError()

    def join(self,timeout):
        return self._finished.wait(timeout)

class QueueDriverFactory(object):
    @staticmethod
    def create_queue(driver,**settings):
        module_name = 'spiderQueue.%squeue'%driver.lower()
        module = __import__(module_name,globals(),locals(),['object'],-1)
        cls = getattr(module,'%sQueue'%driver.capitalize())
        if not 'QueueDriver' in [ base.__name__ for base in cls.__bases__ ]:
            raise InvalidQueueDriverException('%s not found in current spiderQueue driver implements '% driver)

class InvalidQueueDriverException(Exception):
    pass


