import serial
import time
# import datetime
# ts = time.time()
# st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
ser = serial.Serial(port='COM5',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout = 0)
time.sleep(2)
ser.readline()
while True:
    s = ser.readline()[:-2]
    # if len(s)>0:
    print(int(s)+1)

    time.sleep(1)
