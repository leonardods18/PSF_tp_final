#!python3
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


#STREAM_FILE=(r"F:/PSF/psf_2021-dev/clases/tp2/chapu_noise.npy","file")
#STREAM_FILE=("log.bin","file")
#STREAM_FILE=('COM15',"serial")
header = { "pre": b"*header*", "id": 0, "N": 128, "fs": 10000, "hLength":0,"pos":b"end*" }
fig    = plt.figure ( 1 )
fig.suptitle('Convolucion en tiempo con la CIAA', fontsize=16)

#--------------------------ADC--------------------------
adcAxe = fig.add_subplot ( 3,2,1                  )
adcAxe.set_title("adc",rotation=0,fontsize=10,va="center")
adcLn, = plt.plot        ( [],[],'r-o',linewidth = 12, alpha = 0.3 ,label = "adc")
adcLg  = adcAxe.legend()
adcAxe.grid     ( True      )
adcAxe.set_ylim ( 0,0.005 )#np.max(absFft))
adcAxe.set_ylim ( -1.2 ,1.2 )

ciaaConvAxe        = fig.add_subplot ( 3,2,5 )
ciaaConvAxe.set_title("ciaaConv",rotation = 0,fontsize = 10,va = "center")
ciaaConvLn,     = plt.plot ( [] ,[] ,'r-o' ,linewidth = 12  ,alpha = 0.3 ,label = "ciaaConv" )
ciaaConvLg      = ciaaConvAxe.legend()
ciaaConvAxe.set_ylim ( 0,0.05 )#np.max(absFft))
ciaaConvAxe.set_ylim ( -1.2 ,1.2 )


XAxe = fig.add_subplot ( 3,2,2 )
XAxe.set_title("FFT(adc)",rotation=0,fontsize=10,va="center")
XLn, = plt.plot        ( [],[],'b-o',linewidth = 5, alpha = 0.3 ,label = "X")
XLg  = XAxe.legend()
XAxe.grid     ( True      )
XAxe.set_ylim ( 0 ,0.05 )

YAxe        = fig.add_subplot ( 3,2,6 )
YAxe.set_title("FFT(conv)",rotation = 0,fontsize = 10,va = "center")
YLn, = plt.plot ( [] ,[] ,'b-o' ,linewidth = 5  ,alpha = 0.3 ,label = "Y" )
YLg  = YAxe.legend()
YAxe.set_ylim ( 0,0.05 )

def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]
    h["id"]      = readInt4File(f,4)
    h["N" ]      = readInt4File(f)
    h["fs"]      = readInt4File(f)
    h["hLength"] = readInt4File(f)  
 
    
    
    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    #print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"],h["hLength"]

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

def readSamples(adc,h,conv,N,trigger=False,th=0):
    state="waitLow" if trigger else "sampling"
    i=0
    for t in range(N):
        sample    = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        ciaaH     = (readInt4File(streamFile,sign = True)/2**15)
        ciaaConv  = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        state,nextI= {
                "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
                "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
                "sampling": lambda sample,i: ("sampling",i+1)
                }[state](sample,i)
        adc [ i ] = sample
        h   [ i ] = ciaaH
        conv[ i ] = ciaaConv
        i=nextI

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs,hLength=findHeader ( streamFile,header )
    nData    = np.arange(0,N+hLength-1,1) #arranco con numeros enteros para evitar errores de float
    adc      = np.zeros(N+hLength-1)
    h        = np.zeros(N+hLength-1)
    ciaaConv = np.zeros(N+hLength-1)
    tData    = nData/fs
    readSamples(adc,h,ciaaConv,N+hLength-1,False,0)

    adcAxe.set_xlim ( 0     ,(N+hLength-1)/fs )
    adcLn.set_data  ( tData ,adc  )

    ciaaConvAxe.set_xlim ( 0     ,(N+hLength-1 )/fs     )
    ciaaConvAxe.set_xlim ( 0     ,(N+hLength-1 )/fs     )    
    ciaaConvLn.set_data ( tData ,ciaaConv )
#
    fData=nData[0:N]*fs/N-fs/2    
    XAxe.set_xlim ( -fs/2,fs/2)
    XLn.set_data (fData ,np.abs(np.fft.fftshift(np.fft.fft(adc[:N]))/N)**2)

    fData=nData[0:hLength]*fs/hLength-fs/2
    H=np.abs(np.fft.fftshift(np.fft.fft(h[:hLength]))/hLength)**2
    
    fData=nData*fs/(N+hLength-1)-fs/2
    YAxe.set_xlim (-fs/2,fs/2)
    YLn.set_data (fData ,np.abs(np.fft.fftshift(np.fft.fft(ciaaConv))/N)**2)
    #cutFrecZoneLn = fftAxe.fill_between([-cutFrec,cutFrec],100,-100,facecolor="yellow",alpha=0.5)

    return adcLn, ciaaConvLn, XLn ,YLn



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
