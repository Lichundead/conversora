# Calculadora de Dinero COP

Aplicación de escritorio para contar y sumar efectivo en pesos colombianos.
Escribes cuántas unidades tienes de cada denominación y el total se actualiza
al instante.

[![CI](https://github.com/Lichundead/conversora/actions/workflows/ci.yml/badge.svg)](https://github.com/Lichundead/conversora/actions/workflows/ci.yml)
[![Release](https://github.com/Lichundead/conversora/actions/workflows/release.yml/badge.svg)](https://github.com/Lichundead/conversora/actions/workflows/release.yml)

## Requisitos

- Python 3.11 o superior con `tkinter` (en Debian/Ubuntu: `sudo apt install python3-tk`).
- Sin dependencias externas: la aplicación usa solo la biblioteca estándar.

## Ejecutar

```bash
python main.py
```

## Estructura

```
main.py                        punto de entrada
calculadora_dinero/logica.py   cálculo y tabla de denominaciones (sin tkinter)
calculadora_dinero/gui.py      interfaz tkinter
tests/                         pruebas unitarias
```

La lógica no importa `tkinter`, así que se puede probar y reutilizar sin
interfaz gráfica.

## Pruebas

```bash
python -m unittest discover -s tests -t . -v
```

Las pruebas de `tests/test_gui.py` necesitan un display; si no hay, se saltan
solas. Para forzarlas en Linux sin escritorio:

```bash
xvfb-run -a python -m unittest discover -s tests -t . -v
```

## Lint

```bash
pip install -r requirements-dev.txt
ruff check .
```

## Empaquetar un ejecutable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name CalculadoraDineroCOP main.py
```

## CI/CD

- **CI** (`.github/workflows/ci.yml`): en cada pull request y en cada push a
  `main` corre `ruff`, la suite de pruebas en Linux, Windows y macOS, y
  comprueba que el ejecutable se puede construir. Para lanzarlo a mano sobre
  una rama sin PR, usa el botón *Run workflow* (`workflow_dispatch`).
- **Release** (`.github/workflows/release.yml`): al empujar una etiqueta `v*`
  ejecuta primero el workflow de CI completo y, solo si pasa, construye los
  binarios de las tres plataformas y publica una release de GitHub con ellos
  adjuntos. Una etiqueta no dispara `ci.yml` por sí sola, así que sin ese paso
  una versión se podría publicar desde un commit sin verificar.

Formato de cada entrega:

| Plataforma | Asset | Por qué |
|---|---|---|
| Windows | `.exe` suelto | No hay bit de ejecución que preservar |
| Linux | `.tar.gz` | Un asset suelto se descarga sin permiso de ejecución |
| macOS | `.zip` con el `.app` | Es la forma en que macOS espera una aplicación |

Los binarios no están firmados, así que Gatekeeper y SmartScreen avisarán al
abrirlos. El de macOS es solo para Apple Silicon (arm64).

Para publicar una versión:

```bash
git tag v0.2.0
git push origin v0.2.0
```
