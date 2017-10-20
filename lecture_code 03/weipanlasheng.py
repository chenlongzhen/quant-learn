import tushare as ts
import pandas as pd
import numpy as np
import datetime 

def _ifLasheng(stockid='000001', date='2017-10-15'):
    '''get one days weipan change'''
    
    now = datetime.datetime.strptime(date, '%Y-%m-%d')
    nowPlusOne = datetime.timedelta(days = 1)

    nowStr = now.strftime('%Y-%m-%d')
    nowPlusOneStr = nowPlusOne.strftime('%Y-%m-%d')

    closeData = ts.get_hist_data(stockid, start=nowStr, end=nowPlusOneStr, ktype='30').iloc[0,:]

    change = closeData['price_change']/closeData['open']

    if change >= 0.03:
        return True
    else:
        return False


def stockLasheng(date = '2017-10-15'):
    '''
    计算多日拉升
    '''    
    stockBasic = ts.get_stock_basics()
    stockAllId = stockBasic.index
    stockName =  stockBasic['name']
    
    
    symbols = []
    for sid,sname in zip(stockAllId, sotckName):
        try:
            lasheng = _ifLasheng(sid,date)
        except Exception as e:
            lashen = Flase
            print("[error] {}".format(e))
        if lasheng:
            symbols.append(
                    (sid,sname,date,1)
                    )

    return symbols



def intoDB(symbols):
    '''
    Insert symbols to Mysql
    '''
    
    db_host = 'localhost'
    db_user = 'clz'
    db_pass = '1'
    db_name = 'securities_master'

    con = mdb.connect(
        host=db_host, user=db_user, passwd=db_pass, db=db_name
    )

    # Create the insert strings
    column_str = """stockname, stockid, stockdate, iflasheng"""

    insert_str = ("%s, " * 4)[:-2]
    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % \
        (column_str, insert_str)

    # Using the MySQL connection, carry out 
    # an INSERT INTO for every symbol
    with con: 
        cur = con.cursor()
        cur.executemany(final_str, symbols)


def main(_):
    symbols = stockLasheng(date = "2017-10-15")
    initoDB(symbols)

        
