import MySQLdb

import time
import datetime
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

conn = MySQLdb.connect(host='localhost',user='root',passwd='wns1077511',db='test')
# print("error8")
cur=conn.cursor()
# print("error10")
sql="insert into project(sign,time) values (%s,%s)"
# print("error12")
container=["0",st]
# print("error14")
cur.execute(sql, container)
# print("error16")
conn.commit()
# print("error18")
