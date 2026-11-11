# Parte 3 · Diseño de casos de caja negra

Todos los resultados esperados salen de mi especificación (Parte 1), calculados a mano. Ninguno se obtuvo ejecutando el código.

## 3.1 Particiones de equivalencia

| Entrada | Clase | Tipo | Partición | Valor representativo |
|---------|-------|------|-----------|----------------------|
| peso | PE-P1 | Inválida | peso ≤ 0 | −0,01 ; 0 |
| peso | PE-P2 | Válida | 0 < peso < 3 (tramo 1) | 2 |
| peso | PE-P3 | Válida | 3 ≤ peso ≤ 10 (tramo 2) | 5 |
| peso | PE-P4 | Válida | 10 < peso ≤ 50 (tramo 3) | 25 |
| peso | PE-P5 | Inválida | peso > 50 | 50,01 |
| zona | PE-Z1 | Válida | urbana | "urbana" |
| zona | PE-Z2 | Válida | rural | "rural" |
| zona | PE-Z3 | Válida | nacional | "nacional" |
| zona | PE-Z4 | Inválida | cualquier otro valor | "insular" |
| cliente | PE-C1 | Válida | normal | "normal" |
| cliente | PE-C2 | Válida | frecuente | "frecuente" |
| cliente | PE-C3 | Válida | vip | "vip" |
| día | PE-D1 | Inválida | día < 1 | 0 |
| día | PE-D2 | Válida | 1 a 5 (entre semana) | 1 ; 5 |
| día | PE-D3 | Válida | 6 y 7 (fin de semana) | 6 ; 7 |
| día | PE-D4 | Inválida | día > 7 | 8 |
| cupón | PE-K1 | Válida | sin cupón | None |
| cupón | PE-K2 | Válida | cupón existente | "ENVIO10" |
| cupón | PE-K3 | Inválida | cupón inexistente (F impar → error) | "DESCUENTO99" ; "envio10" |

## 3.2 Valores límite de peso

Mi L1 = 3 **no está incluido** en el tramo 1 (D = 1, impar): 2,99 es tramo 1 y 3 ya es tramo 2. L2 = 10 sí está incluido en el tramo 2. PMAX = 50 es válido.

| Límite | Valor | Clase | Resultado esperado (urbana, normal, día 1, sin cupón) | Caso |
|--------|-------|-------|--------------------------------------------------------|------|
| 0 | −0,01 | inválido | error “peso inválido” | CP-02 |
| 0 | 0 | inválido | error “peso inválido” | CP-01 |
| 0 | 0,01 | tramo 1 | $6.000 | CP-03 |
| L1 = 3 | 2,99 | tramo 1 | $6.000 | CP-10 |
| L1 = 3 | 3 | tramo 2 | $9.000 | CP-11 |
| L1 = 3 | 3,01 | tramo 2 | $9.000 | CP-12 |
| L2 = 10 | 9,99 | tramo 2 | $9.000 | CP-13 |
| L2 = 10 | 10 | tramo 2 | $9.000 | CP-14 |
| L2 = 10 | 10,01 | tramo 3 | 9.000 + 0,01·800 = 9.008 → $9.000 | CP-15 |
| PMAX = 50 | 49,99 | tramo 3 | 9.000 + 39,99·800 = 40.992 → $41.000 | CP-06 |
| PMAX = 50 | 50 | tramo 3 | 9.000 + 40·800 = $41.000 | CP-04 |
| PMAX = 50 | 50,01 | inválido | error “peso inválido” | CP-05 |

## 3.3 Tabla de decisión: cliente × cupón × fin de semana

Reglas que aplican: **B impar** → se aplican ambos descuentos, primero cliente y luego cupón. **E par** → el recargo de $2.000 se suma antes de los descuentos.

Condiciones fijas para calcular: peso = 5 kg (base $9.000), zona urbana. Con fin de semana el valor antes de descuentos es 9.000 + 2.000 = 11.000.

