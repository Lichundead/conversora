import unittest
from calculadora_dinero import logica

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

    def test_tipo_invalido_lanza_error(self):
        with self.assertRaises(TypeError):
            logica.calcular_total(None)

    def test_billete_grande(self):
        entradas = {
            "b100k": (100000, "5"),
        }
        self.assertEqual(logica.calcular_total(entradas), 500000)

if __name__ == '__main__':
    unittest.main()
