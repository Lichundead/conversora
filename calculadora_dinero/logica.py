"""Lógica de cálculo, independiente de la interfaz gráfica."""

from collections.abc import Mapping

# Tope de dígitos aceptados en una cantidad. Evita que un pegado accidental
# de miles de caracteres llegue a int(), que a partir de Python 3.11 rechaza
# enteros de más de 4300 dígitos con ValueError.
LONGITUD_MAXIMA_CANTIDAD = 12


# (valor en pesos, etiqueta, identificador) — dato de dominio, no de interfaz.
DENOMINACIONES = [
    (50,     "Moneda de $50",              "m50"),
    (100,    "Moneda de $100",             "m100"),
    (200,    "Moneda de $200",             "m200"),
    (500,    "Moneda de $500",             "m500"),
    (1000,   "Billete/Moneda de $1.000",   "b1k"),
    (2000,   "Billete de $2.000",          "b2k"),
    (5000,   "Billete de $5.000",          "b5k"),
    (10000,  "Billete de $10.000",         "b10k"),
    (20000,  "Billete de $20.000",         "b20k"),
    (50000,  "Billete de $50.000",         "b50k"),
    (100000, "Billete de $100.000",        "b100k"),
]


def parsear_cantidad(cantidad):
    """Convierte el texto de una casilla en una cantidad entera no negativa.

    Cualquier texto que no represente un entero positivo válido (vacío, con
    letras, negativo o absurdamente largo) se interpreta como 0. Nunca lanza.
    """
    if isinstance(cantidad, int) and not isinstance(cantidad, bool):
        return cantidad if cantidad > 0 else 0

    if not isinstance(cantidad, str):
        return 0

    texto = cantidad.strip()
    if not texto.isdecimal() or len(texto) > LONGITUD_MAXIMA_CANTIDAD:
        return 0

    return int(texto)


def subtotales(entradas):
    """Devuelve {identificador: aporte al total} para un mapa de entradas.

    `entradas` es un mapa {identificador: (valor_denominacion, cantidad)}.
    Lanza TypeError -y solo TypeError- si el formato no se respeta.
    """
    if not isinstance(entradas, Mapping):
        raise TypeError("Formato de diccionario de entradas inválido.")

    resultado = {}
    for identificador, par in entradas.items():
        if isinstance(par, str) or not isinstance(par, (tuple, list)) or len(par) != 2:
            raise TypeError(
                f"Entrada inválida en '{identificador}': se esperaba (valor, cantidad)."
            )

        valor, cantidad = par
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError(
                f"Valor inválido en '{identificador}': se esperaba un entero."
            )

        resultado[identificador] = valor * parsear_cantidad(cantidad)

    return resultado


def calcular_total(entradas):
    """Suma el aporte de todas las denominaciones."""
    return sum(subtotales(entradas).values())
