# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [2.0.0] - 2026-11-11

### Cambiado
- **Cambio incompatible:** `calc` ya no recibe el argumento `flag` ni imprime en consola. La firma pasa de `calc(p, z, c, d, cup=None, flag=False)` a `calc(peso, zona, cliente, dia, cupon=None)`.
- Refactorización de `calc` en funciones pequeñas (`validar_peso`, `tarifa_base`, `redondear`, entre otras).
- Los números mágicos se reemplazaron por constantes con nombre.
- Las zonas usan el patrón Estrategia (`Zona`, `ZonaUrbana`, `ZonaRural`, `ZonaNacional`).
- Los cálculos usan `Decimal` en lugar de `float`.
- Se eliminó la configuración global mutable `CONFIG`.

### Añadido
- Pruebas de unidad de las funciones y estrategias extraídas.

## [1.0.1] - 2026-11-11

### Corregido
- DEF-01: el peso exacto L1 (3 kg) pertenece al tramo 2, no al tramo 1 (R3).
- DEF-02: una zona inválida lanza error en lugar de cobrarse como urbana (R2).
- DEF-03: un día fuera del rango 1 a 7 lanza error (R2).
- DEF-04: el sábado también cobra el recargo de fin de semana (R5).
- DEF-05: un cupón inexistente lanza error en lugar de ignorarse (R7).
- DEF-06: el costo se redondea al múltiplo de $100 más cercano y los $50 suben, en lugar de truncar (R8).

### Añadido
- Suite de 63 pruebas automatizadas con pytest: 48 de caja negra y 15 de caja blanca.
- Documentación de requisitos, plan de pruebas y registro de defectos en `docs/`.

## [1.0.0] - 2026-11-11

### Añadido
- Versión heredada de `calc` con su `CONFIG` personalizado, sin modificar. Contiene los defectos DEF-01 a DEF-06.

[2.0.0]: https://github.com/calo159/EnviaYa/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/calo159/EnviaYa/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/calo159/EnviaYa/releases/tag/v1.0.0
