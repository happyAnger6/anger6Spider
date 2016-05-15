__author__ = 'zhangxa'

import re

re_price = re.compile(r"[\d\.]{1,}")
price="$90.0"

print(re_price.search(price).group())
