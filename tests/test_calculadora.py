import unittest

from calculadora_dinero import logica


class TestParsearCantidad(unittest.TestCase):

    def test_texto_valido(self):
        self.assertEqual(logica.parsear_cantidad("7"), 7)

    def test_espacios_alrededor(self):
        self.assertEqual(logica.parsear_cantidad("  12  "), 12)

    def test_vacio(self):
        self.assertEqual(logica.parsear_cantidad(""), 0)
        self.assertEqual(logica.parsear_cantidad("   "), 0)

    def test_no_numerico(self):
        self.assertEqual(logica.parsear_cantidad("abc"), 0)
        self.assertEqual(logica.parsear_cantidad("1.5"), 0)
        self.assertEqual(logica.parsear_cantidad("-3"), 0)

    def test_superindice_no_cuenta(self):
        # isdigit() aceptaría '²' pero int() lo rechaza; isdecimal() no.
        self.assertEqual(logica.parsear_cantidad("2²"), 0)

    def test_cantidad_absurdamente_larga(self):
        # int() rechaza cadenas de más de 4300 dígitos desde Python 3.11.
        self.assertEqual(logica.parsear_cantidad("9" * 5000), 0)

    def test_limite_de_longitud(self):
        justo = "9" * logica.LONGITUD_MAXIMA_CANTIDAD
        pasado = "9" * (logica.LONGITUD_MAXIMA_CANTIDAD + 1)
        self.assertEqual(logica.parsear_cantidad(justo), int(justo))
        self.assertEqual(logica.parsear_cantidad(pasado), 0)


class TestCalcularTotal(unittest.TestCase):

    def test_basico(self):
        entradas = {
            "m50":  (50,  "2"),
            "m100": (100, "1"),
            "m200": (200, "0"),
        }
        self.assertEqual(logica.calcular_total(entradas), 200)

    def test_entradas_vacias(self):
        entradas = {
            "m50":  (50,  ""),
            "m100": (100, ""),
        }
        self.assertEqual(logica.calcular_total(entradas), 0)

    def test_entrada_invalida_ignorada(self):
        entradas = {
            "m50":  (50,  "abc"),
            "m100": (100, "2"),
        }
        self.assertEqual(logica.calcular_total(entradas), 200)

    def test_cantidad_negativa_ignorada(self):
        # El validate de la GUI bloquea negativos, pero logica también los trata como 0.
        self.assertEqual(logica.calcular_total({"m100": (100, "-3")}), 0)

    def test_diccionario_vacio(self):
        self.assertEqual(logica.calcular_total({}), 0)

    def test_billete_grande(self):
        self.assertEqual(logica.calcular_total({"b100k": (100000, "5")}), 500000)

    def test_todas_las_denominaciones(self):
        entradas = {
            idf: (valor, "1")
            for valor, _nombre, idf in logica.DENOMINACIONES
        }
        esperado = sum(valor for valor, _n, _i in logica.DENOMINACIONES)
        self.assertEqual(logica.calcular_total(entradas), esperado)


if __name__ == '__main__':
    unittest.main()
