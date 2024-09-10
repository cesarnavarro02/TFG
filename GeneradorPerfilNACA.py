# Nombre: GeneradorPerfilNACA.py

# Autor: César Navarro Ramo

# Descripción:
# Este programa genera un archivo ".stl" en el cual se encuentra el perfil NACA
# cuatro dígitos del código que ha sido introducido por el usuario.



import numpy as np
import matplotlib.pyplot as plt

print('Introduzca el código del perfil NACA deseado: ')
codigo = input()

m = float(codigo[0]) / 100.0
p = float(codigo[1]) / 10.0
t = float(codigo[2:]) / 100.0

n = 10000  # número de puntos evaluados
x = np.linspace(0, 1, n)  # Se crea el eje x

# Cálculo de las coordenadas del perfil con respecto a la cuerda
yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)

if p == 0:  # Caso de perfil simétrico
    xu, yu = x, yt
    xd, yd = x, -yt
    
else:  # Caso de perfil asimétrico
    xc1 = x[x <= p]
    xc2 = x[x > p]
    yc1 = m / p**2 * xc1 * (2 * p - xc1)
    yc2 = m / (1 - p)**2 * (1 - 2 * p + xc2) * (1 - xc2)
    yc = np.concatenate((yc1, yc2))
    dyc_dx = np.concatenate((2 * m / p**2 * (p - xc1), 2 * m / (1 - p)**2 * (p - xc2)))
    theta = np.arctan(dyc_dx)
    xu, yu = x - yt * np.sin(theta), yc + yt * np.cos(theta)
    xd, yd = x + yt * np.sin(theta), yc - yt * np.cos(theta)


#Como no cierra el perfil por comleto se añade un punto para cerrarlo
xu = np.append(xu,1.01) 
yu = np.append(yu,0)
xd = np.append(xd,1.01)
yd = np.append(yd,0)



#Coordenada z de la cara1
z1u = np.zeros(n+1)
z1d = np.zeros(n+1)

#Coordenada z de la cara2
z2u = np.ones(n+1)
z2d = np.ones(n+1)

plt.axis('equal')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(False)    
plt.plot(xu,yu,'gray')
plt.plot(xd,yd,'gray')



#Se le da nombre al archivo
nombre_archivo = "NACA_"+codigo+".stl"

# Crear un archivo STL básico con una malla triangular
with open(nombre_archivo, 'w') as stl_file:
    stl_file.write("solid PERFIL\n")
    
    
    #Triangulos superiores cara1
    for i in range(n): 
        
        p1 = np.array([xu[i],yu[i],z1u[i]])
        p2 = np.array([xu[i+1],yu[i+1],z1u[i+1]])
        p3 = np.array([xd[i],yd[i],z1d[i]])
            
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
    #Triangulos superiores cara2
    for i in range(n):       
        p1 = np.array([xu[i],yu[i],z2u[i]])
        p2 = np.array([xu[i+1],yu[i+1],z2u[i+1]])
        p3 = np.array([xd[i],yd[i],z2d[i]])
            
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
        
        
    #Triangulos inferiores cara1
    for i in range(n):       
        p1 = np.array([xd[i],yd[i],z1d[i]])
        p2 = np.array([xd[i+1],yd[i+1],z1d[i+1]])
        p3 = np.array([xu[i+1],yu[i+1],z1u[i+1]])
            
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
    #Triangulos inferiores cara2
    for i in range(n):
        p1 = np.array([xd[i],yd[i],z2d[i]])
        p2 = np.array([xd[i+1],yd[i+1],z2d[i+1]])
        p3 = np.array([xu[i+1],yu[i+1],z2u[i+1]])
            
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
        
        
        
    #Triangulos transversales superior 1
    for i in range(n):
        
        p1 = np.array([xu[i],yu[i],z1u[i]])
        p2 = np.array([xu[i+1],yu[i+1],z1u[i+1]])
        p3 = np.array([xu[i],yu[i],z2u[i]])
            
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
    #Triangulos transversales superor 2
    for i in range(n):
        
        p1 = np.array([xu[i],yu[i],z2u[i]])
        p2 = np.array([xu[i+1],yu[i+1],z2u[i+1]])
        p3 = np.array([xu[i+1],yu[i+1],z1u[i+1]])
            
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
        
    #Triangulos transversales inferior 1
    for i in range(n):
            
        p1 = np.array([xd[i],yd[i],z1d[i]])
        p2 = np.array([xd[i+1],yd[i+1],z1d[i+1]])
        p3 = np.array([xd[i],yd[i],z2d[i]])
                
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
            
    #Triangulos transversales inferior 2
    for i in range(n):

        p1 = np.array([xd[i],yd[i],z2d[i]])
        p2 = np.array([xd[i+1],yd[i+1],z2d[i+1]])
        p3 = np.array([xd[i+1],yd[i+1],z1d[i+1]])
                
        normal = np.cross((p2 - p1), (p3 - p1))
        stl_file.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
        stl_file.write("  outer loop\n")
        for p in [p1, p2, p3]:
            stl_file.write(f"    vertex {p[0]} {p[1]} {p[2]}\n")
        stl_file.write("  endloop\n")
        stl_file.write("endfacet\n")
        
        
        
    stl_file.write("endsolid MySTLModel\n")