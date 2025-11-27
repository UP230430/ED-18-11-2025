import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class EulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Método de Euler - Solucionador EDO")
        self.root.geometry("900x650")

        # --- Frame de Entrada de Datos ---
        input_frame = ttk.LabelFrame(root, text="Parámetros de Entrada", padding="10")
        input_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Variables de control
        self.func_str = tk.StringVar(value="x - y + 2")  # Ejemplo por defecto
        self.x0_val = tk.DoubleVar(value=0.0)
        self.y0_val = tk.DoubleVar(value=2.0)
        self.h_val = tk.DoubleVar(value=0.1)
        self.xf_val = tk.DoubleVar(value=1.0)

        # Grid de inputs
        ttk.Label(input_frame, text="Función dy/dx = f(x,y):").grid(row=0, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.func_str, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="x inicial (x0):").grid(row=0, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.x0_val, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="y inicial (y0):").grid(row=1, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.y0_val, width=10).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(input_frame, text="Paso (h):").grid(row=1, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.h_val, width=10).grid(row=1, column=3, padx=5, pady=5)

        #ttk.Label(input_frame, text="x final:").grid(row=1, column=4, sticky="e")
        #ttk.Entry(input_frame, textvariable=self.xf_val, width=10).grid(row=1, column=5, padx=5, pady=5)

        # Botón Calcular
        ttk.Button(input_frame, text="CALCULAR", command=self.calcular_euler).grid(row=0, column=6, rowspan=2, padx=20)

        # Nota de ayuda
        help_lbl = ttk.Label(input_frame,
                             #text="Nota: Usa sintaxis Python (ej: x**2 para cuadrado). Funciones disponibles: sin, cos, exp, sqrt, log.",
                             font=("Arial", 8, "italic"), foreground="gray")
        help_lbl.grid(row=2, column=0, columnspan=7, pady=5)

        # --- Frame de Resultados (Gráfica y Tabla) ---
        results_frame = ttk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # -- Sección Tabla --
        table_frame = ttk.LabelFrame(results_frame, text="Tabla de Iteraciones")
        table_frame.pack(side="left", fill="y", padx=5)

        columns = ("n", "x", "y")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        self.tree.heading("n", text="Iter")
        self.tree.heading("x", text="x")
        self.tree.heading("y", text="y (aprox)")
        self.tree.column("n", width=50, anchor="center")
        self.tree.column("x", width=80, anchor="center")
        self.tree.column("y", width=100, anchor="center")

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

    def evaluar_funcion(self, expr, x, y):
        """Evalúa la función f(x,y) ingresada como texto."""
        # Diccionario seguro de funciones matemáticas permitidas
        allowed_locals = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
            "pi": np.pi, "e": np.e
        }
        try:
            # Evalua la expresión string reemplazando x e y por sus valores numéricos
            return eval(expr, {"__builtins__": None}, {**allowed_locals, 'x': x, 'y': y})
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
            x0 = self.x0_val.get()
            y0 = self.y0_val.get()
            h = self.h_val.get()
            xf = self.xf_val.get()

            # Validaciones básicas
            if h <= 0:
                messagebox.showerror("Error", "El paso h debe ser positivo.")
                return
            if xf <= x0:
                messagebox.showerror("Error", "x final debe ser mayor que x inicial.")
                return

            # 3. Algoritmo de Euler
            xs = [x0]
            ys = [y0]

            x_actual = x0
            y_actual = y0
            n = 0

            # Insertar condición inicial en tabla
            self.tree.insert("", "end", values=(n, f"{x_actual:.4f}", f"{y_actual:.6f}"))

            while x_actual < xf - 1e-9:  # 1e-9 para evitar errores de punto flotante
                try:
                    pendiente = self.evaluar_funcion(f_str, x_actual, y_actual)
                except ValueError as ve:
                    messagebox.showerror("Error de Sintaxis", str(ve))
                    return

                # Fórmula de Euler: y_new = y_old + h * f(x, y)
                y_siguiente = y_actual + h * pendiente
                x_siguiente = x_actual + h

                # Actualizar variables
                x_actual = x_siguiente
                y_actual = y_siguiente
                n += 1

                # Guardar datos
                xs.append(x_actual)
                ys.append(y_actual)

                # Insertar en tabla
                self.tree.insert("", "end", values=(n, f"{x_actual:.4f}", f"{y_actual:.6f}"))

            # 4. Graficar Resultados
            self.ax.plot(xs, ys, 'b-o', label='Euler Aprox', markersize=4)
            self.ax.set_title(f"Solución de dy/dx = {f_str}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
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