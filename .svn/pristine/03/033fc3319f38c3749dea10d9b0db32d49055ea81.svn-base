__author__ = 'zhangxa'

from tornado.httputil import HTTPHeaders
import re
_charset_from_content_type_re = re.compile(r';\s*charset=(?P<charset>[^\s;]+)', re.I)
_mine_from_content_type_re = re.compile(r'text/()')

def charset_from_content(content_type):
    matched = _charset_from_content_type_re.search(content_type)
    if matched:
        # Extract the charset and strip its double quotes
        return matched.group('charset').replace('"', '')

def mine_from_content(content_type):
    splits = content_type.split("/")
    type = splits[0]
    detail = splits[1]
    for spliter in (";"," "):
        if spliter in detail:
            detail = detail.split(spliter)[0]

    return (type.lower(),detail.lower()) or None

"""
pase information from HTTPHeaders
return a dict or None
"""
def parse_headers(httpHeader):
    result = {}
    assert isinstance(httpHeader,HTTPHeaders)
    try:
        for value in httpHeader.get_all():
            if 'content-type' in value[0].lower():
                result['charset'] = charset_from_content(value[1])
    except:
        pass
    return result or None

if __name__ == "__main__":
    print(charset_from_content("text/html; charset=GBK"))
    print(charset_from_content("text/html;charset=utf-8"))
    print(mine_from_content("image/png;charset=utf-8"))
    print(mine_from_content("image/png charset=utf-8"))
    print(mine_from_content("image/jpg"))
    print(mine_from_content("Image/Png"))