import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
import time

#get ready to use ECG signal
rawsignals=pd.read_csv("yeniveri_test13-34-06.csv", delimiter=";")

ecg = rawsignals[rawsignals.columns[1]].to_numpy()
real_time = rawsignals[rawsignals.columns[0]].to_numpy()
# sampling frequency 125Hz
fs = 125
time = np.arange(ecg.size) / fs
winsize = fs * 25
winhop = fs
i = 0

def on_press(event):
    global i
    print('press', event.key)
    sys.stdout.flush()
    lower = i
    upper = i + winsize
    winhighlight=np.ones(len(ecg))*-3
    winhighlight[lower:upper]=4
    ax1.cla()
    ax1.plot(time, ecg, 'g')
    ax1.plot(time, winhighlight, 'r')
    ax1.plot(time[lower:upper], ecg[lower:upper], 'r')
    ax1.grid()
    ax1.set_title('Raw Signal')

    x = ecg[lower:upper]
    derx=np.gradient(x)
    pwe_indx=[]
    
    ax2.cla()
    ax2.plot(x, 'black')
    ax2.plot(derx ,'r')
    ax2.plot(pwe_indx,x[pwe_indx], 'x')
    
    # Pulse Wave Systolic Peak
    peaks2, properties = find_peaks(x, prominence=[0.5], distance=25)
    ax2.plot(peaks2, x[peaks2], 'go', label='Pulse Wave Systolic Peak')
    
    ymin=x[peaks2] - properties["prominences"]
    ymax = x[peaks2]
    
    elapsedtime = (peaks2[-1]-peaks2[1])
    x1 = pd.to_datetime(real_time[peaks2[1]],format='%H:%M:%S')
    x2 = pd.to_datetime(real_time[peaks2[-1]],format='%H:%M:%S')

#küçük tansiyon için algoritmayı tekrar ayarladığım kısım
    for i in range(len(peaks2), 0, -1):
        if (ymax[1]- ymax[i-1] > 50) & (ymax[1]- ymax[i-1] < 70):
            print(ymax[i-1])

        else:
            print("*******",ymax[i-1])
            break



        
    num_peaks = len(peaks2) - 1
    print("high blood pressure",ymax[1])
    print("low blood pressure",ymax[i-1]) 
    # print(ymax[control])
    # print("peak number:",num_peaks)
    # print("pulse:", (num_peaks * 60) / elapsedtime ) 
    # print("elapsedtime:", elapsedtime)
    
    tpeaks=(x2-x1)
    tpeaks=tpeaks.total_seconds()
    numbeats=60/(tpeaks/num_peaks)
    # print("timepeaks:",tpeaks)
    print("number of beats",numbeats)
       
    if event.key == 'right':
        i = i + winhop
        fig.canvas.draw()
    elif event.key == 'left':
        i = i - winhop
        fig.canvas.draw()

def calculateAverageValue(startPeaks, endPeaks):
    sum=0
    if(len(startPeaks)>=len(endPeaks)):
        for i in range(0, len(endPeaks)):
            sum=sum+(endPeaks[i]-startPeaks[i])
    else:
        for i in range(0, len(startPeaks)):
            sum=sum+(endPeaks[i]-startPeaks[i])
                
    return str(sum/len(startPeaks))

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(time, ecg, 'g')
ax1.grid()
ax1.set_title('Raw Signal')
ax2 = fig.add_subplot(212)
ax2.grid()

fig.canvas.mpl_connect('key_press_event', on_press)

plt.show()
