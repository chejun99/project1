import MySQLdb
import serial
import time
import datetime

ser = serial.Serial(port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0)
time.sleep(2)
ser.readline()

conn = MySQLdb.connect(host='localhost',user='root',passwd='wns1077511',db='test')

cur=conn.cursor()

sql="insert into project(sign,time) values (%s,%s)"

while True:
    s = ser.readline()[:-2]

    print(int(s)+1)

    time.sleep(0.9)
#----------------------------------------------------------
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    container=[s,st]

    cur.execute(sql, container)

    conn.commit()

    print(container)

    print("commit")
