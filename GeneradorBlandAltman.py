# Nombre: GeneradorBlandAltman.py

# Autor: César Navarro Ramo

# Descripción:
# Este programa genera un gráfico Bland-Altman de las mediciones de presión


import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
# Presión 
presion_referencia = np.array([10, 61, 80, 130, 9, 60, 85, 125, 8, 51, 75,113,8,47,72,103,12,65,126,188,9,59,91,156])

# Presión medida por el nuevo sistema
presion_nuevo_sistema = np.array([10, 68, 90, 133, 10, 62, 90, 135,9, 56, 85, 120,9,48,74,108,12,67,123,179,10,60,89,146])

# Crear el diagrama de Bland-Altman
def bland_altman_plot(data1, data2, *args, **kwargs):
    """Genera un gráfico de Bland-Altman"""
    mean = np.mean([data1, data2], axis=0)
    diff = data1 - data2
    md = np.mean(diff)
    sd = np.std(diff, axis=0)

    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md, color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='red', linestyle='--')
    plt.axhline(md - 1.96*sd, color='red', linestyle='--')
    plt.xlabel('Promedio de las dos mediciones')
    plt.ylabel('Diferencia entre las dos mediciones')
    plt.title('Diagrama de Bland-Altman')
    plt.show()

# Llamada a la función para generar el diagrama
bland_altman_plot(presion_referencia, presion_nuevo_sistema)