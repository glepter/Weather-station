from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from datetime import date
from datetime import datetime as dtime
from openpyxl import load_workbook
from openpyxl.utils import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import serial.tools.list_ports
import serial
from threading import *
import time
import numpy as np


#Crea Objeto de comunicacion self.serial (para conectar con Arduino), lo llamamos: self.ser
ser = serial.Serial(baudrate=115200, timeout=2)

#Creamos clase para Objeto que genera y maneja la UI (Interfaz de Usuario) y su funcionalidad.
class UI:

    #Inicializa el objeto, requiere una hoja de excel como argumento.
    def __init__(self, master, wb, ser):
        #Crea variable interna para controlar el libro y la hoja de excel.
        self.wb = wb
        self.sheet = self.wb.active
        #Crea variable interna para Objeto Serial. Crea variable para el root de TKInter y asigna titulo.
        self.ser = ser
        self.master = master
        self.master.title("Interfaz")
        #Crea un contenedor para la pagina principal (Frame).
        self.First = Frame(self.master)
        #Crea y configura contenedor para sensores.
        Top = LabelFrame(self.First, text="Lectura de sensores", bd=2)
        Top.grid(columnspan=5, padx=10, pady=15, ipadx=2, ipady=2)
        #Crea figura para contener las graficas.
        self.fig = Figure(dpi= 50, facecolor='Black', constrained_layout=True)
        #Crea y configura un area de dibujo de TKinter para contener la figura.       
        self.cs1 = FigureCanvasTkAgg(self.fig, master=Top)
        self.cs1.draw()
        self.cs1.get_tk_widget().grid(row=0, column=1, rowspan=4, sticky=E)
        #Crea y configura Labels para contener el valor actual.
        self.sLabel1 = Label(Top, text="grados", font=("Verdana",14))
        self.sLabel1.grid(row=0, column=3, sticky=E, pady=4, padx=5)
        self.sLabel2 = Label(Top, text="grados", font=("Verdana",14))
        self.sLabel2.grid(row=1, column=3, sticky=E, pady=4, padx=5)
        self.sLabel3 = Label(Top, text="grados", font=("Verdana",14))
        self.sLabel3.grid(row=2, column=3, sticky=E, pady=4, padx=5)
        self.sLabel4 = Label(Top, text="grados", font=("Verdana",14))
        self.sLabel4.grid(row=3, column=3, sticky=E, pady=4, padx=5)
        #Crea Etiquetas para identificar las graficas.
        ls1 = Label(Top, text="Sensor 1", font=("Verdana",18))
        ls1.grid(row=0, column=0, sticky=E, pady=4, padx=5)
        #Crea y define Boton para el Sensor 2.
        ls2 = Label(Top, text="Sensor 2", font=("Verdana",18))
        ls2.grid(row=1, column=0, sticky=E, pady=4, padx=5)
        #Crea y define Boton para el Sensor 3.
        ls3 = Label(Top, text="Sensor 3", font=("Verdana",18))
        ls3.grid(row=2, column=0, sticky=E, pady=4, padx=5)
        #Crea y define Boton para el Sensor 4.
        ls4 = Label(Top, text="Sensor 4", font=("Verdana",18))
        ls4.grid(row=3, column=0, sticky=E, pady=4, padx=5)
        #Crea y define texto y dropdown menu del contador de minutos.
        lsample = Label(self.First, text="Tiempo de muestreo", highlightthickness=0)
        lsample.grid(row=1, column=0)
        self.spin = Spinbox(self.First,  from_= 0, to = 60, wrap = True, width=2, highlightthickness=0, border=0, font=Font(family='Helvetica', size=9, weight='normal'))   
        self.spin.delete(0,"end")
        self.spin.insert(0,5)
        self.spin.grid(row=1,column=1, sticky=W)
        lmin = Label(self.First, text="minutos", highlightthickness=0)
        lmin.grid(row=1, column=1)
        #Crea y define Botones de funciones y manda llamar sus respectivas subrutinas.
        breport = Button(self.First, text="Reporte", width=10, height=2, command=self.report)
        breport.grid(row=2, column=0, padx=35, pady=10)
        bstop = Button(self.First, text="Detener", width=10, height=2, command=self.readFile)
        bstop.grid(row=2, column=1, padx=55, pady=5)
        bresume = Button(self.First, text="Continuar", width=10, height=2,command=self.connectSerial)
        bresume.grid(row=2, column=2, padx=35, pady=5)
        #Asigna contenedor a la pantalla principal (default).
        self.First.grid()


    #Funcion para generar reporte, crea un TopLevel (segunda pantalla que toma el frente cuando aparece)
    #con las opciones para generar el reporte.
    def report(self):
        #Crea y define TopLevel y asigna a Root (Objeto), define en una estructura de grid.
        self.Second = Toplevel(self.master)
        #Crea Label Frame para contener parte de las opciones.
        frame = LabelFrame(self.Second, text="Parametros de reporte")
        frame.grid(row=0, column=0, columnspan=3, padx=15, pady=10)
        #Crea y define el texto de las opciones.
        flab = Label(frame, text="Desde: ")
        flab.grid(row=1 , column=0, pady=0, padx=20)
        tlab = Label(frame, text="hasta: ")
        tlab.grid(row=2 , column=0, pady=10, padx=20)
        #Crea Objeto datetime (declarado en el header).
        d = date.today()
        #Asigna valores obtenidos del Objeto a las varibles internas declaradas en el main.
        dia.set(d.day)
        mes.set(d.month)
        #La funcion ofrece 5 dias de reporte en modo por defecto, en caso de que la diferencia de los
        #dias incluya dos meses distintos esta condicion lo controla restando los dias predeterminados o 
        #agregandoselos a 25 (considerando un mes de 30 dias, 30-5+los dias del mes, ie: request en
        #Febrero 3, 5 dias antes es 29 de Enero :. 30-5=25+3=28, el dia faltante se da porque por
        #simplicidad se considera un mes de 30 dias).
        if d.day > 5:
            ddia.set(d.day-5)
            mmes.set(d.month)
        else:
            ddia.set(25+d.day)
            mmes.set(d.month-1)
        anio.set(d.year)
        #Crea y define Labels para texto de las opciones.
        dlab = Label(frame, text="Dia")
        dlab.grid(row=0, column=1, pady=2, padx=10)
        mlab = Label(frame, text="Mes")
        mlab.grid(row=0, column=2, pady=2, padx=10)
        alab = Label(frame, text="Año")
        alab.grid(row=0, column=3, pady=2, padx=10)
        #Crea y define menus tipo Dropdown de la primera seccion con los valores predeterminados calculados arriba.
        fdia = Spinbox(frame, from_= 0, to = 31, wrap = True, width=4, textvariable=ddia, font=Font(family='Helvetica', size=9, weight='normal'))
        fdia.grid(row=1, column=1, pady=5, padx=10)
        fmes = Spinbox(frame, from_= 0, to = 12, wrap = True, width=4, textvariable=mmes, font=Font(family='Helvetica', size=9, weight='normal'))
        fmes.grid(row=1, column=2, pady=5)
        fanio = Spinbox(frame, from_= 2021, to = 2022, wrap = True, width=4, textvariable=anio, font=Font(family='Helvetica', size=9, weight='normal'))
        fanio.grid(row=1, column=3, pady=5, padx=10)    
        #Crea y define los menus de la segunda seccion.
        sdia = Spinbox(frame, from_= 0, to = 31, wrap = True, width=4, textvariable=dia, font=Font(family='Helvetica', size=9, weight='normal'))
        sdia.grid(row=2 , column=1, pady=5, padx=10)
        smes = Spinbox(frame, from_= 0, to = 12, wrap = True, width=4, textvariable=mes, font=Font(family='Helvetica', size=9, weight='normal'))
        smes.grid(row=2 , column=2, pady=5)
        sanio = Spinbox(frame, from_= 2021, to = 2022, wrap = True, width=4, textvariable=anio, font=Font(family='Helvetica', size=9, weight='normal'))
        sanio.grid(row=2 , column=3, pady=5, padx=10)
        #Crea y define checkboxes para seleccionar que sensores seran incluidos en el reporte (todos por default).
        sen1 = Checkbutton(frame, text = "Sensor 1", variable=s1)
        sen1.grid(row=3, column=0, padx=10, pady=10)
        sen2 = Checkbutton(frame, text = "Sensor 2", variable=s2)
        sen2.grid(row=3, column=1, padx=10, pady=10)
        sen3 = Checkbutton(frame, text = "Sensor 3", variable=s3)
        sen3.grid(row=3, column=2, padx=10, pady=10)
        sen4 = Checkbutton(frame, text = "Sensor 4", variable=s4)
        sen4.grid(row=3, column=3, padx=10, pady=10)
        #Crea y define Botones para cancelar o exportar reporte.
        gen = Button(self.Second, text="Generar", width=10, height=2, command=self.Second.destroy)
        gen.grid(row=2, column=0, padx=10, pady=10)
        cancel = Button(self.Second, text="Cancelar", width=10, height=2, command=self.Second.destroy)
        cancel.grid(row=2, column=2, padx=20, pady=5)
        self.Second.grid()


    #Funcion para leer de la hoja de excel que se paso como argumento para el Objeto.
    def readFile(self):
        #Obtiene y evalua (If) la respuesta de la funcion por errores.
        info = self.requestData()
        if info == 0 or info == None:
            print("Error de respuesta")
        #Agreaga un estampado de tiempo y los valores obtenidos de la funcion llamada.
        else:
            #Crea Objeto para contener el tiempo, crea una lista con el tiempo en formato y le concatena la respuesta.
            d = dtime.now()
            feta = ["{}".format(d.strftime("%y-%m-%d %H:%M:%S"))]
            feta += info
            #Agrega la linea a la hoja de excel, guarda los cambios del libro, llama funcion para graficar y threading.
            self.sheet.append(feta)
            self.wb.save("Hola.xlsx")
            self.updateGraph()
            self.threading()


    #Funcion para establecer comunicacion con Arduino usando el Objeto de serial creado al inicio.
    def connectSerial(self):
        #Crea Toplevel y Label Frame para contener parte de las opciones.
        self.ConnectWindow = Toplevel(self.master, height=500, width= 500)
        frame = LabelFrame(self.ConnectWindow, text="Puertos disponibles")
        frame.grid(row=0, column=0, columnspan=3, sticky=N+S+E+W, padx=15, pady=10)
        #Cierra cualquier coneccion abierta para evitar problemas.
        self.ser.close()
        #Crea una lista de Python con el retorno de la funcion llamada, obtiene y almacena datos obtenidos.
        ports = list(serial.tools.list_ports.comports())
        self.items = StringVar()
        self.portsDict = {x.description:x.name for x in ports}
        self.items.set([x.description for x in ports])
        #Crea Listbox para los puertos disponibles.
        self.list = Listbox(frame, listvariable=self.items, width=35)
        self.list.select_set(0)
        self.list.grid(row=0, column=0, sticky=N+S+E+W, padx=15, pady=10)
        #Crea Botones para controlar las funciones.
        cncel = Button(self.ConnectWindow, text="Cancelar", width=10, height=2, command=self.ConnectWindow.destroy)
        cncel.grid(row=1, column=0, padx=30, pady=10)
        connect = Button(self.ConnectWindow, text="Connectar", width=10, height=2, command=self.Connect)
        connect.grid(row=1, column=2, padx=30, pady=10)
        #Configura el Toplevel en la pantalla.
        self.ConnectWindow.grid()


    #Funcion para connectarse al puerto seleccionado.
    def Connect(self):
        #Evalua si la seleccion actual esta vacia, si es valida abre el puerto con esa descripcion.
        if self.list.get(ACTIVE) == None:
            return 
        else:
            self.ser.port=self.portsDict[self.list.get(ACTIVE)]
        #Intenta abrir el puerto y validar el Arduino, de responder correctamente llama la subrutina y cierra la ventana.
        try:
            self.ser.open()
            if self.validateSerial() < 0:
                self.ConnectWindow.destroy()
                raise Exception("Arduino no validado") 
            else:
                messagebox.showinfo("Autentificacion satisfactoria","Mensaje de autentificacion validado correctamente")
                self.readFile()
                self.ConnectWindow.destroy()
        #De no poder abrir el puerto crea mensaje de alerta y cierra la ventana.
        except:
            messagebox.showerror("Puerto Serial no reconocido", "El puerto seleccionado no produce respuesta de autentificacion")
            self.ConnectWindow.destroy()


    #Funcion para pedir informacion al Arduino.
    def requestData(self):        
        #Limpia buffer, manda solicitud; lee y evalua respuesta, si es satiscatoria lee los datos y los regresa.
        
        self.ser.write(b'R')
        answer = self.ser.read().decode()
        if answer == 'E':            
            data = [float(self.ser.readline().decode('UTF-8')[:-2]) for x in range(4)]
            if "nan" in data:
                return 0
            return data
        return 0       


    #Funcion para pedir autorizacion.
    def validateSerial(self):
        count = 0
        #Limpia buffer, manda solicitud; lee, decodifica y evalua respuesta, si es satiscatoria retorna positivo.
        while True:
            ser.write(b'O')
            data = ser.read().decode()
            if data == 'K':
                break
            else:
                if count >3:
                    return -1
                
        return 1
    

    #Funcion para comenzar Hilo de espera.
    def threading(self):
        #Crea Hilo con la funcion esperando el valor del spinbox por una constante, inicia el hilo.
        self.t1=Thread(target=self.master.after(int(self.spin.get())*60000, self.readFile))
        self.t1.start()


    #Funcion para actualizar datos.
    def updateGraph(self):
        #Lee los ultimos 10 valores en cada columna de la hoja de excel (comprehension list).
        self.sensor1 = [a.value for a in self.sheet['B'][-10:-1]]
        self.sensor2 = [a.value for a in self.sheet['C'][-10:-1]]
        self.sensor3 = [a.value for a in self.sheet['D'][-10:-1]]
        self.sensor4 = [a.value for a in self.sheet['E'][-10:-1]]
        #Limpia el contenedor de las graficas.
        self.fig.clf()
        #Agrega las graficas al contenedor, las dibuja y configura en la pantalla.
        self.s1 = self.fig.add_subplot(4, 1, 1, frameon=False).plot([x for x in range(len(self.sensor1))], self.sensor1, 'b')
        self.s2 = self.fig.add_subplot(4, 1, 2, frameon=False).plot([x for x in range(len(self.sensor2))], self.sensor2, 'r')
        self.s3 = self.fig.add_subplot(4, 1, 3, frameon=False).plot([x for x in range(len(self.sensor3))], self.sensor3, 'g')
        self.s4 = self.fig.add_subplot(4, 1, 4, frameon=False).plot([x for x in range(len(self.sensor4))], self.sensor4)
        self.cs1.draw()
        self.cs1.get_tk_widget().grid(row=0, column=1, rowspan=4, sticky=E)
        #Actualiza valores en Labels.    
        self.sLabel1['text'] = str(self.sensor1[-1])+"*"
        self.sLabel2['text'] = str(self.sensor2[-1])+"*"
        self.sLabel3['text'] = str(self.sensor3[-1])+"*"
        self.sLabel4['text'] = str(self.sensor4[-1])+"*"
      

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
mmes = IntVar()
anio = IntVar()
wb = load_workbook(filename = 'hola.xlsx')  

gui = UI(root, wb, ser)
root.mainloop()