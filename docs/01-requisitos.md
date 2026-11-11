# Parte 1 · Requisitos y criterios de aceptación

## 1.1 Mis parámetros (código 0182410125)

Seis últimos dígitos: **4 1 0 1 2 5** → A=4, B=1, C=0, D=1, E=2, F=5.

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 4 | 1 | 0 | 1 | 2 | 5 | 50 kg | 3 kg | 10 kg | 20 % | 50 % | 15 % | $2.000 | 0 |

Cálculo:

- PMAX = 30 + 5·4 = **50**
- L1 = 2 + (1 mod 3) = **3**
- L2 = 10 + 0 = **10**
- RR = 10 + 5·(2 mod 4) = 10 + 10 = **20 %**
- RN = 40 + 5·(5 mod 3) = 40 + 10 = **50 %**
- V = 10 + 5·(4 mod 3) = 10 + 5 = **15 %**
- S = 2000 + 500·(0 mod 4) = **$2.000**
- CAMBIO = (A + F) mod 3 = (4 + 5) mod 3 = 9 mod 3 = **0** → nueva zona insular (San Andrés), recargo 70 %, sin cupón.

Reglas de paridad:

| Dígito | Valor | Paridad | Regla resultante |
|--------|-------|---------|------------------|
| D (tramo 1) | 1 | impar | Tramo 1 **no incluye** el límite: peso **< 3** |
| E (fin de semana) | 2 | par | El recargo se suma **antes** de los descuentos |
| B (cliente y cupón) | 1 | impar | Se aplican **ambos**: primero el del cliente y luego el cupón |
| F (cupón inexistente) | 5 | impar | Un cupón que no existe es **error** |

## 1.2 Especificación completa (R1–R8) con mis valores

Entradas: `peso` (kg, admite decimales), `zona` (urbana, rural, nacional), `cliente` (normal, frecuente, vip), `dia` (1 a 7; 6 = sábado, 7 = domingo) y `cupon` (opcional).

| ID | Regla |
|----|-------|
| R1 | El peso debe cumplir 0 < peso ≤ 50. Si no, se lanza el error “peso inválido”. |
| R2 | Si la zona no es urbana, rural ni nacional, o el día no está entre 1 y 7, se lanza un error. |
| R3 | Tarifa base. Tramo 1 (peso < 3): $6.000. Tramo 2 (3 ≤ peso ≤ 10): $9.000. Más de 10 kg: $9.000 + $800 por cada kg sobre 10, proporcional. |
| R4 | Recargo por zona. Rural: +20 %. Nacional: +50 %. Urbana: sin recargo. |
| R5 | Fin de semana (día 6 o 7): +$2.000, **antes** de los descuentos. |
| R6 | Descuentos. Cliente frecuente: 5 %. Cliente VIP: 15 %. Cupón ENVIO10: 10 %. Si hay cliente con descuento y cupón se aplican **ambos**: primero el del cliente y luego el cupón (sobre el valor ya descontado). |
| R7 | Un cupón que no existe es **error** (el único cupón válido es `ENVIO10`). |
| R8 | El costo nunca es menor que $5.000. El resultado se redondea al múltiplo de $100 más cercano; los $50 redondean hacia arriba. |

Orden de cálculo: base (R3) → zona (R4) → fin de semana (R5) → descuento de cliente → cupón (R6) → mínimo $5.000 → redondeo (R8).

Decisiones de interpretación (la especificación no las fija; se documentan):

- El mínimo de $5.000 se aplica antes del redondeo.
- Un cliente que no es normal, frecuente ni vip no tiene regla de error en R1–R8; se trata como normal. Queda como pregunta abierta para el negocio.
- `cupon = None` significa “sin cupón”. Cualquier otra cadena distinta de `ENVIO10` (incluido `envio10` en minúscula o cadena vacía) es un cupón inexistente.

## 1.3 Historias de usuario

**HU-1 · Validar el envío (R1, R2, R7)**
Como operador de EnvíaYa quiero que el sistema rechace envíos con datos inválidos para no cobrar ni despachar envíos imposibles.

- *Dado* un peso de 0 kg o negativo, *cuando* calculo el costo, *entonces* se lanza “peso inválido”.
- *Dado* un peso de 50,01 kg, *cuando* calculo el costo, *entonces* se lanza “peso inválido”; con exactamente 50 kg se calcula normalmente.
- *Dado* una zona “insular” (o cualquier valor fuera de urbana, rural y nacional), *cuando* calculo el costo, *entonces* se lanza un error.
- *Dado* un día 0 u 8, *cuando* calculo el costo, *entonces* se lanza un error.
- *Dado* un cupón “DESCUENTO99”, *cuando* calculo el costo, *entonces* se lanza un error (no se ignora).

**HU-2 · Calcular la tarifa con recargos (R3, R4, R5)**
Como cliente quiero conocer el costo según peso, zona y día para saber cuánto pagaré.

- *Dado* un peso de 2,99 kg, *cuando* calculo, *entonces* la base es $6.000; con 3 kg la base es $9.000.
- *Dado* un peso de 10 kg, *cuando* calculo, *entonces* la base es $9.000; con 10,5 kg es $9.400.
- *Dado* una zona rural o nacional, *cuando* calculo, *entonces* se suma 20 % o 50 % a la base.
- *Dado* un día sábado (6) o domingo (7), *cuando* calculo, *entonces* se suman $2.000 antes de aplicar descuentos; de lunes a viernes no se suma.

**HU-3 · Aplicar descuentos, mínimo y redondeo (R6, R8)**
Como cliente frecuente, VIP o con cupón quiero que se apliquen mis descuentos para pagar menos, y como negocio quiero un costo mínimo y un redondeo claro.

- *Dado* un cliente frecuente o VIP, *cuando* calculo, *entonces* se descuenta 5 % o 15 %.
- *Dado* un cliente VIP con cupón ENVIO10, *cuando* calculo, *entonces* se aplican ambos: primero 15 % y luego 10 % sobre el resultado.
- *Dado* un valor calculado menor a $5.000, *cuando* calculo, *entonces* el costo es $5.000.
- *Dado* un valor de $8.550, *cuando* calculo, *entonces* el resultado es $8.600 (los $50 suben); con $8.549 es $8.500.

## 1.4 Matriz de trazabilidad (inicial)

La columna de casos de prueba se completa con el detalle de la Parte 3; la de defectos, en la Parte 5.

| Requisito | Historia | Casos de prueba | Defectos asociados |
|-----------|----------|-----------------|--------------------|
| R1 | HU-1 | CP-01, CP-02, CP-03, CP-04, CP-05, CP-06 | — |
| R2 | HU-1 | CP-07, CP-08, CP-09 | DEF-02, DEF-03 |
| R3 | HU-2 | CP-10, CP-11, CP-12, CP-13, CP-14, CP-15, CP-16 | DEF-01 |
| R4 | HU-2 | CP-17, CP-18, CP-19 | — |
| R5 | HU-2 | CP-20, CP-21, CP-22, CP-23 | DEF-04 |
| R6 | HU-3 | CP-24, CP-25, CP-26, CP-27, CP-28 | — |
| R7 | HU-1 | CP-29, CP-30 | DEF-05 |
| R8 | HU-3 | CP-31, CP-32, CP-33, CP-34 | DEF-06 |
