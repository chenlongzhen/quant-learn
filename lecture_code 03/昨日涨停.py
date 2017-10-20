#encoding=utf-8
# 股票涨停日

import tushare as ts
import datetime
import MySQLdb as mdb
from sqlalchemy import create_engine


def intoDB(date='2017-10-20'):
    '''
    Insert symbols to Mysql
    '''

    print("[info] getting {}".format(date))
    data = ts.top_list(date)

    print("[info] into mysql")
    engine = create_engine('mysql://clz:1@127.0.0.1/stock?charset=utf8')

    data.to_sql('longhu', engine)


def main(_):
    date = datetime.datetime.now() + datetime.timedelta(days=-1)
    date = date.strftime("%Y-%m-%d")
    intoDB(date)

if __name__ == "__main__":
    main(1)