| Regla | Cliente | Cupón | Fin de semana | +$2.000 antes | Desc. cliente | Desc. cupón 10 % | Cálculo | Esperado |
|-------|---------|-------|---------------|---------------|---------------|------------------|---------|----------|
| TD-01 | normal | no | no | — | — | — | 9.000 | $9.000 |
| TD-02 | normal | no | sí | ✔ | — | — | 11.000 | $11.000 |
| TD-03 | normal | ENVIO10 | no | — | — | ✔ | 9.000 × 0,90 = 8.100 | $8.100 |
| TD-04 | normal | ENVIO10 | sí | ✔ | — | ✔ | 11.000 × 0,90 = 9.900 | $9.900 |
| TD-05 | frecuente | no | no | — | 5 % | — | 9.000 × 0,95 = 8.550 | $8.600 |
| TD-06 | frecuente | no | sí | ✔ | 5 % | — | 11.000 × 0,95 = 10.450 | $10.500 |
| TD-07 | frecuente | ENVIO10 | no | — | 5 % | ✔ | 8.550 × 0,90 = 7.695 | $7.700 |
| TD-08 | frecuente | ENVIO10 | sí | ✔ | 5 % | ✔ | 10.450 × 0,90 = 9.405 | $9.400 |
| TD-09 | vip | no | no | — | 15 % | — | 9.000 × 0,85 = 7.650 | $7.700 |
| TD-10 | vip | no | sí | ✔ | 15 % | — | 11.000 × 0,85 = 9.350 | $9.400 |
| TD-11 | vip | ENVIO10 | no | — | 15 % | ✔ | 7.650 × 0,90 = 6.885 | $6.900 |
| TD-12 | vip | ENVIO10 | sí | ✔ | 15 % | ✔ | 9.350 × 0,90 = 8.415 | $8.400 |

Cupón inexistente: para cualquier cliente y día la acción es **error** (regla F impar); se cubre con CP-29 y CP-30.

## 3.4 Matriz de casos de prueba

Salvo que se indique otra cosa: zona urbana, cliente normal, día 1 (lunes), sin cupón. Técnicas: PE = partición de equivalencia, VL = valor límite, TD = tabla de decisión.

