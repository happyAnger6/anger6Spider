__author__ = 'zhangxa'

import functools
from threading import Lock
"""
This is a decorator used to define differents log level functions
usage:
define three functions infolog,errlog,debuglog for class Log and the loglevel is 1,4,0.
@log_wrap(infolog,1)
@log_wrap(errlog,4)
@log_wrap(debuglog,0)
class Log
    level = 1
    pass
"""
def log_wrap(funcname,log_level):
    def wrap(cls):
        def log(*args):
            if not hasattr(cls,"level"):
                raise NotImplementedError
            if log_level < getattr(cls,"level"):
                return
            lockname = funcname+"_lock"
            if not hasattr(cls,lockname):
                setattr(cls,lockname,Lock())
            lock_instance = getattr(cls,lockname)

            with lock_instance:
                data_file = funcname+"_file"
                if not hasattr(cls,data_file):
                    logfile = funcname+".log"
                    setattr(cls,data_file,open(logfile,"wb"))

            log_func = getattr(cls,data_file)
            with lock_instance:
                for arg in args:
                    log_func.write(str(arg).encode("UTF-8"))
                log_func.write("\n".encode("UTF-8"))
                log_func.flush()

        if hasattr(cls,funcname):
            return cls
        setattr(cls,funcname,staticmethod(log))
        return cls

    return wrap

if __name__ == "__main__":
    @log_wrap("errlog",2)
    @log_wrap("infolog",1)
    @log_wrap("debuglog",0)
    class Log:
        level = 0


    Log.errlog("err msg!")
    Log.infolog("info msg!")
    Log.debuglog("debug msg!")
    print(Log.__dict__)