#encoding=utf-8
from sqlalchemy import create_engine
import tushare as ts


#买卖数据存入数据库
df = ts.get_tick_data('600848', date='2014-12-22')
engine = create_engine('mysql://clz:1@127.0.0.1/securities_master?charset=utf8')

#存入数据库
df.to_sql('tick_data',engine)