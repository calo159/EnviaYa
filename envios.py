"""EnviaYa: calculo del costo de un envio.

Reglas R1 a R8 con los parametros del codigo estudiantil 0182410125.
El patron Estrategia se aplica a las zonas: cada zona sabe como aplicar
su propio recargo, y agregar una zona nueva no obliga a tocar calc().
"""
from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

# --- Parametros del negocio (R1 a R8) ---
PESO_MAXIMO = Decimal("50")               # PMAX
LIMITE_TRAMO_1 = Decimal("3")             # L1 (no incluido: peso < L1)
LIMITE_TRAMO_2 = Decimal("10")            # L2 (incluido: peso <= L2)
TARIFA_TRAMO_1 = Decimal("6000")
TARIFA_TRAMO_2 = Decimal("9000")
TARIFA_POR_KG_EXTRA = Decimal("800")      # por cada kg sobre L2

RECARGO_RURAL = Decimal("0.20")           # RR
RECARGO_NACIONAL = Decimal("0.50")        # RN
RECARGO_INSULAR = Decimal("0.70")         # San Andres (solicitud de cambio)

DIA_SABADO = 6
DIA_DOMINGO = 7
DIA_MINIMO = 1
DIA_MAXIMO = 7
RECARGO_FIN_DE_SEMANA = Decimal("2000")   # S, se suma antes de los descuentos

DESCUENTO_FRECUENTE = Decimal("0.05")
DESCUENTO_VIP = Decimal("0.15")           # V
CUPON_ENVIO10 = "ENVIO10"
DESCUENTO_ENVIO10 = Decimal("0.10")

COSTO_MINIMO = Decimal("5000")
MULTIPLO_REDONDEO = Decimal("100")

DESCUENTOS_CLIENTE = {
    "frecuente": DESCUENTO_FRECUENTE,
    "vip": DESCUENTO_VIP,
}
CUPONES = {
    CUPON_ENVIO10: DESCUENTO_ENVIO10,
}


# --- Estrategia de zona ---
class Zona(ABC):
    """Estrategia: como se aplica el recargo de una zona."""

    acepta_cupon = True

    @abstractmethod
    def aplicar_recargo(self, valor):
        """Devuelve el valor con el recargo de la zona aplicado."""


class ZonaUrbana(Zona):
    def aplicar_recargo(self, valor):
        return valor


class ZonaConRecargoPorcentual(Zona):
    def __init__(self, porcentaje):
        self.porcentaje = porcentaje

    def aplicar_recargo(self, valor):
        return valor + valor * self.porcentaje


class ZonaRural(ZonaConRecargoPorcentual):
    def __init__(self):
        super().__init__(RECARGO_RURAL)


class ZonaNacional(ZonaConRecargoPorcentual):
    def __init__(self):
        super().__init__(RECARGO_NACIONAL)


class ZonaInsular(ZonaConRecargoPorcentual):
    """San Andres: recargo del 70 % y no acepta cupones."""

    acepta_cupon = False

    def __init__(self):
        super().__init__(RECARGO_INSULAR)


ZONAS = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
    "insular": ZonaInsular(),
}


# --- Funciones extraidas ---
def validar_peso(peso):
    """R1: 0 < peso <= PMAX."""
    if peso <= 0 or peso > PESO_MAXIMO:
        raise ValueError("peso invalido")


def obtener_zona(nombre):
    """R2: la zona debe ser una de las validas."""
    try:
        return ZONAS[nombre]
    except KeyError:
        raise ValueError("zona invalida") from None


def validar_dia(dia):
    """R2: el dia debe estar entre 1 y 7."""
    if dia < DIA_MINIMO or dia > DIA_MAXIMO:
        raise ValueError("dia invalido")


def obtener_descuento_cupon(cupon):
    """R7: un cupon que no existe es error. Sin cupon, no hay descuento."""
    if cupon is None:
        return Decimal("0")
    try:
        return CUPONES[cupon]
    except KeyError:
        raise ValueError("cupon invalido") from None


def tarifa_base(peso):
    """R3: tarifa base por tramos."""
    if peso < LIMITE_TRAMO_1:
        return TARIFA_TRAMO_1
    if peso <= LIMITE_TRAMO_2:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (peso - LIMITE_TRAMO_2) * TARIFA_POR_KG_EXTRA


def es_fin_de_semana(dia):
    return dia in (DIA_SABADO, DIA_DOMINGO)


def aplicar_descuento(valor, porcentaje):
    return valor - valor * porcentaje


def aplicar_costo_minimo(valor):
    """R8: el costo nunca es menor al minimo."""
    return max(valor, COSTO_MINIMO)


def redondear(valor):
    """R8: multiplo de 100 mas cercano; los 50 suben."""
    return int((valor / MULTIPLO_REDONDEO).to_integral_value(ROUND_HALF_UP) * MULTIPLO_REDONDEO)


def calc(peso, zona, cliente, dia, cupon=None):
    """Costo del envio en pesos, redondeado a multiplos de 100."""
    peso = Decimal(str(peso))
    validar_peso(peso)
    estrategia_zona = obtener_zona(zona)
    validar_dia(dia)
    descuento_cupon = obtener_descuento_cupon(cupon)
    if cupon is not None and not estrategia_zona.acepta_cupon:
        raise ValueError("los envios insulares no aceptan cupon")

    valor = tarifa_base(peso)
    valor = estrategia_zona.aplicar_recargo(valor)
    if es_fin_de_semana(dia):
        valor += RECARGO_FIN_DE_SEMANA
    valor = aplicar_descuento(valor, DESCUENTOS_CLIENTE.get(cliente, Decimal("0")))
    valor = aplicar_descuento(valor, descuento_cupon)
    valor = aplicar_costo_minimo(valor)
    return redondear(valor)
