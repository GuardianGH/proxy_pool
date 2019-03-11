import json
import time

from DB.mysql_connector import OpenMySQL as conn
import requests

Schedule_Time_Wait = 30


class ProxyTimeTable:

    def __init__(self):
        self.db = conn()

    def save_proxies_count(self):
        dic = dict()

        response = requests.get("http://127.0.0.1:5010/get_all/")
        status = response.status_code
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dic['date_time'] = date_time

        count = 0

        if status == 200:
            content = response.content
            count = len(json.loads(content))
            dic['count'] = count

        else:
            print('由于连接失败，时间：%s 数据为0' % date_time)

        self.db.save_proxy_count(dic=dic)

        return date_time, count


def run():
    PTT = ProxyTimeTable()
    count_time = 1
    while True:
        date_time, count = PTT.save_proxies_count()
        time.sleep(Schedule_Time_Wait)

        print("************************  %s  %s---%s *********************" % (count_time, date_time, count))
        count_time += 1


if __name__ == "__main__":
    run()
