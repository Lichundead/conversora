"""Pruebas de humo de la interfaz.

Necesitan tkinter y un display; se saltan solas si falta alguno (por eso en
CI se ejecutan bajo xvfb en Linux).
"""

import unittest

try:
    import tkinter as tk
except ImportError:  # pragma: no cover - depende del entorno
    tk = None


def _hay_display():
    if tk is None:
        return False
    try:
        raiz = tk.Tk()
    except Exception:
        return False
    raiz.destroy()
    return True


@unittest.skipUnless(_hay_display(), "requiere tkinter y un display")
class TestCalculadoraDineroCOP(unittest.TestCase):

    def setUp(self):
        from calculadora_dinero.gui import CalculadoraDineroCOP

        self.root = tk.Tk()
        self.root.withdraw()
        self.app = CalculadoraDineroCOP(self.root)

    def tearDown(self):
        self.root.destroy()

    def _escribir(self, identificador, texto):
        _valor, variable = self.app.entries[identificador]
        variable.set(texto)

    def _total_en_pantalla(self):
        return self.app.resultado_label.cget('text')

    def test_arranca_en_cero(self):
        self.assertEqual(self._total_en_pantalla(), "TOTAL: $0 COP")

    def test_una_casilla_actualiza_el_total(self):
        self._escribir("b10k", "3")
        self.assertEqual(self._total_en_pantalla(), "TOTAL: $30.000 COP")

    def test_varias_casillas_se_suman(self):
        self._escribir("b10k", "2")
        self._escribir("m500", "4")
        self.assertEqual(self._total_en_pantalla(), "TOTAL: $22.000 COP")

    def test_corregir_una_casilla_no_acumula(self):
        self._escribir("b1k", "5")
        self._escribir("b1k", "50")
        self._escribir("b1k", "5")
        self.assertEqual(self._total_en_pantalla(), "TOTAL: $5.000 COP")

    def test_borrar_vuelve_a_cero(self):
        self._escribir("b20k", "7")
        self._escribir("b20k", "")
        self.assertEqual(self._total_en_pantalla(), "TOTAL: $0 COP")

    def test_validador_rechaza_lo_que_no_sea_digito(self):
        self.assertTrue(self.app._validate_input(""))
        self.assertTrue(self.app._validate_input("123"))
        self.assertFalse(self.app._validate_input("abc"))
        self.assertFalse(self.app._validate_input("-1"))
        self.assertFalse(self.app._validate_input("2²"))
        self.assertFalse(self.app._validate_input("9" * 99))

    def test_se_crean_todas_las_casillas(self):
        from calculadora_dinero import logica

        self.assertEqual(len(self.app.entries), len(logica.DENOMINACIONES))


if __name__ == '__main__':
    unittest.main()
