#!python3 TP FINAL DE PSF

from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

root = Tk()
root .title("Frecuencia:")
root. geometry("340x600+0+0")
#root.attributes("-fullscreen", True) 
# this should make Esc exit fullscrreen, but doesn't seem to work..
#root.bind('',root.attributes("-fullscreen", False))
root.configure(background='white')

time1 = 1
titulo = Label(root, font=('arial', 20, 'bold'), fg='black',bg='white')
titulo.pack()
titulo.config(text="Frecuencia [Hz]")
clock_lt = Label(root, font=('arial', 80, 'bold'), fg='red',bg='white')
clock_lt.pack()
Leds = Label(root, font=('arial', 20, 'bold'), fg='black',bg='white')
Leds.pack()
Leds.config(text="Estado LEDs:")
estadoLed1 = Label(root, font=('arial', 20, 'bold'), fg='red',bg='white')
estadoLed1.pack()
estadoLed2 = Label(root, font=('arial', 20, 'bold'), fg='green',bg='white')
estadoLed2.pack()
estadoLed3 = Label(root, font=('arial', 20, 'bold'), fg='blue',bg='white')
estadoLed3.pack()
estadoLed4 = Label(root, font=('arial', 20, 'bold'), fg='purple',bg='white')
estadoLed4.pack()

STREAM_FILE=('COM7',"serial")
#STREAM_FILE=("/dev/ttyUSB1","serial")
#STREAM_FILE=("log.bin","file")

header = { "pre": b"*header*", "id": 0, "N": 128, "fs": 10000, "maxIndex":0, "maxValue":0,"pos":b"end*" }
plt.title("Espectro en frecuencia",fontsize=15)
fig    = plt.figure ( 1 )

adcAxe = fig.add_subplot ( 2,1,1                            )
adcLn, = plt.plot        ( [],[],'r-',linewidth=4           )
adcAxe.grid              ( True                             )
adcAxe.set_ylim          ( -2 ,2                            )


fftAxe      = fig.add_subplot ( 2,1,2                                 )
fftLn,      = plt.plot        ( [],[],'b-',linewidth = 5,alpha  = 1   )
ciaaFftLn,  = plt.plot        ( [],[],'r-',linewidth = 10,alpha = 0.4 )
maxValueLn, = plt.plot        ( [],[],'y-',linewidth = 2,alpha  = 0.3 )
maxIndexLn, = plt.plot        ( [],[],'y-o',linewidth = 6,alpha = 0.8 )
fftAxe.grid                   ( True                                  )
fftAxe.set_ylim               ( 0 ,0.30                               )

def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]
    h["id"]       = readInt4File(f,4)
    h["N" ]       = readInt4File(f)
    h["fs"]       = readInt4File(f)
    h["maxIndex"] = readInt4File(f,4)
    h["maxValue"] = (readInt4File(f,sign = True)*1.65**2)/(2**4*512) #el resultado sale en 3.13 y yo arranque con 1.15 corrido 6 a la izq. asi que ahora solo basta correr 4 a la derecha, normalizar con 1.65/512, pero como lo muestro comparando con potencia, elevo al cuadrado
    frecValue= h["maxIndex"] *100
    print("el valor es:", frecValue)
    clock_lt.config(text=frecValue)
    
    if frecValue>1000 and frecValue<1500:
        estadoLed1.config(text="Led1: OFF")
    else:  
        estadoLed1.config(text="Led1: ON")
    if frecValue>2000 and frecValue<2500:
        estadoLed2.config(text="Led2: OFF")
    else : 
        estadoLed2.config(text="Led2: ON")
    if frecValue>3000 and frecValue<3500:
        estadoLed3.config(text="Led3: OFF")
    else: 
        estadoLed3.config(text="Led3: ON")
    if frecValue>4000 and frecValue<4500:
        estadoLed4.config(text="Led4: OFF")
    else: 
        estadoLed4.config(text="Led4: ON")


    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    
    #print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    
    return h["id"],h["N"],h["fs"],h["maxIndex"],h["maxValue"]

def readInt4File(f,size=2,sign=False):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return (int.from_bytes(raw,"little",signed=sign))

def flushStream(f,h):
    if(STREAM_FILE[1]=="serial"): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*h["N"],io.SEEK_END)

def readSamples(adc,fft,N,trigger=False,th=0):
    state="waitLow" if trigger else "sampling"
    i=0
    for t in range(N):
        sample = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        #part real plus imag
        fftBin = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512) +\
                 1j*(readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        state,nextI= {
                "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
                "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
                "sampling": lambda sample,i: ("sampling",i+1)
                }[state](sample,i)
        adc[i]=sample
        fft[i]=fftBin
        i=nextI

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs,maxIndex,maxValue=findHeader ( streamFile,header )
    adc     = np.zeros(N)
    ciaaFft = np.zeros(N).astype(complex)
    time    = np.arange(0,N/fs,1/fs)
    readSamples(adc,ciaaFft,N,False,0)     
    adcAxe.set_xlim ( 0    ,N/fs )
    adcLn.set_data  ( time ,adc  )

    fft=np.abs ( 1/N*np.fft.fft(adc ))**2
    fftAxe.set_ylim ( 0 ,np.max(fft)+0.006)
    fftAxe.set_xlim ( 0 ,fs/2 )
    fftLn.set_data    ( (fs/N )*fs*time ,fft)
    ciaaFftLn.set_data ( (fs/N )*fs*time ,np.abs(ciaaFft)**2)
    
  #  maxValueLn.set_data ( time,maxValue           )
    maxIndexLn.set_data ( [(fs/N )*fs*time[maxIndex],(fs/N )*fs*time[maxIndex]],[0,maxValue] )    
    return adcLn, fftLn,  maxValueLn,  maxIndexLn, ciaaFftLn


def tick():
    global time1
    time2 = 2

    #if time2 != time1: # if time string has changed, update it
    #    time1 = time2
    #clock_lt.config(text=time2)
        
        
        
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use &gt;200 ms, but display gets jerky
    clock_lt.after(200, tick)
 


#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

tick()

ani=FuncAnimation(fig,update,10000,init_func=None,blit=True,interval=1,repeat=True)
plt.draw()
plt.get_current_fig_manager()
plt.show()
streamFile.close()

