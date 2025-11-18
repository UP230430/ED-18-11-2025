import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt

def newton_raphson():
    try:
        # Leer entradas del usuario
        funcion_str = entry_funcion.get()
        derivada_str = entry_derivada.get()
        x0 = float(entry_x0.get())
        iter_user = int(entry_iter.get())  # Iteraciones que solicita el usuario

        # Definir f(x) y f'(x) usando eval
        def f(x):
            return eval(funcion_str, {"x": x, "np": np, 
                                      "sin": np.sin, "cos": np.cos, "exp": np.exp,
                                      "log": np.log, "sqrt": np.sqrt})

        def fprima(x):
            return eval(derivada_str, {"x": x, "np": np,
                                       "sin": np.sin, "cos": np.cos, "exp": np.exp,
                                       "log": np.log, "sqrt": np.sqrt})

        # Limpiar consola
        texto_resultados.delete(1.0, tk.END)
        texto_resultados.insert(tk.END, "Iteraciones del método de Newton-Raphson:\n\n")

        iteraciones = [x0]
        convergio_en = None

        for i in range(iter_user):
            fx = f(x0)
            dfx = fprima(x0)

            if dfx == 0:
                messagebox.showerror("Error", "La derivada es cero. No se puede continuar.")
                return

            x1 = x0 - fx / dfx
            iteraciones.append(x1)

            texto_resultados.insert(
                tk.END,
                f"Iteración {i+1}: x = {x1:.6f}, f(x) = {fx:.6f}, f'(x) = {dfx:.6f}\n"
            )

            # Si la función llega cerca de 0, detener
            if abs(f(x1)) < 1e-6:
                convergio_en = i + 1
                texto_resultados.insert(tk.END, "\nRaíz encontrada antes de las iteraciones solicitadas.\n")
                break

            x0 = x1

        # Si convergió antes
        if convergio_en is not None and convergio_en < iter_user:
            texto_resultados.insert(
                tk.END,
                f"\nSolo se necesitaron {convergio_en} iteraciones para llegar a la raíz aproximada.\n"
            )
        else:
            texto_resultados.insert(
                tk.END,
                f"\nSe realizaron las {iter_user} iteraciones solicitadas.\n"
            )

        texto_resultados.insert(tk.END, f"\nRaíz aproximada: {x1:.6f}")

        # --- Gráfica ---
        x_vals = np.linspace(x1 - 5, x1 + 5, 400)
        y_vals = [f(x) for x in x_vals]
        y_deriv = [fprima(x) for x in x_vals]

        plt.figure(figsize=(8,5))
        plt.axhline(0, color='black', lw=1)
        plt.plot(x_vals, y_vals, label=f'f(x) = {funcion_str}', color='blue')
        plt.plot(x_vals, y_deriv, label="f'(x)", color='orange', linestyle='--')
        plt.scatter(iteraciones, [f(x) for x in iteraciones], color='red', label='Iteraciones')
        plt.scatter(x1, f(x1), color='green', s=80, label='Raíz aproximada')
        plt.title("Método de Newton-Raphson")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# --- Interfaz gráfica ---
ventana = tk.Tk()
ventana.title("Método de Newton-Raphson")
ventana.geometry("550x600")

tk.Label(ventana, text="Función f(x):").pack()
entry_funcion = tk.Entry(ventana, width=50)
entry_funcion.insert(0, "x**3 - 6*x**2 + 9*x")  # Ejemplo
entry_funcion.pack()

tk.Label(ventana, text="Derivada f'(x):").pack()
entry_derivada = tk.Entry(ventana, width=50)
entry_derivada.insert(0, "3*x**2 - 12*x + 9")  # Ejemplo
entry_derivada.pack()

tk.Label(ventana, text="Valor inicial x0:").pack()
entry_x0 = tk.Entry(ventana)
entry_x0.insert(0, "2.5")
entry_x0.pack()

tk.Label(ventana, text="¿Cuántas iteraciones desea realizar?").pack()
entry_iter = tk.Entry(ventana)
entry_iter.insert(0, "10")
entry_iter.pack()

tk.Button(ventana, text="Calcular", command=newton_raphson, bg="lightblue").pack(pady=10)

texto_resultados = scrolledtext.ScrolledText(ventana, width=65, height=15)
texto_resultados.pack(padx=10, pady=10)

ventana.mainloop()