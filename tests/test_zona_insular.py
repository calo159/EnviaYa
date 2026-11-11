"""Solicitud de cambio 0: zona insular (San Andres) con recargo del 70 %.
Los envios insulares no aceptan cupon. Escritas ANTES de la implementacion (TDD).

Interpretacion: "no aceptan cupon" = si llega un cupon (valido o no) en un
envio insular, se lanza error, coherente con la regla F impar (cupon invalido
es error) y para que el cliente no crea que tiene un descuento que no recibe.
Los descuentos de cliente (frecuente, vip) y el recargo de fin de semana si aplican.
"""
import pytest

import envios
from envios import calc


@pytest.mark.parametrize("caso, peso, esperado", [
    ("CI-01", 2, 10200),      # 6000 * 1,70
    ("CI-02", 5, 15300),      # 9000 * 1,70
    ("CI-03", 20, 28900),     # 17000 * 1,70
    ("CI-04", 50, 69700),     # 41000 * 1,70
])
def test_recargo_insular_del_70_por_ciento(caso, peso, esperado):
    assert calc(peso, "insular", "normal", 1) == esperado


def test_ci05_insular_en_fin_de_semana_suma_antes_de_descuentos():
    # 9000*1,70 = 15300; +2000 = 17300
    assert calc(5, "insular", "normal", 6) == 17300


def test_ci06_insular_con_cliente_vip():
    # 15300*0,85 = 13005 -> 13000
    assert calc(5, "insular", "vip", 1) == 13000


def test_ci07_insular_frecuente_domingo():
    # 15300 + 2000 = 17300; *0,95 = 16435 -> 16400
    assert calc(5, "insular", "frecuente", 7) == 16400


def test_ci08_insular_vip_sabado_en_el_limite_l1():
    # peso 3 -> 9000; *1,70 = 15300; +2000 = 17300; *0,85 = 14705 -> 14700
    assert calc(3, "insular", "vip", 6) == 14700


def test_ci09_insular_no_acepta_cupon_valido():
    with pytest.raises(ValueError, match="insular"):
        calc(5, "insular", "normal", 1, "ENVIO10")


def test_ci10_insular_no_acepta_cupon_inexistente():
    with pytest.raises(ValueError):
        calc(5, "insular", "vip", 1, "NOEXISTE")


@pytest.mark.parametrize("zona", ["urbana", "rural", "nacional"])
def test_ci11_las_otras_zonas_siguen_aceptando_cupon(zona):
    assert calc(5, zona, "normal", 1, "ENVIO10") > 0


def test_ci12_peso_invalido_sigue_validandose_en_insular():
    with pytest.raises(ValueError, match="peso inv[aá]lido"):
        calc(50.01, "insular", "normal", 1)


def test_ci13_estrategia_insular():
    zona = envios.obtener_zona("insular")
    assert isinstance(zona, envios.ZonaInsular)
    assert zona.acepta_cupon is False
    assert envios.obtener_zona("rural").acepta_cupon is True
