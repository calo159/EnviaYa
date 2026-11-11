# envios.py
CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.20,    # como fracción, ej. 0.15
    "RECARGO_NACIONAL": 0.50,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,    # en pesos
}

def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > 50:
        raise ValueError("peso invalido")
    if p < CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    else:
        raise ValueError("zona invalida")
    # fin de semana
    if d > 6:
        t = t + CONFIG["RECARGO_FINDE"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup != None:
        if cup == "ENVIO10":
            t = t - t * 0.10
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(t / 100) * 100
