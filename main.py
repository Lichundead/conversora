import tkinter as tk

from calculadora_dinero.gui import CalculadoraDineroCOP


def main():
    root = tk.Tk()
    CalculadoraDineroCOP(root)
    root.mainloop()


if __name__ == "__main__":
    main()
