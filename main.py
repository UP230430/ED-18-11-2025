# main_launcher.py
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

# Ruta del intérprete Python actual
PY = sys.executable

# Nombres de archivo (asume que están en la misma carpeta que este archivo)
TRAP_FILE = "Metodo_Trapecios.py"
NEWTON_FILE = "metodonewton.py"
ECUA_FILE ="ecuacionewton.py"

def run_script(filename):
    """Lanza un script en un nuevo proceso."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(path):
        messagebox.showerror("Error", f"No se encontró {filename}\nRuta esperada: {path}")
        return
    try:
        # Popen para que el launcher no quede bloqueado
        subprocess.Popen([PY, path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo lanzar {filename}:\n{e}")

def abrir_trapecios():
    run_script(TRAP_FILE)

def abrir_newton():
    run_script(NEWTON_FILE)

def abrir_ecua():
    run_script(ECUA_FILE)



# Interfaz gráfica simple
def crear_ventana():
    root = tk.Tk()
    root.title("Launcher - Trapecios & Newton")
    root.geometry("360x180")
    tk.Label(root, text="Selecciona un programa para abrir:", font=("Segoe UI", 11)).pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Método del Trapecio", width=22, command=abrir_trapecios, bg="#b3e6b3").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Newton-Raphson", width=22, command=abrir_newton, bg="#cfe8ff").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Newton-solucion_ecuaciones", width=22, command=abrir_ecua, bg="#ffd9b3").grid(row=2, column=0, padx=5, pady=5)

    tk.Label(root, text="(Se abrirán en ventanas separadas)", font=("Segoe UI", 8)).pack(pady=6)
    root.mainloop()

if __name__ == "__main__":
    crear_ventana()
