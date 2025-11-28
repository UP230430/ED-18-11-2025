import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EulerMejoradoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Euler Mejorado (Heun) - [t vs x]")
        self.root.geometry("950x650")

        # --- Frame de Entrada de Datos ---
        input_frame = ttk.LabelFrame(root, text="Parámetros - Euler Mejorado", padding="10")
        input_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Variables de control (Valores por defecto adaptados a t y x)
        self.func_str = tk.StringVar(value="t - x + 2") # Ejemplo: f(t,x)
        self.t0_val = tk.DoubleVar(value=0.0) # Antes x0
        self.x0_val = tk.DoubleVar(value=2.0) # Antes y0
        self.h_val = tk.DoubleVar(value=0.1)
        self.tf_val = tk.DoubleVar(value=1.0) # Antes xf

        # Grid de inputs
        ttk.Label(input_frame, text="dx/dt = f(t,x):").grid(row=0, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.func_str, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="t inicial (t0):").grid(row=0, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.t0_val, width=8).grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="x inicial (x0):").grid(row=1, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.x0_val, width=8).grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(input_frame, text="Paso (h):").grid(row=1, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.h_val, width=8).grid(row=1, column=3, padx=5)

        ttk.Label(input_frame, text="t final:").grid(row=1, column=4, sticky="e")
        ttk.Entry(input_frame, textvariable=self.tf_val, width=8).grid(row=1, column=5, padx=5)

        ttk.Button(input_frame, text="CALCULAR", command=self.calcular_heun).grid(row=0, column=6, rowspan=2, padx=20)

        #help_lbl = ttk.Label(input_frame, text="Sintaxis Python: t**2, sin(t), exp(x), etc. (Usar 't' y 'x')",
                            # font=("Arial", 8, "italic"), foreground="gray")
        #help_lbl.grid(row=2, column=0, columnspan=7, pady=5)

        # --- Resultados ---
        results_frame = ttk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Tabla
        table_frame = ttk.LabelFrame(results_frame, text="Tabla de Iteraciones")
        table_frame.pack(side="left", fill="y", padx=5)

        columns = ("n", "t", "x_aprox")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        self.tree.heading("n", text="Iter")
        self.tree.heading("t", text="t (tiempo)")
        self.tree.heading("x_aprox", text="x (Mejorado)")

        self.tree.column("n", width=40, anchor="center")
        self.tree.column("t", width=80, anchor="center")
        self.tree.column("x_aprox", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Gráfica
        graph_frame = ttk.LabelFrame(results_frame, text="Gráfica")
        graph_frame.pack(side="right", fill="both", expand=True, padx=5)

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def evaluar_funcion(self, expr, t, x):
        """ Evalúa f(t, x) """
        allowed = {"sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
                   "pi": np.pi, "e": np.e}
        # IMPORTANTE: Diccionario adaptado para recibir t y x
        return eval(expr, {"__builtins__": None}, {**allowed, 't': t, 'x': x})

    def calcular_heun(self):
        # Limpieza
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax.clear()

        try:
            f_str = self.func_str.get()
            t0 = self.t0_val.get()
            x0 = self.x0_val.get()
            h = self.h_val.get()
            tf = self.tf_val.get()

            if h <= 0:
                messagebox.showerror("Error", "h debe ser > 0")
                return
            if tf <= t0:
                messagebox.showerror("Error", "t final debe ser mayor que t inicial")
                return

            # Inicialización
            ts = [t0]
            xs = [x0]
            t = t0
            x = x0
            n = 0

            self.tree.insert("", "end", values=(n, f"{t:.4f}", f"{x:.6f}"))

            # --- BUCLE PRINCIPAL (Lógica Euler Mejorado con t y x) ---
            while t < tf - 1e-9:
                # 1. Calcular k1 (Pendiente al inicio) -> f(t_n, x_n)
                k1 = self.evaluar_funcion(f_str, t, x)

                # 2. Predecir el siguiente punto (Euler simple) -> x_star (antes y_star)
                # x* = x_n + h * k1
                x_star = x + h * k1

                # 3. Calcular el tiempo siguiente
                t_next = t + h

                # 4. Calcular k2 (Pendiente al final estimado usando t_next y x_star)
                k2 = self.evaluar_funcion(f_str, t_next, x_star)

                # 5. Corrector (Promedio de pendientes)
                pendiente_promedio = (k1 + k2) / 2
                x_next = x + h * pendiente_promedio

                # Actualizar valores reales
                t = t_next
                x = x_next
                n += 1

                # Guardar y mostrar
                ts.append(t)
                xs.append(x)
                self.tree.insert("", "end", values=(n, f"{t:.4f}", f"{x:.6f}"))

            # Graficar
            self.ax.plot(ts, xs, 'g-o', label='Euler Mejorado (Heun)', markersize=4)
            self.ax.set_title(f"Solución: {f_str}")
            self.ax.set_xlabel("Tiempo (t)")
            self.ax.set_ylabel("Estado (x)")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Error de cálculo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EulerMejoradoApp(root)
    root.mainloop()
