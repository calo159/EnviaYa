# Parte 7 · Gestión de configuración

Repositorio: <https://github.com/calo159/EnviaYa>

## 7.1 Etiqueta del código heredado

El commit inicial contiene `envios.py` tal como se entregó, con solo el `CONFIG` diligenciado con mis valores, y está etiquetado `v1.0.0`.

## 7.2 Ramas

Una rama por cada defecto, una de refactorización, una de pruebas y una de la solicitud de cambio. Todas se integraron a `main` con `git merge --no-ff`, para que el historial conserve la rama de cada trabajo.

| Rama | Contenido | Integración |
|------|-----------|-------------|
| `test/suite` | 48 casos de caja negra y 15 de caja blanca, automatizados con pytest | Merge a `main`. Se integró antes de las correcciones, por eso contra v1.0.0 la suite falla (23 rojos). |
| `fix/DEF-01` | El tramo 1 no incluye L1 (R3) | Merge a `main` |
| `fix/DEF-02` | Zona inválida lanza error (R2) | Merge a `main` |
| `fix/DEF-03` | Día fuera de 1 a 7 lanza error (R2) | Merge a `main` |
| `fix/DEF-04` | El sábado cobra el recargo de fin de semana (R5) | Merge a `main` |
| `fix/DEF-05` | Cupón inexistente lanza error (R7) | Merge a `main` |
| `fix/DEF-06` | Redondeo al $100 más cercano, los $50 suben (R8) | Merge a `main` → etiqueta `v1.0.1` |
| `refactor/estrategia` | Funciones extraídas, constantes, sin `flag`, patrón Estrategia | Merge a `main` → etiqueta `v2.0.0` |
| `feature/zona-insular` | Solicitud de cambio 0: pruebas primero y luego implementación | Merge a `main` → etiqueta `v2.1.0` |

Orden de trabajo: cada rama de defecto se creó desde el `main` ya actualizado con la anterior, así que las integraciones no generaron conflictos. Tras cada corrección se ejecutó la suite completa: los rojos bajaron 23 → 22 → 20 → 18 → 13 → 10 → 0.

## 7.3 Versionado semántico

El formato es `MAJOR.MINOR.PATCH`: major si se rompe la interfaz, minor si se agrega funcionalidad compatible, patch si solo se corrigen defectos.

| Versión | Qué cambió | Por qué esa versión |
|---------|-----------|---------------------|
| `v1.0.0` | Código heredado | Punto de partida. |
| `v1.0.1` | Se corrigen DEF-01 a DEF-06 | **Patch**: solo correcciones, la firma de `calc` es la misma y no se agrega funcionalidad. |
| `v2.0.0` | Refactorización y eliminación de `flag` | **Major**: ver abajo. |
| `v2.1.0` | Zona insular | **Minor**: funcionalidad nueva que no rompe a quien ya usa la función. |

**¿Quitar `flag` hace que sea major? Sí.** `flag` era parte de la interfaz pública de `calc`. Quien llamaba `calc(5, "urbana", "normal", 1, None, True)` ahora recibe un `TypeError` porque la función ya no acepta un sexto argumento, y además deja de imprimir en consola. Eso es un cambio incompatible hacia atrás, y el versionado semántico exige subir el major aunque el resto de la función siga igual. Matiz: quien llamaba sin `flag` (el caso normal) no nota la diferencia en la firma; el major es por quienes sí lo usaban, ya que el versionado semántico protege a todos los usuarios de la interfaz.

Las correcciones de defectos (v1.0.1) cambian resultados (por ejemplo, el sábado ahora cuesta $2.000 más), pero no son un cambio incompatible: el comportamiento anterior era un error contra la especificación, así que se publican como patch.

## 7.4 CHANGELOG

Ver [CHANGELOG.md](../CHANGELOG.md) en el formato *Keep a Changelog*.

## 7.5 Notas de la versión v2.1.0

**EnvíaYa · cálculo de costos v2.1.0**

*Novedades*
- Nueva zona **insular** (San Andrés) con recargo del 70 %. Los envíos insulares no aceptan cupón.

*Si vienes de v1.x*
- `calc` ya no recibe el argumento `flag` ni imprime nada. Actualiza las llamadas: `calc(peso, zona, cliente, dia, cupon=None)`.
- Un día fuera de 1 a 7, una zona inválida o un cupón inexistente ahora lanzan `ValueError` en lugar de calcularse o ignorarse.
- El sábado ahora cobra el recargo de fin de semana.
- El tramo 1 es peso < 3 kg (antes 3 kg caía en el tramo 1).
- El resultado se redondea al múltiplo de $100 más cercano (antes se truncaba).

*Calidad*
- 100 pruebas automatizadas pasan y 1 se omite (la del `flag`). Cobertura de sentencias y de ramas: 100 %.
- Complejidad ciclomática máxima por función: 3.

## 7.6 Historial de Git

La salida de `git log --oneline --graph --all` está en [evidencia/07-git-log.txt](../evidencia/07-git-log.txt) y al final del informe. Los commits están hechos con la hora real en que se trabajó cada parte: el primero a las 16:34 y los siguientes a medida que se completaba cada parte, sin alterar las fechas.
