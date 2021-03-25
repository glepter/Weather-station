from tkinter import *
from tkinter import ttk
from tkinter.font import Font

#crea objeto Tk y pone titulo a la ventana
window = Tk()
window.title("Interfaz")

#crea frame interno
Top = LabelFrame(window, text="Lectura de sensores", bd=2)
Top.grid(columnspan=5, padx=10, pady=15)

#boton y fondo para el sensor 1
bs1 = Button(Top, text="Sensor 1", width=10, height=2, command=window.quit)
bs1.grid(row=0, column=0, sticky=E)
cs1 = Canvas(Top, bg='black', width=300, height=40)
cs1.grid(row=0, column=1,  columnspan=2, sticky=W)

#boton y fondo para el sensor 2
bs2 = Button(Top, text="Sensor 2", width=10, height=2, command=window.quit)
bs2.grid(row=1, column=0, sticky=E)
cs2 = Canvas(Top, bg='black', width=300, height=40)
cs2.grid(row=1, column=1,  columnspan=2, sticky=W)

#boton y fondo para el sensor 3
bs3 = Button(Top, text="Sensor 3", width=10, height=2, command=window.quit)
bs3.grid(row=2, column=0, sticky=E)
cs3 = Canvas(Top, bg='black', width=300, height=40)
cs3.grid(row=2, column=1,  columnspan=2, sticky=W)

#boton y fondo para el sensor 4
bs4 = Button(Top, text="Sensor 4", width=10, height=2, command=window.quit)
bs4.grid(row=3, column=0, sticky=E)
cs4 = Canvas(Top, bg='black', width=300, height=40)
cs4.grid(row=3, column=1,  columnspan=2, sticky=W)

#texto y numeros para tiempo de muestreo
lsample = Label(text="Tiempo de muestreo")
lsample.grid(row=1, column=0)
spin = Spinbox( from_= 0, to = 60, wrap = True, width=2, font=Font(family='Helvetica', size=9, weight='normal'))   
spin.grid(row=1,column=1, sticky=W)
lmin = Label(text="minutos")
lmin.grid(row=1, column=1)

#botones de interaccion
breport = Button(text="Reporte", width=10, height=2, command=window.quit)
breport.grid(row=2, column=0, padx=10, pady=10)
bstop = Button(text="Detener", width=10, height=2, command=window.quit)
bstop.grid(row=2, column=1, padx=20, pady=5)
bresume = Button(text="Continuar", width=10, height=2, command=window.quit)
bresume.grid(row=2, column=2, padx=10, pady=5)



window.mainloop()