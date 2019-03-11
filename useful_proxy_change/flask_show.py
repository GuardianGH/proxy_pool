# -*- coding: utf-8 -*-
# !/usr/bin/env python
import sys
import time
from DB.schedul import Schedule_Time_Wait as STW
from flask import Flask, render_template
from DB.mysql_connector import OpenMySQL as conn

sys.path.append('../')

app = Flask(__name__)
app.jinja_env.auto_reload = True
db = conn()

X_Axis_Span = 10  # 设置图表的x轴跨度，单位分钟


def get_data(flag):
    data = db.select_all(sql="""select date_time, count from proxy_time_table;""", db="proxy")

    point_num = X_Axis_Span * 60 // STW

    if data:
        if flag == 1:
            datetime = []
            count = []
            dic = dict()
            for i in data:
                datetime.append(str(i.get("date_time")))
                count.append(str(i.get("count")))
            dic["date_time"] = datetime
            dic["count"] = count
            return dic
        elif flag == 2:
            new_list = [[x.get('date_time'), str(x.get('count'))] for x in data]
            count = 1
            num_list = list()
            lis_for_count = list()
            for p in new_list:
                tem_num = 0
                tem_date = p[0]
                if len(lis_for_count) < point_num:
                    tem_num += int(p[1])
                    lis_for_count.append(tem_num)
                else:
                    num_avg = sum(lis_for_count) // len(lis_for_count)
                    date = tem_date
                    num_list.append([date, str(num_avg)])
                    lis_for_count = list()
                count += 1
            return num_list
        elif flag == 3:
            lis = [x.get("count") for x in data]
            avg = sum(lis) // len(lis)
            return int(avg)


@app.route('/chart/')
def chart():
    data = get_data(flag=1)
    date_time = data.get("date_time")
    count = data.get("count")
    return render_template("show.html", date_time=date_time, count=count)


@app.route('/chart2/')
def chart2():
    data = get_data(flag=2)
    data_all = {"data": data, "min_status": X_Axis_Span, "avg": get_data(flag=3)}
    return render_template("show_2.html", data=data_all)


@app.route('/')
def index():
    data = get_data(flag=2)
    data_all = {"data": data, "min_status": X_Axis_Span, "avg": get_data(flag=3)}
    return render_template("show_2.html", data=data_all)


def run():
    app.run(host='0.0.0.0', port=9991)


if __name__ == '__main__':
    run()
