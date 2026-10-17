"""
SIGMA — generador de indice.json para CronoMX
=============================================
Toma el GTFS limpio (Metro + Metrobús), construye el grafo, calcula tiempos
mínimos a cada polo de empleo, aplica el tramo Mexibús y el IM de CONAPO, y
exporta un JSON estático que consume el frontend.

Uso (desde la raíz del repo, sigma-cronomx/):
    python backend/sigma_indice.py

"""
import json
import os
from datetime import date

import networkx as nx
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# CONFIGURACIÓN
# ----------------------------------------------------------------------------
RUTA_GTFS = "backend/gtfs_limpio/"
RUTA_IM_CSV = "backend/datos/conapo_im_2020.csv"
RUTA_SALIDA = "frontend/public/data/indice.json"

TRANSBORDO_MIN = 5.0          # mismo supuesto que el grafo base
DECAIMIENTO_MIN = 120.0       # Acc_Relativa = max(0, 1 - t/120)
VELOCIDAD_BRT_KMH = 20.0      # velocidad comercial supuesta del Mexibús (ESTIMACIÓN)
# Tramo "puerta a estación" (el GTFS empieza en la estación, no en tu casa). ESTIMACIONES:
VELOCIDAD_ACCESO_KMH = 15.0   # combi/colectivo en tráfico urbano
FACTOR_RODEO = 1.3            # distancia por calle ≈ 1.3 × línea recta
ESPERA_INICIAL_MIN = 7.0      # espera del primer vehículo
IPT_MAX_TEORICO = 2.0         # (1-0) * (1+1): sirve para escalar a 0-100

DESTINOS = {
    "Centro CDMX": "B_0200L2-PINOSUAREZ",
    "Reforma / Polanco": "B_0200L7-POLANCO",
    "Santa Fe (Observatorio)": "B_0200L1-OBSERVATORIO",
}

# km_mexibus: distancia del tramo Mexibús que NO está en el GTFS (None = sin Mexibús)
# im_provisional: se usa solo si no existe el CSV de CONAPO
ORIGENES = {
    "Ecatepec":       {"nodo": "B_0200LB-CIUDADAZTECA", "lat": 19.6015, "lng": -99.0503, "km_mexibus": None, "im_provisional": 0.75},
    "Nezahualcóyotl": {"nodo": "B_0200LB-NEZAHUALCO",   "lat": 19.4003, "lng": -99.0148, "km_mexibus": None, "im_provisional": 0.60},
    "Chimalhuacán":   {"nodo": "B_0200LA-PANTITLAN",    "lat": 19.4150, "lng": -98.9950, "km_mexibus": 18.2, "im_provisional": 0.85},
    "Tecámac":        {"nodo": "B_0200L3-INDIOSVERD",   "lat": 19.7128, "lng": -98.9767, "km_mexibus": 22.3, "im_provisional": 0.55},
}
# Nombre con el que cada municipio aparece en el CSV de CONAPO
NOMBRE_CONAPO = {
    "Ecatepec": "Ecatepec de Morelos",
    "Nezahualcóyotl": "Nezahualcóyotl",
    "Chimalhuacán": "Chimalhuacán",
    "Tecámac": "Tecámac",
}


# ----------------------------------------------------------------------------
# 1. GRAFO
# ----------------------------------------------------------------------------
def a_minutos(hora):
    if pd.isna(hora):
        return np.nan
    h, m, s = map(int, hora.split(":"))
    return h * 60 + m + s / 60.0


def construir_grafo(ruta):
    stops = pd.read_csv(ruta + "stops.csv")
    st = pd.read_csv(ruta + "stop_times.csv")
    st["t"] = st["arrival_time"].apply(a_minutos)
    st = st.sort_values(["trip_id", "stop_sequence"])
    st["sig"] = st.groupby("trip_id")["stop_id"].shift(-1)
    st["t_sig"] = st.groupby("trip_id")["t"].shift(-1)
    st["tramo"] = st["t_sig"] - st["t"]
    e = st.dropna(subset=["sig", "tramo"])
    e = e[e["tramo"] > 0]

    # Si hay varios viajes sobre el mismo tramo, nos quedamos con el mínimo
    e = e.groupby(["stop_id", "sig"], as_index=False)["tramo"].min()

    G = nx.DiGraph()
    for a, b, w in e.itertuples(index=False):
        G.add_edge(a, b, weight=float(w))

    for _, grupo in stops.groupby("stop_name"):
        ids = grupo["stop_id"].tolist()
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                G.add_edge(ids[i], ids[j], weight=TRANSBORDO_MIN)
                G.add_edge(ids[j], ids[i], weight=TRANSBORDO_MIN)
    return G


# ----------------------------------------------------------------------------
# 2. IM
# ----------------------------------------------------------------------------
def cargar_im():
    """Devuelve {municipio: (im_0a1, fuente)}."""
    if os.path.exists(RUTA_IM_CSV):
        df = pd.read_csv(RUTA_IM_CSV)
        lo, hi = df["im_raw"].min(), df["im_raw"].max()
        df["im"] = (hi - df["im_raw"]) / (hi - lo)  # invertido: 1 = más marginado
        por_nombre = dict(zip(df["municipio"].str.strip(), df["im"]))
        salida = {}
        for k, nombre in NOMBRE_CONAPO.items():
            if nombre not in por_nombre:
                raise SystemExit(f"'{nombre}' no aparece en {RUTA_IM_CSV}")
            salida[k] = (float(por_nombre[nombre]), "CONAPO 2020 (Edomex, min-max invertido)")
        return salida
    print(f"[AVISO] No existe {RUTA_IM_CSV}: se usan IM PROVISIONALES.")
    return {k: (v["im_provisional"], "provisional") for k, v in ORIGENES.items()}


