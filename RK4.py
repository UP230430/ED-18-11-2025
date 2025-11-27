import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RK4App:
    def __init__(self, root):
        self.root = root
        self.root.title("Método Runge-Kutta 4 (RK4)")
        self.root.geometry("950x650")

        # --- Frame de Entrada ---
        input_frame = ttk.LabelFrame(root, text="Parámetros - RK4", padding="10")
        input_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Variables
        self.func_str = tk.StringVar(value="x - y + 2")
        self.x0_val = tk.DoubleVar(value=0.0)
        self.y0_val = tk.DoubleVar(value=2.0)
        self.h_val = tk.DoubleVar(value=0.1)
        self.xf_val = tk.DoubleVar(value=1.0)

        # Inputs Grid
        ttk.Label(input_frame, text="f(x,y):").grid(row=0, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.func_str, width=25).grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="x0:").grid(row=0, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.x0_val, width=8).grid(row=0, column=3, padx=5)

        ttk.Label(input_frame, text="y0:").grid(row=1, column=0, sticky="e")
        ttk.Entry(input_frame, textvariable=self.y0_val, width=8).grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(input_frame, text="h:").grid(row=1, column=2, sticky="e")
        ttk.Entry(input_frame, textvariable=self.h_val, width=8).grid(row=1, column=3, padx=5)

        ttk.Label(input_frame, text="x final:").grid(row=1, column=4, sticky="e")
        ttk.Entry(input_frame, textvariable=self.xf_val, width=8).grid(row=1, column=5, padx=5)

        ttk.Button(input_frame, text="CALCULAR RK4", command=self.calcular_rk4).grid(row=0, column=6, rowspan=2,
                                                                                     padx=20)

        ttk.Label(input_frame, text="Sintaxis: x**2, sin(x), exp(x), log(x)...", font=("Arial", 8, "italic"),
                  foreground="gray").grid(row=2, column=0, columnspan=7, pady=5)

        # --- Resultados ---
        results_frame = ttk.Frame(root)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Tabla
        table_frame = ttk.LabelFrame(results_frame, text="Tabla de Resultados")
        table_frame.pack(side="left", fill="y", padx=5)

        columns = ("n", "x", "y_rk4")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        self.tree.heading("n", text="n")
        self.tree.heading("x", text="x")
        self.tree.heading("y_rk4", text="y (RK4)")

        self.tree.column("n", width=40, anchor="center")
        self.tree.column("x", width=80, anchor="center")
        self.tree.column("y_rk4", width=120, anchor="center")

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

    def evaluar_funcion(self, expr, x, y):
        allowed = {"sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "sqrt": np.sqrt, "log": np.log,
                   "pi": np.pi, "e": np.e}
        # Evalúa f(x,y) de forma segura
        return eval(expr, {"__builtins__": None}, {**allowed, 'x': x, 'y': y})

    def calcular_rk4(self):
        # Limpieza
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.ax.clear()

        try:
            f_str = self.func_str.get()
            x0 = self.x0_val.get()
            y0 = self.y0_val.get()
            h = self.h_val.get()
            xf = self.xf_val.get()

            if h <= 0:
                messagebox.showerror("Error", "h debe ser > 0")
                return

            # Inicialización
            xs = [x0]
            ys = [y0]
            x = x0
            y = y0
            n = 0

            self.tree.insert("", "end", values=(n, f"{x:.4f}", f"{y:.6f}"))

            # --- BUCLE PRINCIPAL (Lógica RK4) ---
            while x < xf - 1e-9:
                # 1. k1: Pendiente al inicio
                k1 = self.evaluar_funcion(f_str, x, y)

                # 2. k2: Pendiente en el punto medio (usando k1)
                # x aumenta h/2, y aumenta h/2 * k1
                k2 = self.evaluar_funcion(f_str, x + 0.5 * h, y + 0.5 * h * k1)

                # 3. k3: Pendiente en el punto medio (usando k2)
                # x aumenta h/2, pero y aumenta usando k2
                k3 = self.evaluar_funcion(f_str, x + 0.5 * h, y + 0.5 * h * k2)

                # 4. k4: Pendiente al final
                # x aumenta h completo, y aumenta h * k3
                k4 = self.evaluar_funcion(f_str, x + h, y + h * k3)

                # Fórmula RK4: Promedio ponderado
                y_next = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
                x_next = x + h

                # Actualizar variables reales
                x = x_next
                y = y_next
                n += 1

                # Guardar y mostrar
                xs.append(x)
                ys.append(y)
                self.tree.insert("", "end", values=(n, f"{x:.4f}", f"{y:.6f}"))

            # Graficar
            self.ax.plot(xs, ys, 'r-o', label='Método RK4', markersize=4)  # 'r' es rojo
            self.ax.set_title(f"Solución RK4: {f_str}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.legend()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Error de cálculo: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RK4App(root)
    root.mainloop()