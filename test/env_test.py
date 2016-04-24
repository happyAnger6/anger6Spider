__author__ = 'zhangxa'

from tornado import gen
from anger6Spider.env import SpiderEnv
from tornado.ioloop import IOLoop

if __name__ == "__main__":
    @gen.coroutine
    def main():
        env = SpiderEnv("http://www.taobao.com")
        yield env.gen_env()
        print(env.env)

    IOLoop.instance().run_sync(main)