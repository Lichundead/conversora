import tkinter as tk

from calculadora_dinero.gui import CalculadoraDineroCOP

def main():
    try:
        root = tk.Tk()
    except tk.TclError as e:
        print(f"Error crítico: No se pudo inicializar Tkinter: {e}")
        raise SystemExit(1)

    try:
        CalculadoraDineroCOP(root)
    except Exception as e:
        print(f"Error crítico: No se pudo crear la aplicación: {e}")
        root.destroy()
        raise SystemExit(1)

    root.mainloop()

if __name__ == "__main__":
    main()
