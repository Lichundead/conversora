import tkinter as tk
from tkinter import ttk

from . import logica


class CalculadoraDineroCOP:

    def __init__(self, root):
        self.root = root

        # identificador -> (valor_denominacion, StringVar)
        self.entries = {}

        self.root.title("Calculadora de Dinero COP")
        self.root.geometry("400x600")

        self._validate_cmd = self.root.register(self._validate_input)
        self._crear_interfaz()
        self._mostrar_total()

    def _validate_input(self, P):
        return P == "" or (
            P.isdecimal() and len(P) <= logica.LONGITUD_MAXIMA_CANTIDAD
        )

    def _crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(len(logica.DENOMINACIONES) + 1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Denominación", font=('Arial', 14, 'bold')).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        ttk.Label(main_frame, text="Cantidad", font=('Arial', 14, 'bold')).grid(
            row=0, column=1, padx=10, pady=10, sticky="w"
        )

        for i, (valor, nombre, identificador) in enumerate(logica.DENOMINACIONES, start=1):
            ttk.Label(main_frame, text=nombre, font=('Arial', 12)).grid(
                row=i, column=0, sticky="w", padx=10, pady=8
            )

            variable = tk.StringVar(master=self.root, value="")
            entry = ttk.Entry(
                main_frame,
                width=12,
                font=('Arial', 12),
                justify='right',
                textvariable=variable,
                validate='key',
                validatecommand=(self._validate_cmd, '%P'),
            )
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")

            # Un trace sobre la variable cubre teclado, pegado con el ratón y
            # cambios programáticos; <KeyRelease> solo cubría el teclado.
            variable.trace_add('write', lambda *_args: self._mostrar_total())

            self.entries[identificador] = (valor, variable)

        self.resultado_label = ttk.Label(main_frame, font=('Arial', 18, 'bold'))
        self.resultado_label.grid(
            row=len(logica.DENOMINACIONES) + 1,
            column=0,
            columnspan=2,
            pady=20,
        )

    def _mostrar_total(self):
        total = logica.calcular_total(
            {idf: (valor, variable.get()) for idf, (valor, variable) in self.entries.items()}
        )
        self.resultado_label.config(
            text=f"TOTAL: ${total:,.0f} COP".replace(',', '.'),
            foreground="dark green",
        )
