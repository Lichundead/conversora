import tkinter as tk
import logging

from calculadora_dinero.gui import CalculadoraDineroCOP

LOG_FILE = 'app.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def main():
    setup_logging()

    try:
        root = tk.Tk()
    except tk.TclError as e:
        logging.critical("No se pudo inicializar Tkinter: %s", e)
        raise SystemExit(1)

    try:
        CalculadoraDineroCOP(root)
    except Exception as e:
        logging.critical("No se pudo crear la instancia de la aplicación: %s", e, exc_info=True)
        root.destroy()
        raise SystemExit(1)

    root.mainloop()

if __name__ == "__main__":
    main()
