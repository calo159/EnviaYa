"""Casos de caja negra (Parte 3).

Los resultados esperados se calcularon a mano con la especificacion del
codigo 0182410125: PMAX=50, L1=3 (no incluido), L2=10, rural 20 %,
nacional 50 %, VIP 15 %, fin de semana $2.000 antes de los descuentos,
descuentos acumulados (cliente y luego cupon) y cupon inexistente = error.
"""
import pytest

from envios import calc


# ---------- R1: peso valido ----------

@pytest.mark.parametrize("caso, peso", [
    ("CP-01", 0),
    ("CP-02", -0.01),
    ("CP-05", 50.01),
])
def test_r1_peso_invalido(caso, peso):
    with pytest.raises(ValueError, match="peso inv[aá]lido"):
        calc(peso, "urbana", "normal", 1)


@pytest.mark.parametrize("caso, peso, esperado", [
    ("CP-03", 0.01, 6000),
    ("CP-04", 50, 41000),
    ("CP-06", 49.99, 41000),   # 9000 + 39,99*800 = 40992 -> 41000
])
def test_r1_peso_en_los_limites_validos(caso, peso, esperado):
    assert calc(peso, "urbana", "normal", 1) == esperado


# ---------- R2: zona y dia validos ----------

def test_cp07_zona_invalida_es_error():
    with pytest.raises(ValueError):
        calc(5, "internacional", "normal", 1)


@pytest.mark.parametrize("caso, dia", [
    ("CP-08", 0),
    ("CP-09", 8),
])
def test_r2_dia_fuera_de_rango_es_error(caso, dia):
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", dia)


# ---------- R3: tarifa base por tramos ----------

@pytest.mark.parametrize("caso, peso, esperado", [
    ("CP-10", 2.99, 6000),
    ("CP-11", 3, 9000),        # L1 no se incluye en el tramo 1
    ("CP-12", 3.01, 9000),
    ("CP-13", 9.99, 9000),
    ("CP-14", 10, 9000),       # L2 si se incluye en el tramo 2
    ("CP-15", 10.01, 9000),    # 9008 -> 9000
    ("CP-16", 25, 21000),
])
def test_r3_tarifa_base(caso, peso, esperado):
    assert calc(peso, "urbana", "normal", 1) == esperado


# ---------- R4: recargo por zona ----------

@pytest.mark.parametrize("caso, zona, esperado", [
    ("CP-17", "urbana", 9000),
    ("CP-18", "rural", 10800),
    ("CP-19", "nacional", 13500),
])
def test_r4_recargo_por_zona(caso, zona, esperado):
    assert calc(5, zona, "normal", 1) == esperado


# ---------- R5: fin de semana ----------

@pytest.mark.parametrize("caso, dia, esperado", [
    ("CP-20", 5, 9000),
    ("CP-21", 6, 11000),
    ("CP-22", 7, 11000),
])
def test_r5_recargo_fin_de_semana(caso, dia, esperado):
    assert calc(5, "urbana", "normal", dia) == esperado


def test_cp23_recargo_finde_va_antes_del_descuento():
    # 9000*1,20 = 10800; +2000 = 12800; *0,85 = 10880 -> 10900
    assert calc(5, "rural", "vip", 6) == 10900


# ---------- R6: descuentos ----------

def test_cp24_cliente_frecuente():
    assert calc(2, "urbana", "frecuente", 1) == 5700


def test_cp25_cliente_vip():
    assert calc(2, "urbana", "vip", 1) == 5100


def test_cp26_cupon_envio10():
    assert calc(5, "urbana", "normal", 1, "ENVIO10") == 8100


def test_cp27_vip_y_cupon_se_aplican_ambos():
    # 13500*0,85 = 11475; *0,90 = 10327,5 -> 10300
    assert calc(5, "nacional", "vip", 1, "ENVIO10") == 10300


def test_cp28_frecuente_cupon_y_domingo():
    # 10800 + 2000 = 12800; *0,95 = 12160; *0,90 = 10944 -> 10900
    assert calc(5, "rural", "frecuente", 7, "ENVIO10") == 10900


# ---------- R7: cupon inexistente ----------

def test_cp29_cupon_inexistente_es_error():
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", 1, "DESCUENTO99")


def test_cp30_cupon_en_minuscula_no_existe():
    with pytest.raises(ValueError):
        calc(5, "urbana", "vip", 6, "envio10")


# ---------- R8: minimo y redondeo ----------

def test_cp31_costo_minimo():
    # 6000*0,85 = 5100; *0,90 = 4590 -> minimo 5000
    assert calc(1, "urbana", "vip", 1, "ENVIO10") == 5000


def test_cp32_los_50_redondean_hacia_arriba():
    # 9000*0,95 = 8550 -> 8600
    assert calc(5, "urbana", "frecuente", 1) == 8600


def test_cp33_redondeo_hacia_arriba():
    # 8550*0,90 = 7695 -> 7700
    assert calc(5, "urbana", "frecuente", 1, "ENVIO10") == 7700


def test_cp34_redondeo_hacia_abajo():
    # 9000 + 0,06*800 = 9048 -> 9000
    assert calc(10.06, "urbana", "normal", 1) == 9000


def test_cp35_justo_sobre_el_minimo():
    # 6000*0,95 = 5700; *0,90 = 5130 -> 5100
    assert calc(1, "urbana", "frecuente", 1, "ENVIO10") == 5100


def test_cp36_caso_combinado():
    # 17000*1,50 = 25500; +2000 = 27500; *0,95 = 26125; *0,90 = 23512,5 -> 23500
    assert calc(20, "nacional", "frecuente", 7, "ENVIO10") == 23500


# ---------- Tabla de decision: cliente x cupon x fin de semana ----------
# peso 5 kg, zona urbana. Dia 1 = entre semana, dia 6 = sabado.

@pytest.mark.parametrize("regla, cliente, cupon, dia, esperado", [
    ("TD-01", "normal", None, 1, 9000),
    ("TD-02", "normal", None, 6, 11000),
    ("TD-03", "normal", "ENVIO10", 1, 8100),
    ("TD-04", "normal", "ENVIO10", 6, 9900),
    ("TD-05", "frecuente", None, 1, 8600),       # 8550
    ("TD-06", "frecuente", None, 6, 10500),      # 10450
    ("TD-07", "frecuente", "ENVIO10", 1, 7700),  # 7695
    ("TD-08", "frecuente", "ENVIO10", 6, 9400),  # 9405
    ("TD-09", "vip", None, 1, 7700),             # 7650
    ("TD-10", "vip", None, 6, 9400),             # 9350
    ("TD-11", "vip", "ENVIO10", 1, 6900),        # 6885
    ("TD-12", "vip", "ENVIO10", 6, 8400),        # 8415
])
def test_tabla_de_decision(regla, cliente, cupon, dia, esperado):
    assert calc(5, "urbana", cliente, dia, cupon) == esperado
