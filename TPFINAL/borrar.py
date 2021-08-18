from tkinter import*

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = Tk()
root .title("Procesamiento de señales fundamentos")
root. geometry("1024x800+0+0")
root .configure(background = 'white')


def do_plot(z):
    frame1 = Frame(root); frame1.place(x=500, y=0, width=500, height=500)
    fig = Figure(figsize=(1, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot().plot(t, 2 * np.sin(2 * np.pi * t*z))

    canvas = FigureCanvasTkAgg(fig, frame1)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    

# pack_toolbar=False will make it easier to use a layout manager later on.

y=5
do_plot(4)


#button = tkinter.Button(master=root, text="Quit", command=root.quit)

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
#button.pack(side=tkinter.BOTTOM)
#toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)


root.mainloop()