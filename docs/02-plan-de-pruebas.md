# Parte 2 · Plan de pruebas

## 2.1 Alcance

**Dentro del alcance**

- La función de cálculo de costo de envío de `envios.py` (`calc`), versión heredada 1.0.0 y sus versiones corregidas.
- Las reglas R1 a R8 con mis parámetros: PMAX = 50, L1 = 3 (no incluido), L2 = 10, rural 20 %, nacional 50 %, VIP 15 %, fin de semana $2.000 antes de descuentos, descuentos acumulados (cliente y luego cupón), cupón inexistente = error.
- La solicitud de cambio 0 (zona insular), una vez implementada.

**Fuera del alcance**

- Interfaz de usuario, base de datos, facturación y cualquier otro módulo de EnvíaYa: no existen en el código entregado.
- Pruebas de rendimiento, carga y seguridad: la función es un cálculo puro sin entrada/salida.
- Validación de tipos (por ejemplo, peso como texto): la especificación no la define.

## 2.2 Niveles de prueba y cómo se aplican a este caso

| Nivel | Cómo se aplica aquí |
|-------|---------------------|
| **Unidad** | Es el nivel principal. Se prueba `calc` de forma aislada con pytest: particiones, valores límite de peso (0, 3, 10, 50), tabla de decisión y caminos independientes. Tras la refactorización también se prueban por separado las funciones extraídas (tarifa base, redondeo) y cada estrategia de zona. |
| **Integración** | En la versión heredada hay una sola función, así que no hay nada que integrar. Después de refactorizar sí: se verifica que `calc` combine bien tarifa base + estrategia de zona + recargo de fin de semana + descuentos + redondeo. Los casos combinados (por ejemplo CP-23, CP-27, CP-28 y CP-36) cumplen ese papel porque atraviesan todas las piezas en orden. |
| **Sistema** | Se prueba el módulo completo como caja negra desde su interfaz pública (`from envios import calc`), ejecutando toda la suite en un ambiente limpio y comprobando R1–R8 de punta a punta, incluidos los errores. En un EnvíaYa real este nivel incluiría la pantalla de cotización y el servicio que llama a la función. |
| **Aceptación** | Los criterios Dado/Cuando/Entonces de HU-1, HU-2 y HU-3 se ejecutan como pruebas de aceptación. El “cliente” (el docente, en la sustentación) valida que los resultados coinciden con los calculados a mano en la Parte 3. |

## 2.3 Estrategia

1. **Diseño de caja negra** a partir de la especificación: particiones de equivalencia, análisis de valores límite y tabla de decisión (Parte 3).
2. **Diseño de caja blanca** sobre el código heredado: grafo de flujo, complejidad ciclomática y caminos independientes (Parte 4).
3. **Automatización** de todos los casos con pytest. Los resultados esperados se calculan a mano desde la especificación, nunca ejecutando el código.
4. **Ejecución contra el código heredado** (v1.0.0) para detectar defectos; cada fallo se analiza y se registra (Parte 5).
5. **Corrección** de cada defecto en su rama, y **regresión**: la misma suite completa se ejecuta después de cada corrección y después de la refactorización.
6. **Cobertura** de sentencias y ramas con pytest-cov; meta: 100 % de sentencias y ≥ 95 % de ramas.
7. Para la solicitud de cambio se usa **TDD**: primero las pruebas (rojo), luego el código (verde).

## 2.4 Ambiente

| Elemento | Valor |
|----------|-------|
| Sistema operativo | Windows 11 Pro |
| Lenguaje | Python 3.13 |
| Framework de pruebas | pytest 9.2 |
| Cobertura | pytest-cov 7.1 (coverage 7.17), con medición de ramas |
| Complejidad | radon 6.0 |
| Control de versiones | Git 2.54 + GitHub (`calo159/EnviaYa`) |
| Datos de prueba | Valores escritos en los propios casos; no hay datos externos |

Comando de ejecución: `python -m pytest --cov=envios --cov-branch --cov-report=term-missing`

## 2.5 Roles

Trabajo individual; una sola persona asume todos los roles.

| Rol | Responsabilidad | Quién |
|-----|-----------------|-------|
| Analista de pruebas | Especificación, historias, diseño de casos | Carlos David Sierra |
| Automatizador | Scripts de pytest y medición de cobertura | Carlos David Sierra |
| Desarrollador de mantenimiento | Correcciones y refactorización | Carlos David Sierra |
| Gestor de configuración | Ramas, etiquetas, CHANGELOG | Carlos David Sierra |
| Cliente / aprobador | Aceptación en la sustentación | Docente |

## 2.6 Riesgos y mitigación

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|--------|-------|---------|------------|
| 1 | Resultado esperado mal calculado a mano (una prueba “correcta” que valida algo errado) | Media | Alto | Mostrar el cálculo paso a paso; revisar cada caso que falle antes de declararlo defecto. |
| 2 | Parámetros personalizados mal derivados del código estudiantil | Baja | Muy alto (nota 0) | Tabla de parámetros con las fórmulas resueltas al inicio; `CONFIG` verificado contra ella. |
| 3 | La refactorización introduce defectos nuevos | Media | Alto | Suite de regresión completa antes y después; cambios pequeños en ramas separadas. |
| 4 | Errores de precisión con decimales (pesos como 10,01 o descuentos encadenados) que alteran el redondeo | Media | Medio | Casos en los límites del redondeo ($49, $50, $51); usar aritmética decimal exacta en la versión corregida. |
| 5 | Ambigüedad de la especificación (cliente inválido, orden mínimo/redondeo) | Media | Medio | Documentar la interpretación adoptada en la Parte 1 y marcarla como pregunta abierta. |
| 6 | Tiempo limitado (un solo día) | Alta | Medio | Priorizar por riesgo: primero límites y reglas que dependen de la paridad; commits frecuentes. |
| 7 | Conflictos al integrar varias ramas de corrección sobre el mismo archivo | Media | Bajo | Una rama por defecto, integradas una a una y con la suite ejecutada tras cada merge. |

## 2.7 Criterios de entrada

- Especificación R1–R8 escrita con mis parámetros y `CONFIG` diligenciado.
- Código heredado bajo control de versiones y etiquetado como `v1.0.0`.
- Ambiente instalado (Python, pytest, pytest-cov) y la suite ejecutable.
- Casos de prueba diseñados, con resultado esperado calculado a mano.

## 2.8 Criterios de salida

- 100 % de los casos diseñados ejecutados.
- 100 % de los casos pasan sobre la versión corregida.
- Ningún defecto abierto de severidad crítica o alta; todo defecto registrado está corregido y verificado con su caso.
- Cobertura de sentencias = 100 % y de ramas ≥ 95 %.
- Matriz de trazabilidad completa: cada requisito tiene al menos un caso que pasa.
- Versión nueva etiquetada y CHANGELOG actualizado.

**Criterios de suspensión:** si la suite no puede ejecutarse (error de importación o de ambiente) se suspenden las pruebas hasta corregir el ambiente.
