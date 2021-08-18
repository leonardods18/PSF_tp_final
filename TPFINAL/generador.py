from tkinter import*
import time;
import datetime
import pygame
import scipy.io.wavfile as sci
import matplotlib.pyplot as plt

pygame.init()
root = Tk()
root .title("Procesamiento de señales fundamentos")
root. geometry("1024x800+0+0")
root .configure(background = 'white')


ABC = Frame(root, bg = "powder blue",bd = 20, relief = RIDGE)
ABC.grid()
ABC1 = Frame(root, bg = "powder blue",bd = 20, relief = RIDGE)
ABC1.grid()
ABC2 = Frame(root, bg = "powder blue", relief = RIDGE)
ABC2.grid()
ABC3 = Frame(root, bg = "powder blue", relief = RIDGE)
ABC3.grid()

strl = StringVar()
strl.set("Generador de tonos")

#================================

def value_C():
    strl.set("L1")
    sound=pygame.mixer.Sound(r"F:/PSF/ProcesamientoDatos-master/Scripts/7.data/rec_SOL.wav")
    sound.play()
def value_D():
    strl.set("L2")
    sound=pygame.mixer.Sound(r"F:/PSF/ProcesamientoDatos-master/Scripts/7.data/rec_RE.wav")
    sound.play()
def value_E():
    strl.set("L3")
    sound=pygame.mixer.Sound(r"F:/PSF/ProcesamientoDatos-master/Scripts/7.data/rec_MI.wav")
    sound.play()
def value_F():
    strl.set("Ruido")
  #  sound=pygame.mixer.Sound(r"C:\Users\Dell\Desktop\Music_Notes\F.wav")
    sound.play()

#========================================================================================================


Label(ABC1, text = "PSF MSE2021", font = ('arial', 25 , 'bold'), padx = 8, pady = 8, bd = 4, bg = "powder blue",
      fg = "white", justify = CENTER).grid(row = 0, column = 0, columnspan = 11)

#===================================================================================================================



txtDisplay = Entry(ABC1, textvariable = strl, font = ('arial', 18, 'bold'), bd = 34, bg = "powder blue",
      fg = "black", width = 28, justify = CENTER).grid(row = 1, column = 1, pady = 1)

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





root.mainloop()