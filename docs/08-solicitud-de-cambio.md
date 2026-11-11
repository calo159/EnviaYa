# Parte 8 · Solicitud de cambio y análisis de impacto

**Mi solicitud:** (A + F) mod 3 = (4 + 5) mod 3 = 0 → *Nueva zona insular (San Andrés) con un recargo del 70 %. Los envíos insulares no aceptan cupón.*

## 8.1 Análisis de impacto con la matriz de trazabilidad

| Elemento | ¿Se afecta? | Detalle |
|----------|-------------|---------|
| **R1** peso válido | No | Se mantiene igual para la nueva zona. |
| **R2** zona válida | **Sí** | “insular” deja de ser una zona inválida: pasa a ser la cuarta zona válida. |
| **R3** tarifa base | No | La base no depende de la zona. |
| **R4** recargo por zona | **Sí** | Se agrega: insular +70 %. |
| **R5** fin de semana | No | Se mantiene: se suma antes de los descuentos, también en la zona insular. |
| **R6** descuentos | **Sí, parcial** | Cliente frecuente y VIP siguen aplicando; el cupón ENVIO10 no aplica en la zona insular. |
| **R7** cupón inexistente | **Sí, parcial** | En zona insular, cualquier cupón (válido o no) es error. |
| **R8** mínimo y redondeo | No | |
| **R9 (nuevo)** | **Nuevo** | Los envíos insulares no aceptan cupón. |

Interpretación adoptada: “no aceptan cupón” significa que, si en un envío insular llega un cupón, se lanza error (`los envios insulares no aceptan cupon`). Se eligió error y no ignorarlo en silencio para ser coherente con mi regla F impar y porque el cliente no debe creer que recibió un descuento que no se aplicó. Es una pregunta abierta para el negocio.

### Matriz de trazabilidad afectada

| Requisito | Historia | Casos existentes afectados | Casos nuevos | Parte del código |
|-----------|----------|----------------------------|--------------|------------------|
| R2 | HU-1 | **CP-07** y la prueba unitaria `obtener_zona` usaban “insular” como zona inválida; ahora usan “internacional” | CI-13 | `ZONAS` y `obtener_zona` |
| R4 | HU-2 | CP-17 a CP-19 siguen igual (regresión) | CI-01 a CI-04 | Nueva clase `ZonaInsular` y constante `RECARGO_INSULAR` |
| R5 | HU-2 | Sin cambios | CI-05, CI-07, CI-08 | Sin cambios |
| R6 | HU-3 | CP-24 a CP-28 y TD-01 a TD-12 siguen igual (regresión) | CI-06, CI-07, CI-08, CI-11 | `calc` (validación de cupón) |
| R7 | HU-1 | CP-29 y CP-30 siguen igual | CI-10 | `calc` |
| R9 (nuevo) | HU-1 (criterio nuevo) | — | CI-09, CI-10, CI-11 | `Zona.acepta_cupon`, `calc` |

**Historia afectada:** HU-1 (validación) y HU-2 (recargos) ganan criterios nuevos:

- *Dado* una zona insular y 5 kg, *cuando* calculo, *entonces* se suma 70 % a la base ($9.000 → $15.300).
- *Dado* una zona insular y un cupón, *cuando* calculo, *entonces* se lanza error.

**Partes del código que cambian** (todas en `envios.py`): constante `RECARGO_INSULAR`; atributo `acepta_cupon` en `Zona`; clase `ZonaInsular`; entrada `"insular"` en `ZONAS`; y una validación en `calc`. Gracias al patrón Estrategia de la Parte 6, `tarifa_base`, `redondear` y las demás funciones no se tocan, y las otras tres zonas tampoco.

**Riesgos del cambio:** (1) que la zona insular rompa las zonas existentes → se mitiga con la regresión completa; (2) que un caso que daba error ahora no lo dé (CP-07) → se actualizó de forma explícita; (3) interpretación de “no aceptan cupón” → documentada.

## 8.2 Tipo de mantenimiento

**Perfectivo** (evolutivo): amplía la funcionalidad por una solicitud del negocio. No es correctivo (no hay defecto), ni adaptativo (no cambia el entorno técnico o legal), ni preventivo.

## 8.3 Implementación con pruebas primero

Rama `feature/zona-insular`, en este orden:

1. **Commit de pruebas (rojo):** 15 pruebas nuevas en `tests/test_zona_insular.py` (CI-01 a CI-13) y la actualización de CP-07. Se ejecutaron antes de tocar el código: **10 fallan, 5 pasan** (las 5 que ya pasaban son las que verifican que lo existente no cambia o que ya daban error).
2. **Commit de implementación (verde):** `ZonaInsular` y la validación de cupón. Resultado: **100 pasan, 1 omitida**, cobertura 100 % de sentencias y ramas.

![Pruebas de la zona insular fallando antes de implementar](../evidencia/05-insular-rojo.png)

![Suite completa en verde tras implementar](../evidencia/06-pruebas-v2.1.0.png)

Cálculo a mano de dos casos nuevos:

**CI-08 · peso = 3 kg, insular, vip, día 6, sin cupón**
1. Tramo: 3 no es menor que 3, tramo 2 → $9.000
2. Zona insular +70 % → 9.000 × 1,70 = $15.300
3. Sábado, recargo antes de los descuentos → 15.300 + 2.000 = $17.300
4. VIP 15 % → 17.300 × 0,85 = $14.705
5. Se redondea a $100 (5 < 50, baja) → **$14.700**

**CI-07 · peso = 5 kg, insular, frecuente, día 7, sin cupón**
1. Tramo 2 → $9.000 → insular: $15.300
2. Domingo: 15.300 + 2.000 = $17.300
3. Frecuente 5 % → 17.300 × 0,95 = $16.435
4. Se redondea a $100 (35 < 50, baja) → **$16.400**

## 8.4 Nueva versión

**v2.1.0.** Se agrega una función nueva sin romper la interfaz de `calc` (misma firma), así que es un cambio *minor* según el versionado semántico. Hay un matiz: un envío insular que antes daba error ahora se calcula; se considera parte de la nueva funcionalidad y no una ruptura de la interfaz, porque lo que se agrega es un valor aceptado, no una firma distinta.
