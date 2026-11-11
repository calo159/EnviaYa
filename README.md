# EnvíaYa · cálculo del costo de envío

Parcial 3 · Ingeniería de Software I · Universidad de La Guajira · 2026-2
Estudiante: Carlos David Sierra · Código: 0182410125

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 4 | 1 | 0 | 1 | 2 | 5 | 50 | 3 | 10 | 20 % | 50 % | 15 % | $2.000 | 0 |

## Contenido

| Ruta | Qué hay |
|------|---------|
| `envios.py` | Función `calc` (versión actual 2.1.0) |
| `tests/` | Suite de pytest: caja negra, caja blanca, unidad y zona insular |
| `docs/` | Las 8 partes del informe en Markdown |
| `evidencia/` | Salidas y capturas de las ejecuciones de pruebas |
| `informe/` | Informe en PDF |
| `CHANGELOG.md` | Cambios por versión (Keep a Changelog) |

## Ejecutar las pruebas

```
pip install pytest pytest-cov radon
python -m pytest --cov=envios --cov-branch --cov-report=term-missing
```

## Versiones

`v1.0.0` código heredado · `v1.0.1` defectos corregidos · `v2.0.0` refactorización (sin `flag`) · `v2.1.0` zona insular.

Para ver el código heredado con sus defectos: `git checkout v1.0.0`.
