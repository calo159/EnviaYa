"""Casos de caja blanca (Parte 4): un caso por camino independiente de calc.

V(G) = 15 en el codigo heredado. El esperado sale de la especificacion,
no del codigo: por eso CB-08 y CB-12 fallan contra la version 1.0.0.
"""
import inspect

import pytest

from envios import calc

TIENE_FLAG = "flag" in inspect.signature(calc).parameters


def test_cb01_peso_cero():
    with pytest.raises(ValueError, match="peso inv[aá]lido"):
        calc(0, "urbana", "normal", 1)


def test_cb02_peso_mayor_al_maximo():
    with pytest.raises(ValueError, match="peso inv[aá]lido"):
        calc(51, "urbana", "normal", 1)


def test_cb03_camino_base():
    assert calc(1, "urbana", "normal", 1) == 6000


def test_cb04_tramo_2():
    assert calc(5, "urbana", "normal", 1) == 9000


def test_cb05_tramo_3():
    assert calc(20, "urbana", "normal", 1) == 17000


def test_cb06_zona_rural():
    assert calc(1, "rural", "normal", 1) == 7200


def test_cb07_zona_nacional():
    assert calc(1, "nacional", "normal", 1) == 9000


def test_cb08_zona_que_no_existe():
    with pytest.raises(ValueError):
        calc(1, "internacional", "normal", 1)


def test_cb09_domingo():
    assert calc(1, "urbana", "normal", 7) == 8000


def test_cb10_cliente_frecuente():
    assert calc(1, "urbana", "frecuente", 1) == 5700


def test_cb11_cliente_vip():
    assert calc(1, "urbana", "vip", 1) == 5100


def test_cb12_cupon_que_no_es_envio10():
    with pytest.raises(ValueError):
        calc(1, "urbana", "normal", 1, "NOEXISTE")


def test_cb13_cupon_envio10():
    assert calc(1, "urbana", "normal", 1, "ENVIO10") == 5400


def test_cb14_costo_minimo():
    assert calc(1, "urbana", "vip", 1, "ENVIO10") == 5000


@pytest.mark.skipif(not TIENE_FLAG, reason="el argumento flag se elimino en la v2.0.0")
def test_cb15_flag_imprime_el_costo(capsys):
    assert calc(1, "urbana", "normal", 1, None, True) == 6000
    assert "costo:" in capsys.readouterr().out
