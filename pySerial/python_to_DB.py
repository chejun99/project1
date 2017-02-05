import MySQLdb

import time
import datetime
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

conn = MySQLdb.connect(host='localhost',user='root',passwd='wns1077511',db='test')

cur=conn.cursor()

sql="insert into sensor(sign,time) values (%s,%s)"

container=["0",st]

cur.execute(sql, container)

conn.commit()