def cargar_catalogo():
    """Todos los municipios del Edomex con su IM normalizado (para el buscador)."""
    if not os.path.exists(RUTA_IM_CSV):
        return []
    df = pd.read_csv(RUTA_IM_CSV)
    lo, hi = df["im_raw"].min(), df["im_raw"].max()
    df["im"] = ((hi - df["im_raw"]) / (hi - lo)).round(3)
    df["municipio"] = df["municipio"].str.strip()
    return [{"nombre": r.municipio, "im": float(r.im)} for r in df.itertuples()]


# ----------------------------------------------------------------------------
# 3. CÁLCULO
# ----------------------------------------------------------------------------
def haversine_km(lat1, lng1, lat2, lng2):
    r = 6371.0
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi, dl = p2 - p1, np.radians(lng2 - lng1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return float(2 * r * np.arcsin(np.sqrt(a)))


def tiempo(G, a, b):
    try:
        return nx.shortest_path_length(G, a, b, weight="weight")
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return float("inf")


def main():
    G = construir_grafo(RUTA_GTFS)
    print(f"Grafo: {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")
    im = cargar_im()
    stops = pd.read_csv(RUTA_GTFS + "stops.csv").set_index("stop_id")

    municipios = []
    for nombre, o in ORIGENES.items():
        if o["nodo"] not in G:
            raise SystemExit(f"stop_id no existe en el GTFS: {o['nodo']}")

        # Tramo Mexibús (+ transbordo a Metro) que el GTFS no contiene
        mexibus = 0.0
        acceso = 0.0
        if o["km_mexibus"]:
            mexibus = o["km_mexibus"] / VELOCIDAD_BRT_KMH * 60 + TRANSBORDO_MIN
        else:
            # Del centro del municipio a la estación de origen (combi/colectivo)
            est = stops.loc[o["nodo"]]
            km = haversine_km(o["lat"], o["lng"], est["stop_lat"], est["stop_lon"]) * FACTOR_RODEO
            acceso = km / VELOCIDAD_ACCESO_KMH * 60
        extra = mexibus + acceso + ESPERA_INICIAL_MIN

        destinos = []
        for dn, did in DESTINOS.items():
            t = tiempo(G, o["nodo"], did)
            destinos.append({
                "nombre": dn,
                "stop_id": did,
                "tp_min": None if np.isinf(t) else round(t + extra, 1),
            })

        validos = [d["tp_min"] for d in destinos if d["tp_min"] is not None]
        mejor = min(validos) if validos else None
        acc = max(0.0, 1 - mejor / DECAIMIENTO_MIN) if mejor is not None else 0.0
        im_val, im_fuente = im[nombre]
        ipt = (1 - acc) * (1 + im_val)

        municipios.append({
            "id": nombre.lower().replace("á", "a").replace("ó", "o").replace("é", "e").replace(" ", "-"),
            "nombre": nombre,
            "nombre_conapo": NOMBRE_CONAPO[nombre],
            "lat": o["lat"],
            "lng": o["lng"],
            "nodo_origen": o["nodo"],
            "tramo_mexibus_min": round(mexibus, 1) if mexibus else None,
            "acceso_min": round(acceso, 1) if acceso else None,
            "espera_min": ESPERA_INICIAL_MIN,
            "destinos": destinos,
            "mejor_tp_min": mejor,
            "acc_relativa": round(acc, 3),
            "im": round(im_val, 3),
            "im_fuente": im_fuente,
            "ipt_comp": round(ipt, 3),
            "ipt_100": round(min(100.0, ipt / IPT_MAX_TEORICO * 100), 1),
        })

    salida = {
        "meta": {
            "proyecto": "CronoMX / SIGMA",
            "version_datos": "v1-piloto",
            "generado": date.today().isoformat(),
            "formula": "IPT_comp = (1 - Acc_Relativa) * (1 + IM); Acc_Relativa = max(0, 1 - t/120)",
            "parametros": {
                "decaimiento_min": DECAIMIENTO_MIN,
                "transbordo_min": TRANSBORDO_MIN,
                "velocidad_mexibus_kmh": VELOCIDAD_BRT_KMH,
                "velocidad_acceso_kmh": VELOCIDAD_ACCESO_KMH,
                "factor_rodeo": FACTOR_RODEO,
                "espera_inicial_min": ESPERA_INICIAL_MIN,
            },
            "advertencias": [
                "Tiempos de Metro/Metrobús salen del GTFS SEMOVI CDMX (versión 31-oct-2022).",
                "El tramo Mexibús es una estimación distancia/velocidad: no existe GTFS público de Mexibús.",
                "El tramo del centro del municipio a la estación y la espera inicial son estimaciones (velocidad y factor de rodeo supuestos). No incluye esperas en transbordos, caminata fina, congestión del Metrobús ni saturación.",
                "No se calculan tiempos en auto: el comparador aún no tiene esa fuente.",
            ],
        },
        "municipios": municipios,
        "catalogo": cargar_catalogo(),
    }

    os.makedirs(os.path.dirname(RUTA_SALIDA), exist_ok=True)
    with open(RUTA_SALIDA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)

    print(f"\nEscrito: {RUTA_SALIDA}")
    for m in municipios:
        print(f"  {m['nombre']:<15} mejor={m['mejor_tp_min']} min  acc={m['acc_relativa']}  "
              f"IM={m['im']} ({m['im_fuente']})  IPT={m['ipt_comp']}  ipt_100={m['ipt_100']}")


if __name__ == "__main__":
    main()