__author__ = 'zhangxa'

from anger6Spider.util.logTools import log_wrap

@log_wrap("dataLog",7)
@log_wrap("errLog",6)
@log_wrap("warnLog",5)
@log_wrap("downLog",4)
@log_wrap("userLog",3)
@log_wrap("traceLog",2)
@log_wrap("infoLog",1)
@log_wrap("debugLog",0)
class Log4Spider:
    level = 0

if __name__ == "__main__":
    Log4Spider.infoLog("hello the log!","ddd","adfdf")
    info = {'粉丝': '670', '文章': '15', '字数': '41000', 'name': '丑妹', '收获喜欢': '3700', '关注': '19'}
    Log4Spider.userLog(info)