| ID | Req. | peso | zona | cliente | día | cupón | Resultado esperado | Técnica |
|----|------|------|------|---------|-----|-------|--------------------|---------|
| CP-01 | R1 | 0 | urbana | normal | 1 | — | Error “peso inválido” | VL |
| CP-02 | R1 | −0,01 | urbana | normal | 1 | — | Error “peso inválido” | VL / PE-P1 |
| CP-03 | R1, R3 | 0,01 | urbana | normal | 1 | — | $6.000 | VL |
| CP-04 | R1, R3 | 50 | urbana | normal | 1 | — | $41.000 | VL |
| CP-05 | R1 | 50,01 | urbana | normal | 1 | — | Error “peso inválido” | VL / PE-P5 |
| CP-06 | R1, R3, R8 | 49,99 | urbana | normal | 1 | — | $41.000 | VL |
| CP-07 | R2 | 5 | insular | normal | 1 | — | Error (zona inválida) | PE-Z4 |
| CP-08 | R2 | 5 | urbana | normal | 0 | — | Error (día inválido) | VL / PE-D1 |
| CP-09 | R2 | 5 | urbana | normal | 8 | — | Error (día inválido) | VL / PE-D4 |
| CP-10 | R3 | 2,99 | urbana | normal | 1 | — | $6.000 | VL |
| CP-11 | R3 | 3 | urbana | normal | 1 | — | $9.000 | VL |
| CP-12 | R3 | 3,01 | urbana | normal | 1 | — | $9.000 | VL |
| CP-13 | R3 | 9,99 | urbana | normal | 1 | — | $9.000 | VL |
| CP-14 | R3 | 10 | urbana | normal | 1 | — | $9.000 | VL |
| CP-15 | R3, R8 | 10,01 | urbana | normal | 1 | — | $9.000 | VL |
| CP-16 | R3 | 25 | urbana | normal | 1 | — | $21.000 | PE-P4 |
| CP-17 | R4 | 5 | urbana | normal | 1 | — | $9.000 | PE-Z1 |
| CP-18 | R4 | 5 | rural | normal | 1 | — | $10.800 | PE-Z2 |
| CP-19 | R4 | 5 | nacional | normal | 1 | — | $13.500 | PE-Z3 |
| CP-20 | R5 | 5 | urbana | normal | 5 | — | $9.000 | VL día |
| CP-21 | R5 | 5 | urbana | normal | 6 | — | $11.000 | VL día / PE-D3 |
| CP-22 | R5 | 5 | urbana | normal | 7 | — | $11.000 | VL día / PE-D3 |
| CP-23 | R4, R5, R6 | 5 | rural | vip | 6 | — | $10.900 | TD (regla E) |
| CP-24 | R6 | 2 | urbana | frecuente | 1 | — | $5.700 | PE-C2 |
| CP-25 | R6 | 2 | urbana | vip | 1 | — | $5.100 | PE-C3 |
| CP-26 | R6 | 5 | urbana | normal | 1 | ENVIO10 | $8.100 | PE-K2 |
| CP-27 | R4, R6, R8 | 5 | nacional | vip | 1 | ENVIO10 | $10.300 | TD (regla B) |
| CP-28 | R4, R5, R6, R8 | 5 | rural | frecuente | 7 | ENVIO10 | $10.900 | TD (reglas B y E) |
| CP-29 | R7 | 5 | urbana | normal | 1 | DESCUENTO99 | Error (cupón inexistente) | PE-K3 |
| CP-30 | R7 | 5 | urbana | vip | 6 | envio10 | Error (cupón inexistente) | PE-K3 |
| CP-31 | R8 | 1 | urbana | vip | 1 | ENVIO10 | $5.000 | VL mínimo |
| CP-32 | R8 | 5 | urbana | frecuente | 1 | — | $8.600 | VL redondeo ($50) |
| CP-33 | R8 | 5 | urbana | frecuente | 1 | ENVIO10 | $7.700 | VL redondeo ($95) |
| CP-34 | R8 | 10,06 | urbana | normal | 1 | — | $9.000 | VL redondeo ($48) |
| CP-35 | R6, R8 | 1 | urbana | frecuente | 1 | ENVIO10 | $5.100 | VL mínimo |
| CP-36 | R3–R8 | 20 | nacional | frecuente | 7 | ENVIO10 | $23.500 | Combinado |
| TD-01 … TD-12 | R5, R6, R8 | 5 | urbana | (tabla) | 1 o 6 | (tabla) | Ver tabla 3.3 | TD |

Total: **36 casos CP + 12 casos de la tabla de decisión = 48 casos**.

Cálculos cortos de los casos que no se detallan abajo:

- CP-16: 9.000 + (25 − 10)·800 = 9.000 + 12.000 = 21.000.
- CP-18: 9.000 × 1,20 = 10.800. CP-19: 9.000 × 1,50 = 13.500.
- CP-21 y CP-22: 9.000 + 2.000 = 11.000.
- CP-24: 6.000 × 0,95 = 5.700. CP-25: 6.000 × 0,85 = 5.100. CP-26: 9.000 × 0,90 = 8.100.
- CP-28: 9.000 × 1,20 = 10.800; + 2.000 = 12.800; × 0,95 = 12.160; × 0,90 = 10.944 → 10.900.
- CP-33: 9.000 × 0,95 = 8.550; × 0,90 = 7.695 → 7.700.
- CP-34: 9.000 + 0,06·800 = 9.048 → 9.000.
- CP-35: 6.000 × 0,95 = 5.700; × 0,90 = 5.130 (≥ 5.000) → 5.100.

## 3.5 Cálculo paso a paso (6 casos)

**CP-11 · peso = 3 kg, urbana, normal, día 1, sin cupón**
1. Tramo: D = 1 es impar, el tramo 1 es peso < 3. Como 3 no es menor que 3, va al tramo 2 → $9.000
2. Zona urbana: sin recargo → $9.000
3. Lunes: sin recargo de fin de semana → $9.000
4. Cliente normal y sin cupón: sin descuentos → $9.000
5. Es mayor que $5.000 y ya es múltiplo de $100 → **resultado esperado: $9.000**

