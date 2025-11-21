import tkinter as tk
from tkinter import messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


# ----------------- NEWTON RAPHSON PARA UNA RAÍZ -----------------
def newton_all_steps(func_str, deriv_str, x0, iters):
    """Devuelve la raíz y todas las iteraciones para graficar."""
    def f(x):
        return eval(func_str, {"x": x, "np": np})

    def fprima(x):
        return eval(deriv_str, {"x": x, "np": np})

    xs = [x0]

    for _ in range(iters):
        fx = f(x0)
        dfx = fprima(x0)

        if dfx == 0:
            raise ValueError("La derivada se hizo cero. No se puede continuar.")

        x1 = x0 - fx / dfx
        xs.append(x1)

        if abs(f(x1)) < 1e-8:
            return x1, xs

        x0 = x1

    return x1, xs

# ----------------- FUNCIÓN PRINCIPAL -----------------
def calcular_todo():
    try:
        funcion_str = entry_funcion.get()
        derivada_str = entry_derivada.get()
        x0_1 = float(entry_x0_1.get())
        x0_2 = float(entry_x0_2.get())
        iter_user = int(entry_iter.get())

        texto_resultados.delete(1.0, tk.END)
        texto_resultados.insert(tk.END, "=== MÉTODO DE NEWTON PARA LAS DOS RAÍCES ===\n\n")

        # Obtener coeficientes a, b, c automáticamente
        x = sp.Symbol("x")
        pol = sp.sympify(funcion_str)
        pol = sp.expand(pol)

        a = float(pol.coeff(x, 2))
        b = float(pol.coeff(x, 1))
        c = float(pol.coeff(x, 0))

        texto_resultados.insert(tk.END, f"Ecuación característica:\n {a}m² + {b}m + {c} = 0\n\n")

        # Newton para m1
        m1, its1 = newton_all_steps(funcion_str, derivada_str, x0_1, iter_user)
        texto_resultados.insert(tk.END, f"Raíz 1 (m1) usando x0 = {x0_1} → {m1}\n")

        # Newton para m2
        m2, its2 = newton_all_steps(funcion_str, derivada_str, x0_2, iter_user)
        texto_resultados.insert(tk.END, f"Raíz 2 (m2) usando x0 = {x0_2} → {m2}\n\n")

        # Determinar tipo de solución + mostrar m₁ y m₂
        if abs(m1 - m2) < 1e-6:
            caso = "Caso I (Raíz doble)"
            texto_resultados.insert(tk.END, "-> CASO I: Raíz doble\n")
            texto_resultados.insert(
                tk.END,
                f"x(t) = k1 · e^({m1:.6f}·t)  +  t · k2 · e^({m1:.6f}·t)\n"
            )
        else:
            caso = "Caso II (Raíces distintas)"
            texto_resultados.insert(tk.END, "-> CASO II: Raíces distintas\n")
            texto_resultados.insert(
                tk.END,
                f"x(t) = k1 · e^({m1:.6f}·t)  +  k2 · e^({m2:.6f}·t)\n"
            )

        # Reconstrucción de la ecuación diferencial
        texto_resultados.insert(tk.END, "\n=== ECUACIÓN DIFERENCIAL ORIGINAL ===\n")
        texto_resultados.insert(tk.END, f"{a}x'' + {b}x' + {c}x = 0\n\n")

        # Graficar función característica
        xs = np.linspace(-10, 10, 400)
        f_vals = [eval(funcion_str, {"x": x, "np": np}) for x in xs]

        plt.figure(figsize=(8,5))
        plt.axhline(0, color="black")
        plt.plot(xs, f_vals, label="f(m)")
        plt.scatter([m1, m2], [0, 0], color="red", s=80, label="Raíces encontradas")
        plt.title("Función Característica")
        plt.xlabel("m")
        plt.ylabel("f(m)")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Gráfica de iteraciones de Newton para m1
        plt.figure(figsize=(8,5))
        its_f = [eval(funcion_str, {"x": x, "np": np}) for x in its1]
        plt.plot(its1, its_f, marker="o")
        plt.axhline(0, color="black")
        plt.title("Iteraciones Newton - Raíz m1")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True)
        plt.show()

        # Gráfica de iteraciones de Newton para m2
        plt.figure(figsize=(8,5))
        its_f2 = [eval(funcion_str, {"x": x, "np": np}) for x in its2]
        plt.plot(its2, its_f2, marker="o")
        plt.axhline(0, color="black")
        plt.title("Iteraciones Newton - Raíz m2")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True)
        plt.show()

        # Gráfica de la solución diferencial x(t)
        t_vals = np.linspace(0, 10, 300)

        if abs(m1 - m2) < 1e-6:
            m = m1
            x_vals = np.exp(m * t_vals) + t_vals * np.exp(m * t_vals)
        else:
            x_vals = np.exp(m1 * t_vals) + np.exp(m2 * t_vals)

        plt.figure(figsize=(8,5))
        plt.plot(t_vals, x_vals, label="x(t)")
        plt.title(f"Solución de la Ecuación Diferencial ({caso})")
        plt.xlabel("t")
        plt.ylabel("x(t)")
        plt.grid(True)
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


# ----------------- INTERFAZ -----------------
ventana = tk.Tk()
ventana.title("Método de Newton + Ecuación Diferencial Completa")
ventana.geometry("600x750")

tk.Label(ventana, text="Función característica f(m):").pack()
entry_funcion = tk.Entry(ventana, width=50)
entry_funcion.insert(0, "2*x**2 + 8*x - 10")
entry_funcion.pack()

tk.Label(ventana, text="Derivada f'(m):").pack()
entry_derivada = tk.Entry(ventana, width=50)
entry_derivada.insert(0, "4*x + 8")
entry_derivada.pack()

tk.Label(ventana, text="Valor inicial x0 para raíz 1:").pack()
entry_x0_1 = tk.Entry(ventana)
entry_x0_1.insert(0, "-5")
entry_x0_1.pack()

tk.Label(ventana, text="Valor inicial x0 para raíz 2:").pack()
entry_x0_2 = tk.Entry(ventana)
entry_x0_2.insert(0, "5")
entry_x0_2.pack()

tk.Label(ventana, text="Iteraciones:").pack()
entry_iter = tk.Entry(ventana)
entry_iter.insert(0, "20")
entry_iter.pack()

tk.Button(ventana, text="Calcular", command=calcular_todo,
          bg="lightblue").pack(pady=10)

texto_resultados = scrolledtext.ScrolledText(ventana, width=70, height=18)
texto_resultados.pack(padx=10, pady=10)

ventana.mainloop()

