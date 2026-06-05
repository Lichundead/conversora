def calcular_total(entradas):
    if not hasattr(entradas, 'items'):
        raise TypeError("Formato de diccionario de entradas inválido.")

    total = 0
    for _identificador, (valor, cantidad_str) in entradas.items():
        try:
            stripped = cantidad_str.strip() if cantidad_str else ""
            cantidad = int(stripped) if stripped else 0
        except ValueError:
            cantidad = 0

        if cantidad < 0:
            cantidad = 0

        total += valor * cantidad

    return total
