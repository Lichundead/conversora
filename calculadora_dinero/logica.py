"""Lógica de cálculo, independiente de la interfaz gráfica."""

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


def parsear_cantidad(texto):
    """Convierte el texto de una casilla en una cantidad entera no negativa.

    Cualquier texto que no represente un entero positivo válido (vacío, con
    letras, negativo o absurdamente largo) se interpreta como 0. Nunca lanza.
    """
    texto = texto.strip()
    if not texto.isdecimal() or len(texto) > LONGITUD_MAXIMA_CANTIDAD:
        return 0

    return int(texto)


def calcular_total(entradas):
    """Suma el aporte de todas las denominaciones.

    `entradas` es un mapa {identificador: (valor_denominacion, texto)}.
    """
    return sum(valor * parsear_cantidad(texto) for valor, texto in entradas.values())
