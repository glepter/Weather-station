from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from datetime import date
from openpyxl import load_workbook
from openpyxl.utils import *
import serial.tools.list_ports
import serial

#Crea Objeto de comunicacion serial (para conectar con Arduino), lo llamamos: ser
ser = serial.Serial()

#Creamos clase para Objeto que gemera y maneja la UI(Interfaz de Usuario) y funcionalidad
class UI:
    #Inicializacion del objeto, requiere una hoja de excel como entrada, la llamamos: a
    def __init__(self, master, a):
        #crea objeto Tk y pone titulo a la ventana; asigna hoja de excel de la entrada a variable interna del Objeto
        self.sheet = a
        self.master = master
        self.master.title("Interfaz")

        #Crea un contenedor para la pagina principal (Frame)
        self.First = Frame(self.master)

        #Crea contenedor LabelFrame dentro del contenedor (self.First). Lo estructura en un grid definiendo posicion y espacios internos y externos
        Top = LabelFrame(self.First, text="Lectura de sensores", bd=2)
        Top.grid(columnspan=5, padx=10, pady=15, ipadx=2, ipady=2)

        #Crea Boton y Canvas que se usara como fondo para la grafica del sensor 1, los estructura dentro del grid y los define
        bs1 = Button(Top, text="Sensor 1", width=10, height=2,  highlightthickness=0,  command=self.master.destroy)
        bs1.grid(row=0, column=0, sticky=E, pady=4, padx=5)
        cs1 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs1.grid(row=0, column=1,  columnspan=2, sticky=W, padx=5)

        #Crea y define Boton y Canvas para el Sensor 2
        bs2 = Button(Top, text="Sensor 2", width=10, height=2, highlightthickness=0, command=self.master.destroy)
        bs2.grid(row=1, column=0, sticky=E, pady=4, padx=5)
        cs2 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs2.grid(row=1, column=1,  columnspan=2, sticky=W, padx=5)

        #Crea y define Boton y Canvas para el Sensor 3
        bs3 = Button(Top, text="Sensor 3", width=10, height=2, highlightthickness=0, command=self.master.destroy)
        bs3.grid(row=2, column=0, sticky=E, pady=4, padx=5)
        cs3 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs3.grid(row=2, column=1,  columnspan=2, sticky=W, padx=5)

        #Crea y define Boton y Canvas para el Sensor 4
        bs4 = Button(Top, text="Sensor 4", width=10, height=2, highlightthickness=0, command=self.master.destroy)
        bs4.grid(row=3, column=0, sticky=E, pady=4, padx=5)
        cs4 = Canvas(Top, bg='black', width=300, height=40, highlightthickness=0)
        cs4.grid(row=3, column=1,  columnspan=2, sticky=W, padx=5)

        #Crea y define texto y dropdown menu con los numeros
        lsample = Label(self.First, text="Tiempo de muestreo", highlightthickness=0)
        lsample.grid(row=1, column=0)
        spin = Spinbox(self.First,  from_= 0, to = 60, wrap = True, width=2, highlightthickness=0, border=0, font=Font(family='Helvetica', size=9, weight='normal'))   
        spin.grid(row=1,column=1, sticky=W)
        lmin = Label(self.First, text="minutos", highlightthickness=0)
        lmin.grid(row=1, column=1)

        #Crea y define Botones de funciones y manda llamar sus respectivas subrutinas
        breport = Button(self.First, text="Reporte", width=10, height=2, command=self.report)
        breport.grid(row=2, column=0, padx=10, pady=10)
        bstop = Button(self.First, text="Detener", width=10, height=2, command=self.readFile)
        bstop.grid(row=2, column=1, padx=20, pady=5)
        bresume = Button(self.First, text="Continuar", width=10, height=2,command=self.readSerial)
        bresume.grid(row=2, column=2, padx=10, pady=5)

        #Asigna contenedor a la pantalla principal (default)
        self.First.grid()

    #Funcion para generar reporte, crea un TopLevel (segunda pantalla que toma el frente cuando aparece)
    #con las opciones para generar el reporte 
    def report(self):
        #Crea y define TopLevel y asigna a Root (Objeto), define en una estructura de grid
        self.Second = Toplevel(self.master)
        #Crea Label Frame para contener parte de las opciones
        frame = LabelFrame(self.Second, text="Parametros de reporte")
        frame.grid(row=0, column=0, columnspan=3, padx=15, pady=10)

        #Crea y define el texto de las opciones
        flab = Label(frame, text="Desde: ")
        flab.grid(row=1 , column=0, pady=0, padx=20)
        tlab = Label(frame, text="hasta: ")
        tlab.grid(row=2 , column=0, pady=10, padx=20)
        
        #Crea Objeto datetime (declarado en el header)
        d = date.today()
        #Asigna valores obtenidos del Objeto a las varibles internas declaradas en el main
        dia.set(d.day)
        mes.set(d.month)
        #La funcion ofrece 5 dias de reporte en modo por defecto, en caso de que la diferencia de los
        #dias incluya dos meses distintos esta condicion lo controla restando los dias predeterminados o 
        #agregandoselos a 25 (considerando un mes de 30 dias, 30-5+los dias del mes, ie: request en
        #Febrero 3, 5 dias antes es 29 de Enero :. 30-5=25+3=28, el dia faltante se da porque por
        #simplicidad se considera un mes de 30 dias)
        if d.day > 5:
            ddia.set(d.day-5)
            mmes.set(d.month)
        else:
            ddia.set(25+d.day)
            mmes.set(d.month-1)
        anio.set(d.year)

        #Crea y define Labels para texto de las opciones
        dlab = Label(frame, text="Dia")
        dlab.grid(row=0, column=1, pady=2, padx=10)
        mlab = Label(frame, text="Mes")
        mlab.grid(row=0, column=2, pady=2, padx=10)
        alab = Label(frame, text="Año")
        alab.grid(row=0, column=3, pady=2, padx=10)

        #Crea y define menus tipo Dropdown de la primera seccion con los valores predeterminados calculados arriba
        fdia = Spinbox(frame, from_= 0, to = 31, wrap = True, width=4, textvariable=ddia, font=Font(family='Helvetica', size=9, weight='normal'))
        fdia.grid(row=1, column=1, pady=5, padx=10)
        fmes = Spinbox(frame, from_= 0, to = 12, wrap = True, width=4, textvariable=mmes, font=Font(family='Helvetica', size=9, weight='normal'))
        fmes.grid(row=1, column=2, pady=5)
        fanio = Spinbox(frame, from_= 2021, to = 2022, wrap = True, width=4, textvariable=anio, font=Font(family='Helvetica', size=9, weight='normal'))
        fanio.grid(row=1, column=3, pady=5, padx=10)
        
        #Crea y define los menus de la segunda seccion
        sdia = Spinbox(frame, from_= 0, to = 31, wrap = True, width=4, textvariable=dia, font=Font(family='Helvetica', size=9, weight='normal'))
        sdia.grid(row=2 , column=1, pady=5, padx=10)
        smes = Spinbox(frame, from_= 0, to = 12, wrap = True, width=4, textvariable=mes, font=Font(family='Helvetica', size=9, weight='normal'))
        smes.grid(row=2 , column=2, pady=5)
        sanio = Spinbox(frame, from_= 2021, to = 2022, wrap = True, width=4, textvariable=anio, font=Font(family='Helvetica', size=9, weight='normal'))
        sanio.grid(row=2 , column=3, pady=5, padx=10)

        #Crea y define checkboxes para seleccionar que sensores seran incluidos en el reporte (todos por default)   
        sen1 = Checkbutton(frame, text = "Sensor 1", variable=s1)
        sen1.grid(row=3, column=0, padx=10, pady=10)
        sen2 = Checkbutton(frame, text = "Sensor 2", variable=s2)
        sen2.grid(row=3, column=1, padx=10, pady=10)
        sen3 = Checkbutton(frame, text = "Sensor 3", variable=s3)
        sen3.grid(row=3, column=2, padx=10, pady=10)
        sen4 = Checkbutton(frame, text = "Sensor 4", variable=s4)
        sen4.grid(row=3, column=3, padx=10, pady=10)


        #Crea y define Botones para cancelar o exportar reporte
        gen = Button(self.Second, text="Generar", width=10, height=2, command=self.Second.destroy)
        gen.grid(row=2, column=0, padx=10, pady=10)
        cancel = Button(self.Second, text="Cancelar", width=10, height=2, command=self.Second.destroy)
        cancel.grid(row=2, column=2, padx=20, pady=5)
        self.Second.grid()

    #Funcion para leer de la hoja de excel que se paso como argumento para el Objeto
    def readFile(self):
        #Agreaga valores obtenidos de la funcion llamada
        self.sheet.append(self.requestData())

        #TODO: Agregar script para salvar informacion, cerrar y abrir nuevamente Obejeto excel

    #Funcion para establecer comunicacion con Arduino usando el Objeto de Serial creado al inicio
    def readSerial(self):
        #Crea una lista de Python con el retorno de la funcion llamada (se declaro arriba), la llama ports
        ports = list(serial.tools.list_ports.comports())
        #Itera por todos los posibles puertos Seriales que esten conectados a la computadora (lista ports)
        for p in ports:
            #Obtiene el nombre del dispositivo conectado al puerto que se esta iterando, lo nombra a
            a=str(p.name)
            #Si el dispositivo tiene la palabra "Arduino" en la descripcion hace coneccion con ese puerto
            if "Arduino" in p.description:
                ser.port=a
                try: 
                    ser.open()
                    print(ser.is_open)
                except:
                    print("Puerto ocupado")
            else:
                print("Dispositivo no encontrado")
            #TODO:Crear condicion para controlar en caso de que haya mas de un Arduino conectado
    #Funcion para crear conexion y solicitar informacion a un Arduino conectado por Serial
    def requestData(self):
        #Llama funcion que crea conexion con un Arduino
        self.readSerial()

        #TODO: Add function to request data from serial conecction (Arduino will need to have the serial client program loaded)

        #Cierra conexion Serial
        ser.close()

        #Valores provisionales, seran sustituidos por el 'todo' anterior
        data = ['a', 'b', 'c', 'd']
        #Regresa los valores
        return data

         


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
sheet = wb.active


gui = UI(root, sheet)
root.mainloop()