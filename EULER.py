import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Euler - Solucionador EDO (t vs x)")
        self.root.geometry("900x650")

        # --- Frame de Entrada de Datos ---
        input_frame = ttk.LabelFrame(root, text="Parámetros de Entrada", padding="10")
        input_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Variables de control (Renombradas para contexto t, x)
        # Ecuación por defecto cambiada a términos de t y x
        self.func_str = tk.StringVar(value="t - x + 2")
        self.t0_val = tk.DoubleVar(value=0.0)  # Antes x0
        self.x0_val = tk.DoubleVar(value=2.0)  # Antes y0
        self.h_val = tk.DoubleVar(value=0.1)
        self.tf_val = tk.DoubleVar(value=1.0)  # Antes xf

        # Grid de inputs
        ttk.Label(input_frame, text="Función dx/dt = f(t,x):").grid(row=0, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.func_str, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="t inicial (t0):").grid(row=0, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.t0_val, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="x inicial (x0):").grid(row=1, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.x0_val, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Paso (h):").grid(row=1, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.h_val, width=10).grid(row=1, column=3, padx=5, pady=5)

        # Opcional: Input para t final si deseas habilitarlo en el futuro
        ttk.Label(input_frame, text="t final:").grid(row=1, column=4, sticky="e")
        ttk.Entry(input_frame, textvariable=self.tf_val, width=10).grid(row=1, column=5, padx=5, pady=5)

        # Botón Calcular
        ttk.Button(input_frame, text="CALCULAR", command=self.calcular_euler).grid(row=0, column=6, rowspan=2, padx=20)

        # Nota de ayuda
        help_lbl = ttk.Label(input_frame,
                            # text="Nota: Usa 't' para tiempo y 'x' para la variable dependiente (ej: 2*t - x).",
                             font=("Arial", 8, "italic"), foreground="gray")
        help_lbl.grid(row=2, column=0, columnspan=7, pady=5)

        # --- Frame de Resultados (Gráfica y Tabla) ---
        results_frame = ttk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # -- Sección Tabla --
        table_frame = ttk.LabelFrame(results_frame, text="Tabla de Iteraciones")
        table_frame.pack(side="left", fill="y", padx=5)

        columns = ("n", "t", "x")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        self.tree.heading("n", text="Iter")
        self.tree.heading("t", text="t (tiempo)")
        self.tree.heading("x", text="x (aprox)")
        self.tree.column("n", width=50, anchor="center")
        self.tree.column("t", width=80, anchor="center")
        self.tree.column("x", width=100, anchor="center")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # -- Sección Gráfica --
        graph_frame = ttk.LabelFrame(results_frame, text="Gráfica de la Solución")
        graph_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Inicializar figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def evaluar_funcion(self, expr, t, x):
        """Evalúa la función f(t,x) ingresada como texto."""
        # Diccionario seguro de funciones matemáticas permitidas
        allowed_locals = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }
        try:
            # CAMBIO CLAVE: El contexto ahora define 't' y 'x'
            return eval(expr, {"__builtins__": None}, {**allowed_locals, 't': t, 'x': x})
        except Exception as e:
            raise ValueError(f"Error en la función: {e}")

    def calcular_euler(self):
        # 1. Limpiar datos anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax.clear()

        try:
            # 2. Obtener valores de la GUI
            f_str = self.func_str.get()
            t0 = self.t0_val.get() # Variable independiente
            x0 = self.x0_val.get() # Variable dependiente
            h = self.h_val.get()
            tf = self.tf_val.get() # Tiempo final

            # Validaciones básicas
            if h <= 0:
                messagebox.showerror("Error", "El paso h debe ser positivo.")
                return
            # Se asume que t final es 1.0 por defecto o lo que el usuario quiera configurar
            # Si el usuario no cambia el código, usaremos tf_val que está en 1.0
            if tf <= t0:
                # Si tf no se muestra en la GUI, asumimos un rango por defecto o lanzamos error
                # Para este ejemplo, si tf <= t0, sumaremos 10 pasos automáticamente o pedimos corrección
                tf = t0 + (h * 10)

            # 3. Algoritmo de Euler (Adaptado a t y x)
            ts = [t0]
            xs = [x0]

            t_actual = t0
            x_actual = x0
            n = 0

            # Insertar condición inicial en tabla
            self.tree.insert("", "end", values=(n, f"{t_actual:.4f}", f"{x_actual:.6f}"))

            # Iterar mientras el tiempo actual sea menor al tiempo final
            while t_actual < tf - 1e-9:
                try:
                    # Pendiente depende ahora de t y x
                    pendiente = self.evaluar_funcion(f_str, t_actual, x_actual)
                except ValueError as ve:
                    messagebox.showerror("Error de Sintaxis", str(ve))
                    return

                # Fórmula de Euler: x_new = x_old + h * f(t, x)
                x_siguiente = x_actual + h * pendiente
                t_siguiente = t_actual + h

                # Actualizar variables
                t_actual = t_siguiente
                x_actual = x_siguiente
                n += 1

                # Guardar datos
                ts.append(t_actual)
                xs.append(x_actual)

                # Insertar en tabla
                self.tree.insert("", "end", values=(n, f"{t_actual:.4f}", f"{x_actual:.6f}"))

            # 4. Graficar Resultados
            self.ax.plot(ts, xs, 'r-o', label='Euler Aprox (x vs t)', markersize=4) # Color rojo para diferenciar
            self.ax.set_title(f"Solución de dx/dt = {f_str}")
            self.ax.set_xlabel("Tiempo (t)")
            self.ax.set_ylabel("Estado (x)")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()

            # Refrescar el canvas de matplotlib
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EulerApp(root)
    root.mainloop()
