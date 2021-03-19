from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from datetime import date
from openpyxl import load_workbook
from openpyxl.utils import *
import serial.tools.list_ports
import serial
import xlrd
import xlwt

ser = serial.Serial()

SMAIN = 'LightBlue4'


class UI:
    def __init__(self, master, a):
        #crea objeto Tk y pone titulo a la ventana
        self.sheet = a
        self.master = master
        self.master.title("Interfaz")
        
        self.First = Frame(self.master)

        #crea frame interno
        Top = LabelFrame(self.First, text="Lectura de sensores", bd=2)
        Top.grid(columnspan=5, padx=10, pady=15, ipadx=2, ipady=2)

        #boton y fondo para el sensor 1
        bs1 = Button(Top, text="Sensor 1", width=10, height=2,  highlightthickness=0,  command=self.master.destroy)
        bs1.grid(row=0, column=0, sticky=E, pady=4, padx=5)
        cs1 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs1.grid(row=0, column=1,  columnspan=2, sticky=W, padx=5)

        #boton y fondo para el sensor 2
        bs2 = Button(Top, text="Sensor 2", width=10, height=2, highlightthickness=0, command=self.master.destroy)
        bs2.grid(row=1, column=0, sticky=E, pady=4, padx=5)
        cs2 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs2.grid(row=1, column=1,  columnspan=2, sticky=W, padx=5)

        #boton y fondo para el sensor 3
        bs3 = Button(Top, text="Sensor 3", width=10, height=2, highlightthickness=0, command=self.master.destroy)
        bs3.grid(row=2, column=0, sticky=E, pady=4, padx=5)
        cs3 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs3.grid(row=2, column=1,  columnspan=2, sticky=W, padx=5)

        #boton y fondo para el sensor 4
        bs4 = Button(Top, text="Sensor 4", width=10, height=2, highlightthickness=0, command=self.master.destroy)
        bs4.grid(row=3, column=0, sticky=E, pady=4, padx=5)
        cs4 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs4.grid(row=3, column=1,  columnspan=2, sticky=W, padx=5)

        #texto y numeros para tiempo de muestreo
        lsample = Label(self.First, text="Tiempo de muestreo", highlightthickness=0)
        lsample.grid(row=1, column=0)
        spin = Spinbox(self.First,  from_= 0, to = 60, wrap = True, width=2, highlightthickness=0, border=0, font=Font(family='Helvetica', size=9, weight='normal'))   
        spin.grid(row=1,column=1, sticky=W)
        lmin = Label(self.First, text="minutos", highlightthickness=0)
        lmin.grid(row=1, column=1)

        #botones de interaccion
        breport = Button(self.First, text="Reporte", width=10, height=2, command=self.report)
        breport.grid(row=2, column=0, padx=10, pady=10)
        bstop = Button(self.First, text="Detener", width=10, height=2, command=self.readFile)
        bstop.grid(row=2, column=1, padx=20, pady=5)
        bresume = Button(self.First, text="Continuar", width=10, height=2,command=self.readSerial)
        bresume.grid(row=2, column=2, padx=10, pady=5)

        self.First.grid()

        
    def report(self):
        self.Second = Toplevel(self.master)
        frame = LabelFrame(self.Second, text="Parametros de reporte")
        frame.grid(row=0, column=0, columnspan=3, padx=15, pady=10)

        flab = Label(frame, text="Desde: ")
        flab.grid(row=1 , column=0, pady=0, padx=20)
        tlab = Label(frame, text="hasta: ")
        tlab.grid(row=2 , column=0, pady=10, padx=20)
        
        d = date.today()
        dia.set(d.day)
        ddia.set(d.day-5)
        mes.set(d.month)
        anio.set(d.year)

        dlab = Label(frame, text="Dia")
        dlab.grid(row=0 , column=1, pady=2, padx=10)
        mlab = Label(frame, text="Mes")
        mlab.grid(row=0 , column=2, pady=2, padx=10)
        alab = Label(frame, text="Año")
        alab.grid(row=0 , column=3, pady=2, padx=10)


        fdia = Spinbox(frame,  from_= 0, to = 31, wrap = True, width=4, textvariable=ddia, font=Font(family='Helvetica', size=9, weight='normal'))
        fdia.grid(row=1 , column=1, pady=5, padx=10)
        fmes = Spinbox(frame,  from_= 0, to = 12, wrap = True, width=4, textvariable=mes, font=Font(family='Helvetica', size=9, weight='normal'))
        fmes.grid(row=1 , column=2, pady=5)
        fanio = Spinbox(frame,  from_= 2021, to = 2022, wrap = True, width=4, textvariable=anio, font=Font(family='Helvetica', size=9, weight='normal'))
        fanio.grid(row=1 , column=3, pady=5, padx=10)
        
        dia.set(d.day)

        sdia = Spinbox(frame,  from_= 0, to = 31, wrap = True, width=4, textvariable=dia, font=Font(family='Helvetica', size=9, weight='normal'))
        sdia.grid(row=2 , column=1, pady=5, padx=10)
        smes = Spinbox(frame,  from_= 0, to = 12, wrap = True, width=4, textvariable=mes, font=Font(family='Helvetica', size=9, weight='normal'))
        smes.grid(row=2 , column=2, pady=5)
        sanio = Spinbox(frame,  from_= 2021, to = 2022, wrap = True, width=4, textvariable=anio, font=Font(family='Helvetica', size=9, weight='normal'))
        sanio.grid(row=2 , column=3, pady=5, padx=10)

        sen1 = Checkbutton(frame, text = "Sensor 1", variable=s1)
        sen1.grid(row=3, column=0, padx=10, pady=10)
        sen2 = Checkbutton(frame, text = "Sensor 2", variable=s2)
        sen2.grid(row=3, column=1, padx=10, pady=10)
        sen3 = Checkbutton(frame, text = "Sensor 3", variable=s3)
        sen3.grid(row=3, column=2, padx=10, pady=10)
        sen4 = Checkbutton(frame, text = "Sensor 4", variable=s4)
        sen4.grid(row=3, column=3, padx=10, pady=10)


        gen = Button(self.Second, text="Generar", width=10, height=2, command=self.Second.destroy)
        gen.grid(row=2, column=0, padx=10, pady=10)
        cancel = Button(self.Second, text="Cancelar", width=10, height=2, command=self.Second.destroy)
        cancel.grid(row=2, column=2, padx=20, pady=5)
        self.Second.grid()
    
    def readSerial(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            a=str(p.name)
            if "Arduino" in p.description:
                ser.port=a
                try: 
                    ser.open()
                    print(ser.is_open)
                except:
                    print("Puerto ocupado")
            else:
                print("Dispositivo no encontrado")
    
    def readFile(self):
           
         
         print(self.sheet['A1'].value)




root = Tk()
s1 = IntVar()
s1.set(True)
s2 = IntVar()
s2.set(True)
s3 = IntVar()
s3.set(True)
s4 = IntVar()
s4.set(True)

dia = IntVar()
ddia = IntVar()
mes = IntVar()
anio = IntVar()
wb = load_workbook(filename = 'hola.xlsx')  
sheet = wb['Sheet1']

my_gui = UI(root, sheet)
root.mainloop()