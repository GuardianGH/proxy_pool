import json
import re

with open('test_2.html', 'r') as rf:
    file = rf.read()
    res = re.findall('<td> ?([\d\.]+) ?</td>[^<]<td> ?([\d]+)', file)
    for proxy in res:
        pro = ':'.join(proxy)
        print(pro)
