import numpy as np 
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from sympy import sympify, lambdify, symbols

# FUNCIÓN: Aproxima una integral usando el método del trapecio.
def integral_trapecios(f, a, b, n):
    x_vals = np.linspace(a, b, n + 1) # Genera n+1 puntos equidistantes entre a y b.
    y_vals = f(x_vals) # Evalúa la función en todos esos puntos.
    h = (b - a) / n # Distancia entre cada punto.
    area = (h / 2) * (y_vals[0] + 2 * sum(y_vals[1:-1]) + y_vals[-1]) # Fórmula del método del trapecio.
    return area, x_vals, y_vals # Regresa: área calculada + los puntos evaluados.

# FUNCIÓN: Grafica la función y los trapecios utilizados.
def graficar(f, a, b, x_vals, y_vals, area):

    plt.figure(figsize=(9, 6))  # Tamaño de la figura.

    x_smooth = np.linspace(a, b, 400) # Curva suave de la función para una mejor visualización.
    plt.plot(x_smooth, f(x_smooth), label='f(x)', color='blue', linewidth=2)

    for i in range(len(x_vals)-1): # Dibuja cada trapecio en color rojo.
        # Coordenadas x y y del trapecio.
        xs = [x_vals[i], x_vals[i], x_vals[i+1], x_vals[i+1]]
        ys = [0, y_vals[i], y_vals[i+1], 0]

        plt.fill(xs, ys, color='red', alpha=0.4) # Rellena la figura.

    # Muestra el valor del área dentro de un cuadro en la gráfica.
    plt.text(
        0.05, 0.95,
        f"Área aproximada = {area:.6f}",
        transform=plt.gca().transAxes,
        fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle="round", fc="white", ec="black")
    )

    # Estética general de la gráfica.
    plt.title('Integral aproximada con método del trapecio')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()
    plt.show()

# FUNCIÓN: Se ejecuta al presionar el botón "Calcular integral".
def ejecutar():
    try:   
        x = symbols('x') # Prepara un símbolo de SymPy para representar x.
        f_expr = sympify(entry_funcion.get()) # Convierte el texto ingresado por el usuario a una expresión matemática.
        f = lambdify(x, f_expr, 'numpy') # Convierte la expresión simbólica en una función evaluable por numpy.

        # Obtiene los valores ingresados por el usuario
        a = float(entry_a.get())
        b = float(entry_b.get())
        n = int(entry_n.get())

        
        area, x_vals, y_vals = integral_trapecios(f, a, b, n) # Calcula el área y los puntos evaluados.
        
        text_output.delete("1.0", tk.END) # Limpia el cuadro de texto y escribe el resultado.
        text_output.insert(tk.END, f"Área aproximada: {area:.6f}\n")
        graficar(f, a, b, x_vals, y_vals, area) # Muestra la gráfica.

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}") # Muestra un mensaje de error si algo sale mal.

# INTERFAZ GRÁFICA (TKINTER)
ventana = tk.Tk() # Crea la ventana principal.
ventana.title("Integral por método del trapecio")
ventana.geometry("600x550")

tk.Label(ventana, text="Función f(x):").pack() # Campo para ingresar la función f(x).
entry_funcion = tk.Entry(ventana, width=40)
entry_funcion.insert(0, "sin(x)")  # Valor por defecto.
entry_funcion.pack()

tk.Label(ventana, text="Límite inferior a:").pack() # Campo para el límite inferior.
entry_a = tk.Entry(ventana)
entry_a.insert(0, "0")
entry_a.pack()

tk.Label(ventana, text="Límite superior b:").pack() # Campo para el límite superior.
entry_b = tk.Entry(ventana)
entry_b.insert(0, "3.1416")
entry_b.pack()

tk.Label(ventana, text="Número de trapecios:").pack() # Campo para la cantidad de trapecios.
entry_n = tk.Entry(ventana)
entry_n.insert(0, "10")
entry_n.pack()

tk.Button(ventana, text="Calcular integral", command=ejecutar, bg="lightgreen").pack(pady=10) # Botón que ejecuta el cálculo.

tk.Label(ventana, text="Resultados:").pack() # Área donde se muestran los resultados numéricos.
text_output = tk.Text(ventana, height=10, width=70)
text_output.pack()

ventana.mainloop() # Inicia la aplicación.