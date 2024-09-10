# Nombre: ProgramaPlaca.py

# Autor: César Navarro Ramo

# Descripción:
# Este es el programa que gobierna el funcionamiento de la Raspberry Pi


# Importar las bibliotecas necesarias
import tkinter as tk
import smbus
import time
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# --- INICIALIZACIÓN DE TKINTER ---
# Crear una ventana de Tkinter
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

screen_width = screen_width-5
screen_height = screen_height-10

root.geometry(f"{screen_width}x{screen_height}+0+0")
root.title("Lectura de presiones perfil NACA")

#IMÁGENES DEL ENCABEZADO
#Se abren las imágenes
imagen_unizar = tk.PhotoImage(file = "unizar.png")
imagen_eupt = tk.PhotoImage(file = "eupt.png")
imagen_depto = tk.PhotoImage(file = "depto.png")

#Se redimensionan en caso de ser necesario
imagen_eupt = imagen_eupt.subsample(3,3)
imagen_depto = imagen_depto.subsample(3,3)

#Se las asigna a una etiqueta
label_unizar = tk.Label(image = imagen_unizar)
label_eupt = tk.Label(image = imagen_eupt)
label_depto = tk.Label(image = imagen_depto)

#Se representan
#label_unizar.pack(side = "left", padx = 1)
label_eupt.pack(side = "top", padx = 1)
#label_depto.pack(side = "left", padx = 1)


# Crear ocho subplots para los gráficos
fig, axs = plt.subplots(2, 4, figsize=(20, 6))
fig.suptitle("Lecturas de Sensores")
plt.rcParams.update({'font.size': 8})

# Inicializar listas para almacenar datos de sensores
sensor_data = [[] for _ in range(8)]
sensor_data_display = [[] for _ in range(8)]


# --- INICIALIZACIÓN DEL I2C ---

# Dirección I2C del sensor SDP810 (puedes cambiarla según tus conexiones)
SDP_I2C_ADDRESS=0x25
address=0x25

# Dirección del multiplexor
multiplexer=0x70

# Direcciones de los canales del multiplexor
channel_array=[0b00000001,0b00000010,0b00000100,0b00001000,0b00010000,0b00100000,0b01000000,0b10000000]
cha_1 = 0b00000001
# Inicializar el bus I2C
bus=smbus.SMBus(1) #The default i2c bus

#--- RUTINA DE STARTUP SENSORES DE PRESIÓN ---

# Configurar el sensor SDP810
for i in range(8):
    print ("---STARTING UP SENSOR "+str(i+1)+ "---")
    
    #bus=smbus.SMBus(1) #The default i2c bus
    
    #Se selecciona el canal en el multiplexor
    print("    Selecting channel "+str(i+1))
    bus.write_byte_data(multiplexer,0,channel_array[i])
    time.sleep(0.2)
    
    #Se para una posible medición continua que puediera estar haciendo el sensor
    print("    Stopping possible messurements ")
    bus.write_i2c_block_data(SDP_I2C_ADDRESS, 0x3F, [0xF9])
    time.sleep(0.2)

#Start Continuous Measurement (5.3.1 in Data sheet)

    ##Command code (Hex)        Temperature compensation            Averaging
    ##0x3603                    Mass flow                           Average  till read
    ##0x3608                    Mass flow None                      Update rate 0.5ms
    ##0x3615                    Differential pressure               Average till read
    ##0x361E                    Differential pressure None          Update rate 0.5ms

    #Se inicializa el sensor para que comience una medición de presión diferencial
    print("    Selecting averrage till read")
    bus.write_i2c_block_data(address, 0x36, [0X15]) # The command code 0x3603 is split into two arguments, cmd=0x36 and [val]=0x03
    time.sleep(0.5)
    
    print("---Succesfully started---")

#--- FIN DE RUTINA DE STARTUP ---


# Función que lee los datos del sensor SDP810
def update_sensor_data():
    
    
    for i in range(8):#cambiar 2 por 8 para leer todos los sensores
        axs[i // 4, i % 4].clear()
        axs[i // 4, i % 4].plot(sensor_data[i], label=f"Sensor {i+1}")
        axs[i // 4, i % 4].set_title(f"Sensor {i+1}")
        axs[0,0].set_ylabel("Valor")
        axs[1,0].set_ylabel("Valor")
        #axs[i // 4, i % 4].legend()
        axs[i // 4, i % 4].set_xlim([0,50])
        axs[i // 4, i % 4].set_ylim([-50,250])
        time.sleep(0.1)
 
        #Se selecciona el canal que se va a leer
        bus.write_byte(multiplexer,channel_array[i])
        #time.sleep(0.1)
        
        #Se realiza la medición
        reading=bus.read_i2c_block_data(SDP_I2C_ADDRESS,0,9)
        
        
        #---PRESION---
        pressure_value=reading[0]+float(reading[1])/255
        
        if pressure_value>=0 and pressure_value<128:
            diffirential_pressure=pressure_value*256/60 #scale factor adjustment
            
        elif pressure_value>128 and pressure_value<=256:
            diffirential_pressure=-(256-pressure_value)*256/60 #scale factor adjustment
            
        elif pressure_value==128:
            diffirential_pressure=99999999 #Out of range
        print("Diffirential Pressure"+str(i+1)+": "+str(diffirential_pressure)+" PA")
       
        
       
       #---TEMPERATURA---
        temp_value=reading[3]+float(reading[4])/255
        
        if temp_value>=0 and temp_value<=100:
            temperature=temp_value*255/200 #scale factor adjustment
            
        if temp_value<=256 and temp_value>=200:
            temperature=-(256-temp_value)*255/200 #scale factor adjustment
        #print("Temperature: "+str(temperature)+" Degrees Celcius")
       
        #print(reading[0], reading[1])
       
        sensor_data[i].append(diffirential_pressure)  # Datos del sensor i
        sensor_data[i] = sensor_data[i][-50:]  # Limitar a los últimos 50 valores
        
        sensor_data_display[i].append(diffirential_pressure)  # Datos del sensor i
        sensor_data_display[i] = sensor_data[i][-5:]  # Limitar a los últimos 50 valores
        
        #for j in range 5:
        #display[i] = sum(sensor_data_display[i])/5
            
        #print("Diffirential Pressure"+str(i+1)+": "+str(display[i])+" PA")

        #pressure_diff_values[i].append(diffirential_pressure)
        #temperature_values[i].append(temperature)
        

    
    canvas.draw()  # Actualizar la ventana
    root.after(10, update_sensor_data)  # Programar la próxima actualización para dentro de 1 segundo



# Crear listas para almacenar los datos
pressure_diff_values = [],[]
temperature_values = [],[]

#--- CICLO DEL PROGRAMA ---

# Configurar el canvas de Matplotlib en la ventana de Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Iniciar la actualización de los datos de los sensores
root.after(10, update_sensor_data)

# Iniciar el bucle principal de Tkinter
root.mainloop()