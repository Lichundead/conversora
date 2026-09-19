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

    def test_none_y_otros_tipos(self):
        self.assertEqual(logica.parsear_cantidad(None), 0)
        self.assertEqual(logica.parsear_cantidad(3.7), 0)
        self.assertEqual(logica.parsear_cantidad(True), 0)

    def test_entero_directo(self):
        self.assertEqual(logica.parsear_cantidad(5), 5)
        self.assertEqual(logica.parsear_cantidad(-5), 0)

    def test_cantidad_absurdamente_larga(self):
        # int() rechaza cadenas de más de 4300 dígitos desde Python 3.11.
        largo = "9" * 5000
        self.assertEqual(logica.parsear_cantidad(largo), 0)

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
        entradas = {
            "m100": (100, "-3"),
        }
        # El validate de la GUI bloquea negativos, pero logica también los trata como 0
        self.assertEqual(logica.calcular_total(entradas), 0)

    def test_diccionario_vacio(self):
        self.assertEqual(logica.calcular_total({}), 0)

    def test_billete_grande(self):
        entradas = {
            "b100k": (100000, "5"),
        }
        self.assertEqual(logica.calcular_total(entradas), 500000)

    def test_todas_las_denominaciones(self):
        entradas = {
            idf: (valor, "1")
            for valor, _nombre, idf in logica.DENOMINACIONES
        }
        esperado = sum(valor for valor, _n, _i in logica.DENOMINACIONES)
        self.assertEqual(logica.calcular_total(entradas), esperado)


class TestContratoDeTipos(unittest.TestCase):
    """Todo formato inválido debe salir como TypeError, nunca en crudo."""

    def test_none(self):
        with self.assertRaises(TypeError):
            logica.calcular_total(None)

    def test_lista_en_vez_de_mapa(self):
        with self.assertRaises(TypeError):
            logica.calcular_total([(50, "2")])

    def test_par_de_tres_elementos(self):
        with self.assertRaises(TypeError):
            logica.calcular_total({"m50": (50, "2", "extra")})

    def test_valor_no_entero(self):
        with self.assertRaises(TypeError):
            logica.calcular_total({"m50": ("50", "2")})

    def test_valor_es_cadena_suelta(self):
        with self.assertRaises(TypeError):
            logica.calcular_total({"m50": "ab"})

    def test_objeto_con_items_no_invocable(self):
        class Falso:
            items = "no soy un método"

        with self.assertRaises(TypeError):
            logica.calcular_total(Falso())


class TestSubtotales(unittest.TestCase):

    def test_desglose(self):
        entradas = {
            "m50":  (50,  "2"),
            "m100": (100, "3"),
        }
        self.assertEqual(logica.subtotales(entradas), {"m50": 100, "m100": 300})

    def test_total_es_la_suma_de_los_subtotales(self):
        entradas = {
            "m50":   (50,   "4"),
            "b1k":   (1000, "7"),
            "b10k":  (10000, ""),
        }
        self.assertEqual(
            logica.calcular_total(entradas),
            sum(logica.subtotales(entradas).values()),
        )


if __name__ == '__main__':
    unittest.main()
