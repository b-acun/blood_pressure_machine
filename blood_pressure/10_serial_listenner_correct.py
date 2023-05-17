# -*- coding: utf-8 -*-
import serial
import csv 
from datetime import datetime


ser=serial.Serial('COM5',115200, timeout=0.5)
ser.flushInput()
ser.close()
ser.open()

now = datetime.now() 
date_time = now.strftime('%X').replace(":","-")
filename="yeniveri_test"+date_time+".csv"

while True:
    inline = str(ser.readline().strip())
    inline=inline.replace("'","")
    inline=inline.replace("b","")   
    print(inline)
    
    info=inline
    
    now = datetime.now() 
    date_time = now.strftime('%X')
    
    info= date_time+";"+info
    info=info.split(";")
    print(info)


    with open(filename,'a',newline='') as f:
        writer = csv.writer(f,delimiter=";")
        writer.writerow(info)
        