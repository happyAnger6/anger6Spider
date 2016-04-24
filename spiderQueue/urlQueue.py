__author__ = 'zhangxa'

from queue import Queue
from anger6Spider.log4s import Log4Spider

"""
A spiderQueue used to storage and fetch url
"""
class UrlQueue:
    def __init__(self):
        self.visit = Queue(1000000)
        self.visited = []

    def addUrl(self,url):
        if url in self.visited:
            pass
        else:
            self.visit.put(url)
            Log4Spider.infoLog(self,"add a url[[[",url,"]]]","current size:[[[",self.visit.qsize(),"]]]")

    def getUrl(self): #in multi process these should be improved
        url = self.visit.get()
        while url in self.visited:
            url = self.visit.get()
        self.visited.append(url)
        return url

from threading import Lock
from collections import deque
from asyncio import sleep
class LockUrlQueue:
    def __init__(self):
        self._lock = Lock()
        self.count = 0
        self.visit = deque()
        self.visited = deque()

    def addUrl(self,url):
        with self._lock:
            if url not in self.visited:
                self.count+=1
                self.visit.append(url)
        Log4Spider.debugLog(self,"add a url[[[",url,"]]]","current size:[[[",self.count,"]]]")

    def getUrl(self): #we should catch IndexError here!
        while True:
            try:
                with self._lock:
                    url = self.visit.popleft()
                    while url in self.visited:
                        url = self.visit.popleft()
            except IndexError:
                sleep(0.1)
            else:
                self.count-=1
                self.visited.append(url)
                return url

if __name__ == "__main__":
    lckQueue = LockUrlQueue()
    for i in range(10):
        lckQueue.addUrl(i)

    for i in range(10):
        print(lckQueue.getUrl())