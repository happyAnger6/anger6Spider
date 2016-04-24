__author__ = 'zhangxa'

import re

from tornado.web import URLSpec
from anger6Spider.log4s import Log4Spider

"""
  A dictionary may be passed as the third element of the tuple,
    which will be used as keyword arguments to the handler's
    constructor and `BaseSpider.initialize` method.
     application = web.Application([
            (r"/www.test.com/(.*)", anger6Spider.spiders.spider.BaseSpider, {"path": "/var/www"}),
        ])
"""
class Application:
    def __init__(self, handlers=None,
                 **settings):
        self.handlers = []
        self.named_handlers = {}
        self.settings = settings
        if handlers:
            for handler in handlers:
                self.add_handler(handler)

    def add_handler(self,url_handler):
        """Appends the given url_handlers to our handler list.
        """
        print(url_handler)
        url_pattern = url_handler[0]
        if not url_pattern.endswith("$"):
            url_pattern+="$"
        handlers = []
        #wildcard .*$ should have lowest priority
        #notice:first we only insert a empty handlers as a placeholder
        if self.handlers and self.handlers[-1][0].pattern == '.*$':
            self.handlers.insert(-1,(re.compile(url_pattern),handlers))
        else:
            self.handlers.append((re.compile(url_pattern),handlers))

        spec = url_handler
        if isinstance(spec,(tuple,list)): #the url_handler should be inited with some args
            assert len(spec) in (2,3,4)
            spec = URLSpec(*spec)
        handlers.append(spec)
        if spec.name:
            if spec.name and self.named_handlers:
                Log4Spider.warnLog(
                    "Multiple handlers named %s; replacing previous value",
                    spec.name
                )
            self.named_handlers[spec.name] = spec

    def _get_url_handler(self,url):
        matches = []
        for pattern,handlers in self.handlers:
            if pattern.match(url):
                matches.extend(handlers)
        return matches or None


if __name__ == "__main__":
    app = Application([
        (r"^http://www.baidu.com.*$", "anger6Spider.spiders.spider.BaseSpider"),
        (r"^http://www.jianshu.com.*$", "anger6Spider.spiders.spider.UrlSeekSpider"),
    ])
    print("handlers:",app.handlers)
    print("h1:",app._get_url_handler("http://www.baidu.com"))
    print("h2:",app._get_url_handler("http://www.jianshu.com"))


