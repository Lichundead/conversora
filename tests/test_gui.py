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

    def test_arranca_en_cero(self):
        self.assertEqual(self.app._total, 0)
        self.assertEqual(self.app.resultado_label.cget('text'), "TOTAL: $0 COP")

    def test_una_casilla_actualiza_el_total(self):
        self._escribir("b10k", "3")
        self.assertEqual(self.app._total, 30000)
        self.assertEqual(
            self.app.resultado_label.cget('text'), "TOTAL: $30.000 COP"
        )

    def test_varias_casillas_se_suman(self):
        self._escribir("b10k", "2")
        self._escribir("m500", "4")
        self.assertEqual(self.app._total, 22000)

    def test_corregir_una_casilla_no_acumula(self):
        """El total incremental debe seguir al valor, no a la historia."""
        self._escribir("b1k", "5")
        self._escribir("b1k", "50")
        self._escribir("b1k", "5")
        self.assertEqual(self.app._total, 5000)

    def test_borrar_vuelve_a_cero(self):
        self._escribir("b20k", "7")
        self._escribir("b20k", "")
        self.assertEqual(self.app._total, 0)
        self.assertEqual(self.app.resultado_label.cget('text'), "TOTAL: $0 COP")

    def test_total_incremental_coincide_con_el_calculo_completo(self):
        from calculadora_dinero import logica

        for idf, texto in (("m50", "3"), ("b5k", "12"), ("b100k", "2")):
            self._escribir(idf, texto)

        entradas = {
            idf: (valor, variable.get())
            for idf, (valor, variable) in self.app.entries.items()
        }
        self.assertEqual(self.app._total, logica.calcular_total(entradas))

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
