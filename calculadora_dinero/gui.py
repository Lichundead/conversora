import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

from . import logica


class CalculadoraDineroCOP:

    FUENTE_GENERAL = ('Arial', 12)
    FUENTE_TITULO = ('Arial', 14, 'bold')
    FUENTE_RESULTADO = ('Arial', 18, 'bold')

    COLOR_RESULTADO_OK = "dark green"
    COLOR_RESULTADO_ERROR = "red"

    TEXTO_TOTAL_FORMAT = "TOTAL: ${:,.0f} COP"
    TEXTO_TOTAL_ERROR = "Error en cálculo"

    DENOMINACIONES = logica.DENOMINACIONES

    def __init__(self, root):
        self.root = root

        # identificador -> (valor_denominacion, StringVar)
        self.entries = {}
        # identificador -> aporte actual al total, para recalcular de forma
        # incremental en vez de releer las once casillas en cada tecla.
        self._subtotales = {}
        self._total = 0

        # Último estado pintado, para no reconfigurar el label sin necesidad.
        self._texto_actual = None
        self._color_actual = None

        self.root.title("Calculadora de Dinero COP")
        self.root.geometry("400x600")
        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

        # Fuentes con nombre: se resuelven una sola vez y todos los widgets
        # comparten el mismo objeto, en lugar de una especificación por widget.
        self._fuente_general = tkfont.Font(root=self.root, font=self.FUENTE_GENERAL)
        self._fuente_titulo = tkfont.Font(root=self.root, font=self.FUENTE_TITULO)
        self._fuente_resultado = tkfont.Font(root=self.root, font=self.FUENTE_RESULTADO)

        self._validate_cmd = self.root.register(self._validate_input)
        self._crear_interfaz()
        self._recalcular_todo()

    def _validate_input(self, P):
        return P == "" or (
            P.isdecimal() and len(P) <= logica.LONGITUD_MAXIMA_CANTIDAD
        )

    def _crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(len(self.DENOMINACIONES) + 1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(main_frame, text="Denominación", font=self._fuente_titulo).grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )
        ttk.Label(main_frame, text="Cantidad", font=self._fuente_titulo).grid(
            row=0, column=1, padx=10, pady=10, sticky="w"
        )

        for i, (valor, nombre, identificador) in enumerate(self.DENOMINACIONES, start=1):
            ttk.Label(main_frame, text=nombre, font=self._fuente_general).grid(
                row=i, column=0, sticky="w", padx=10, pady=8
            )

            variable = tk.StringVar(master=self.root, value="")
            entry = ttk.Entry(
                main_frame,
                width=12,
                font=self._fuente_general,
                justify='right',
                textvariable=variable,
                validate='key',
                validatecommand=(self._validate_cmd, '%P'),
            )
            entry.grid(row=i, column=1, padx=10, pady=8, sticky="ew")

            # Un trace sobre la variable cubre teclado, pegado con el ratón y
            # cambios programáticos; <KeyRelease> solo cubría el teclado.
            variable.trace_add(
                'write',
                lambda *_args, idf=identificador: self._on_cantidad_cambiada(idf),
            )

            self.entries[identificador] = (valor, variable)
            self._subtotales[identificador] = 0

        self.resultado_label = ttk.Label(
            main_frame,
            font=self._fuente_resultado,
        )
        self.resultado_label.grid(
            row=len(self.DENOMINACIONES) + 1,
            column=0,
            columnspan=2,
            pady=20,
        )

    def _on_cantidad_cambiada(self, identificador):
        """Actualiza el total ajustando solo el aporte de la casilla tocada."""
        try:
            valor, variable = self.entries[identificador]
            subtotal = valor * logica.parsear_cantidad(variable.get())
        except Exception as e:  # noqa: BLE001 - un callback de Tk no debe propagar
            self._mostrar_error(e, con_dialogo=False)
            return

        anterior = self._subtotales[identificador]
        if subtotal == anterior:
            return

        self._subtotales[identificador] = subtotal
        self._total += subtotal - anterior
        self._mostrar_total()

    def _recalcular_todo(self):
        """Recalcula el total completo. Solo se usa al arrancar."""
        try:
            entradas = {
                idf: (valor, variable.get())
                for idf, (valor, variable) in self.entries.items()
            }
            self._subtotales = logica.subtotales(entradas)
            self._total = sum(self._subtotales.values())
        except Exception as e:  # noqa: BLE001 - un callback de Tk no debe propagar
            self._mostrar_error(e)
            return

        self._mostrar_total()

    def _mostrar_total(self):
        texto = self.TEXTO_TOTAL_FORMAT.format(self._total).replace(',', '.')
        self._pintar(texto, self.COLOR_RESULTADO_OK)

    def _mostrar_error(self, error, con_dialogo=True):
        self._pintar(self.TEXTO_TOTAL_ERROR, self.COLOR_RESULTADO_ERROR)
        if con_dialogo:
            messagebox.showerror(
                "Error de Cálculo",
                f"Ocurrió un error al calcular el total:\n{error}",
            )

    def _pintar(self, texto, color):
        """Escribe en el label solo lo que realmente cambió."""
        if texto != self._texto_actual:
            self.resultado_label.config(text=texto)
            self._texto_actual = texto
        if color != self._color_actual:
            self.resultado_label.config(foreground=color)
            self._color_actual = color

    def on_closing(self):
        self.root.destroy()
