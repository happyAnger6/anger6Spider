__author__ = 'zhangxa'

import sys
import yaml
import motor
import tornado.ioloop
import tornado.web, tornado.options
from concurrent import futures

tornado.options.define("port", default=8888, help="Run server on a specific port", type=int)
tornado.options.define("host", default="localhost", help="Run server on a specific host")
tornado.options.define("url", default=None, help="Url to show in HTML")
tornado.options.define("config", default="./config.yaml", help="config file's full path")
tornado.options.parse_command_line()

if not tornado.options.options.url:
	tornado.options.options.url = "http://%s:%d" % (tornado.options.options.host, tornado.options.options.port)

setting = {
	"base_url": tornado.options.options.url,
	"template_path": "templates",
	"cookie_secret": "s3cr3tk3y",
	"config_filename": tornado.options.options.config,
	"compress_response": True,
	"xsrf_cookies": True,
	"static_path": "static",
	"download": "./download",
	"session": {
		"driver": "redis",
		"driver_settings": {
			"host": "localhost",
			"port": 6379,
			"spiderQueue": 1
		},
		"force_persistence": False,
		"cache_driver": True,
		"cookie_config": {
			"httponly": True
		},
	},
	"thread_pool": futures.ThreadPoolExecutor(4),
	"debug":True
}


config = {}
try:
	with open(setting["config_filename"], "r") as fin:
		config = yaml.load(fin)
	for k, v in config["global"].items():
		setting[k] = v
	if "session" in config:
		setting["session"]["driver_settings"] = config["session"]
except:
	print("cannot found config.yaml file")
	sys.exit(0)

# mongodb connection
# format: mongodb://user:pass@host:port/
# database name: minos

try:
	client = motor.MotorClient(config["database"]["config"])
	database = client[config["database"]["spiderQueue"]]
	setting["database"] = database
except:
	print("cannot connect mongodb, check the config.yaml")
	sys.exit(0)

application = tornado.web.Application([
	(r"^/(page/(\d+))?", "controller.main.HomeHandler"),
], **setting)

if __name__ == "__main__":
	try:
		print("main")
		application.listen(tornado.options.options.port)
		tornado.ioloop.IOLoop.instance().start()
	except:
		import traceback
		print(traceback.print_exc())
	finally:
		sys.exit(0)