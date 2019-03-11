import pymysql
import json
import hashlib
from string import Template as TP
from random import choice


class OpenMySQL:
    def __init__(self, user='root',
                 passwd='mysql',
                 host='localhost',
                 port=3306,
                 db='proxy',
                 charset='utf8',
                 cursorclass=pymysql.cursors.DictCursor, connect_timeout=600, **kwargs):
        super(OpenMySQL, self).__init__()
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset,
                                    cursorclass=cursorclass, connect_timeout=connect_timeout, **kwargs)
        self.cur = self.conn.cursor()

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def select_all(self, sql, db):
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as E:
            print("数据库查询出错", db, E)

    @staticmethod
    def hash_it(hash_str):
        md = hashlib.md5()
        md.update(hash_str.encode("utf-8"))
        return md.hexdigest()

    def save_proxy_count(self, dic):
        """
        :param dic: {'date_time': the date time, 'count': int}
        :return: 'success' or 'fail'
        """
        status = 'fail'
        if dic:
            date_time = dic.get('date_time')
            count = dic.get('count')

            save_sql = """insert into proxy_time_table (date_time, count) values ("%s", "%s");""" % (date_time, count)

            try:
                self.cur.execute(save_sql)
                self.conn.commit()
                print('     插入数据成功')
                status = 'Success'
            except Exception as E:
                print("     数据插入出错！　", E)

        return status


if __name__ == "__main__":
    # # sql = """select player_id,team_id,nums,name_zh,name_en,pos_sin,pos_name,sec_sin,sec_name,player_info,icon from leisu.player;"""
    # db = OpenMySQL()
    #
    # # sql = """select team_id from soccer_teams;"""
    # sql = """SELECT data FROM soccer_team_schedule limit 1;"""
    # result = db.select_all(sql=sql, db="hupu")
    # # print(json.loads(result[0]["data"]))
    # # result = db.su_data()
    #
    # with open("soccer_team_schedule_data_limit_1.json", "w") as wf:
    #     result = json.loads(result[0].get("data"))
    #     result = json.dumps(result, ensure_ascii=False)
    #     wf.write(result)

    # ---------------
    # db.save_schedule_data_xpath({"a": "1", "b": "2", "c": "3", "d": "4", "e": {'ee': 55}})

    # db = OpenMySQL(user='quinns',
    #                passwd='Quinns3000',
    #                host='192.168.0.61',
    #                port=3306,
    #                db='leisu',
    #                charset='utf8',
    #                cursorclass=pymysql.cursors.DictCursor, connect_timeout=600)
    # print(db.select_all(sql='select * from team_b limit 1;', db='leisu'))

    db = OpenMySQL(user='quinns',
                   passwd='Quinns3000',
                   host='192.168.0.61',
                   port=3306,
                   db='leisu',
                   charset='utf8',
                   cursorclass=pymysql.cursors.DictCursor, connect_timeout=600)
    print(db.select_all(sql='select team_id,data from leisu_f_team_info limit 1;', db='leisu'))