**CP-23 · peso = 5 kg, rural, vip, día 6 (sábado), sin cupón**
1. Tramo: 3 ≤ 5 ≤ 10, tramo 2 → $9.000
2. Zona rural +20 % → 9.000 × 1,20 = $10.800
3. Sábado, y E = 2 es par: el recargo va antes de los descuentos → 10.800 + 2.000 = $12.800
4. VIP 15 %, sin cupón → 12.800 × 0,85 = $10.880
5. Es mayor que $5.000. Se redondea a $100 (80 ≥ 50, sube) → **resultado esperado: $10.900**

(Si el recargo fuera después: 10.800 × 0,85 = 9.180 + 2.000 = 11.180 → 11.200. El caso distingue la regla E.)

**CP-27 · peso = 5 kg, nacional, vip, día 1, cupón ENVIO10**
1. Tramo 2 → $9.000
2. Zona nacional +50 % → 9.000 × 1,50 = $13.500
3. Lunes: sin recargo → $13.500
4. B = 1 es impar: se aplican ambos. Primero VIP 15 % → 13.500 × 0,85 = $11.475; luego cupón 10 % → 11.475 × 0,90 = $10.327,50
5. Es mayor que $5.000. Se redondea a $100 (27,50 < 50, baja) → **resultado esperado: $10.300**

(Con “solo el mayor” daría 11.475 → 11.500. El caso distingue la regla B.)

**CP-31 · peso = 1 kg, urbana, vip, día 1, cupón ENVIO10**
1. Tramo: 1 < 3, tramo 1 → $6.000
2. Urbana: sin recargo → $6.000
3. Lunes: sin recargo → $6.000
4. VIP 15 % → 6.000 × 0,85 = $5.100; cupón 10 % → 5.100 × 0,90 = $4.590
5. 4.590 es menor que $5.000 → se cobra el mínimo → **resultado esperado: $5.000**

**CP-32 · peso = 5 kg, urbana, frecuente, día 1, sin cupón**
1. Tramo 2 → $9.000
2. Urbana: sin recargo → $9.000
3. Lunes: sin recargo → $9.000
4. Frecuente 5 %, sin cupón → 9.000 × 0,95 = $8.550
5. Es mayor que $5.000. Se redondea a $100: los $50 redondean hacia arriba → **resultado esperado: $8.600**

**CP-36 · peso = 20 kg, nacional, frecuente, día 7 (domingo), cupón ENVIO10**
1. Tramo: 20 > 10, tramo 3 → 9.000 + (20 − 10) × 800 = $17.000
2. Zona nacional +50 % → 17.000 × 1,50 = $25.500
3. Domingo, recargo antes de los descuentos → 25.500 + 2.000 = $27.500
4. Ambos descuentos: frecuente 5 % → 27.500 × 0,95 = $26.125; cupón 10 % → 26.125 × 0,90 = $23.512,50
5. Es mayor que $5.000. Se redondea a $100 (12,50 < 50, baja) → **resultado esperado: $23.500**

## 3.6 Matriz de trazabilidad actualizada

| Requisito | Historia | Casos de prueba |
|-----------|----------|-----------------|
| R1 | HU-1 | CP-01, CP-02, CP-03, CP-04, CP-05, CP-06 |
| R2 | HU-1 | CP-07, CP-08, CP-09 |
| R3 | HU-2 | CP-03, CP-04, CP-06, CP-10 a CP-16, CP-36 |
| R4 | HU-2 | CP-17, CP-18, CP-19, CP-23, CP-27, CP-28, CP-36 |
| R5 | HU-2 | CP-20, CP-21, CP-22, CP-23, CP-28, CP-36, TD-01 a TD-12 |
| R6 | HU-3 | CP-23 a CP-28, CP-35, CP-36, TD-01 a TD-12 |
| R7 | HU-1 | CP-29, CP-30 |
| R8 | HU-3 | CP-06, CP-15, CP-31 a CP-36, TD-05 a TD-12 |
