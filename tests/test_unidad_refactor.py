"""Pruebas de unidad de las piezas extraidas en la refactorizacion (v2.0.0).

Aplican el nivel de unidad y de integracion del plan de pruebas: cada
funcion se prueba sola y las estrategias de zona se prueban por separado.
"""
import inspect
from decimal import Decimal

import pytest

import envios
from envios import (
    ZonaNacional, ZonaRural, ZonaUrbana, aplicar_costo_minimo, aplicar_descuento,
    es_fin_de_semana, obtener_descuento_cupon, obtener_zona, redondear, tarifa_base,
)

pytestmark = pytest.mark.skipif(
    not hasattr(envios, "ZonaUrbana"), reason="solo aplica tras la refactorizacion"
)


def test_calc_ya_no_tiene_argumento_flag():
    assert "flag" not in inspect.signature(envios.calc).parameters


@pytest.mark.parametrize("peso, esperado", [
    ("0.01", "6000"), ("2.99", "6000"), ("3", "9000"), ("10", "9000"),
    ("10.5", "9400"), ("50", "41000"),
])
def test_tarifa_base(peso, esperado):
    assert tarifa_base(Decimal(peso)) == Decimal(esperado)


@pytest.mark.parametrize("zona, esperado", [
    (ZonaUrbana(), "9000"), (ZonaRural(), "10800"), (ZonaNacional(), "13500"),
])
def test_estrategias_de_zona(zona, esperado):
    assert zona.aplicar_recargo(Decimal("9000")) == Decimal(esperado)


def test_obtener_zona_devuelve_la_estrategia_correcta():
    assert isinstance(obtener_zona("rural"), ZonaRural)
    with pytest.raises(ValueError, match="zona"):
        obtener_zona("internacional")


@pytest.mark.parametrize("dia, esperado", [
    (1, False), (5, False), (6, True), (7, True),
])
def test_es_fin_de_semana(dia, esperado):
    assert es_fin_de_semana(dia) is esperado


def test_descuento_de_cupon():
    assert obtener_descuento_cupon(None) == Decimal("0")
    assert obtener_descuento_cupon("ENVIO10") == Decimal("0.10")
    with pytest.raises(ValueError, match="cupon"):
        obtener_descuento_cupon("OTRO")


def test_aplicar_descuento_y_minimo():
    assert aplicar_descuento(Decimal("10000"), Decimal("0.15")) == Decimal("8500")
    assert aplicar_costo_minimo(Decimal("4590")) == Decimal("5000")
    assert aplicar_costo_minimo(Decimal("5130")) == Decimal("5130")


@pytest.mark.parametrize("valor, esperado", [
    ("8549.99", 8500), ("8550", 8600), ("8550.01", 8600),
    ("23512.5", 23500), ("6885", 6900), ("5000", 5000),
])
def test_redondear_los_50_suben(valor, esperado):
    assert redondear(Decimal(valor)) == esperado
