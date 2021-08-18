from tkinter import*
import time;
import datetime
import pygame
import scipy.io.wavfile as sci
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

pygame.init()
root = Tk()
root .title("Procesamiento de señales fundamentos")
root. geometry("1124x600+0+0")
root .configure(background = 'white')


def do_plot(z,frecValue):
    

    frame1 = Frame(root); frame1.place(x=580, y=0, width=500, height=500)
    fig = Figure(figsize=(1, 4), dpi=100)
    fig.suptitle
    fig.suptitle('Frecuencia del tono: %i Hz' %frecValue, fontsize=16)
    
    t = np.arange(0, 3, .01)    
    fig.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t *z))    
    canvas = FigureCanvasTkAgg(fig, frame1)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
   

ABC = Frame(root, bg = "black",bd = 20, relief = RIDGE)
ABC.grid()
ABC1 = Frame(root, bg = "black",bd = 20, relief = RIDGE)
ABC1.grid()
ABC2 = Frame(root, bg = "black", relief = RIDGE)
ABC2.grid()
ABC3 = Frame(root, bg = "black", relief = RIDGE)
ABC3.grid()

strl = StringVar()
strl.set("Generador de tonos")

#================================

def value_C():
    strl.set("L1")  
    fig = Figure(figsize=(1, 4), dpi=100)
    fig.clf()
    do_plot(10,1000)
    #sound=pygame.mixer.Sound(r"F:/PSF/ProcesamientoDatos-master/Scripts/7.data/rec_SOL.wav")
    
    #sound.play()
def value_D():   
    strl.set("L2")    
    do_plot(15,1500)
    #sound=pygame.mixer.Sound(r"F:/PSF/ProcesamientoDatos-master/Scripts/7.data/rec_RE.wav")
    #sound.play()
def value_E():
    strl.set("L3")
    do_plot(20,2000)
    #sound=pygame.mixer.Sound(r"F:/PSF/ProcesamientoDatos-master/Scripts/7.data/rec_MI.wav")
    #sound.play()
def value_F():
    strl.set("Ruido")
    do_plot(40,5000)
  #  sound=pygame.mixer.Sound(r"C:\Users\Dell\Desktop\Music_Notes\F.wav")
    #sound.play()
def value_G():
    strl.set("Off")
    do_plot(0,0)
#========================================================================================================


Label(ABC1, text = "PSF MSE2021", font = ('arial', 25 , 'bold'), padx = 8, pady = 8, bd = 4, bg = "black",
      fg = "white", justify = CENTER).grid(row = 0, column = 0, columnspan = 11)

#===================================================================================================================



txtDisplay = Entry(ABC1, textvariable = strl, font = ('arial', 18, 'bold'), bd = 34, bg = "black",
      fg = "white", width = 28, justify = CENTER).grid(row = 1, column = 1, pady = 1)

#===============================================================================================================

btnC = Button(ABC3,  height = 8, width = 6, bd = 4, text = "L1", font = ('arial', 18 , 'bold'), bg = "white",  fg = "black" ,
              command = value_C)
btnC.grid(row = 0, column = 0, padx = 5, pady = 5)

btnD = Button(ABC3,  height = 8, width = 6, bd = 4, text = "L2", font = ('arial', 18 , 'bold'), bg = "white",  fg = "black",
              command = value_D)
btnD.grid(row = 0, column = 1, padx = 5, pady = 5)

btnE = Button(ABC3,  height = 8, width = 6, bd = 4, text = "L3", font = ('arial', 18 , 'bold'), bg = "white",  fg = "black",
              command = value_E)
btnE.grid(row = 0, column = 2, padx = 5, pady = 5)

btnF = Button(ABC3,  height = 8, width = 6, bd = 4, text = "Ruido", font = ('arial', 18 , 'bold'), bg = "white",  fg = "black",
              command = value_F)
btnF.grid(row = 0, column = 3, padx = 5, pady = 5)

btnG = Button(ABC3,  height = 8, width = 6, bd = 4, text = "Off", font = ('arial', 18 , 'bold'), bg = "white",  fg = "black",
              command = value_G)
btnG.grid(row = 0, column = 4, padx = 5, pady = 5)



root.mainloop()