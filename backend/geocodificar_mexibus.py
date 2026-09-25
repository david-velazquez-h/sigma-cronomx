"""
Geocodifica las estaciones de Mexibús (Líneas 1-4) usando Nominatim
(el geocodificador gratuito de OpenStreetMap), ya que no hay un GTFS
oficial descargable confirmado todavía.

Esto NO es tan preciso como un GTFS real (las coordenadas son aproximadas,
basadas en el nombre del lugar, no en la ubicación exacta del poste de
la parada), pero es suficiente para el propósito del piloto: saber
en qué municipio cae cada estación.

Uso:
    pip install requests
    python geocodificar_mexibus.py

Importante: Nominatim pide máximo 1 petición por segundo y un User-Agent
identificable pero ps el script ya respeta esto.
"""

import requests
import time
import csv

# Estaciones por línea, tal como aparecen en la página oficial de SITRAMyTEM
LINEAS_MEXIBUS = {
    "1": [
        "Ciudad Azteca", "Quinto Sol", "Josefa Ortíz", "Industrial", "Unitec",
        "Torres", "Zodiaco", "Adolfo López Mateos", "Vocacional 3",
        "Valle De Ecatepec", "Las Américas", "Primero De Mayo",
        "Hospital Las Américas", "Aquiles Serdán", "Jardines De Morelos",
        "Palomas", "19 De Septiembre", "Central De Abasto", "Las Torres",
        "Hidalgo", "Cuauhtémoc Sur", "Cuauhtémoc Norte", "Esmeralda",
        "Ojo De Agua",
    ],
    "1A_AIFA": [
        "Ojo de Agua", "Loma Bonita", "Ozumbilla", "San Francisco",
        "Tecámac", "Glorieta Militar", "Combustibles", "Hacienda",
        "Terminal de Pasajeros AIFA",
    ],
    "2": [
        "La Quebrada", "ERO Estación Retorno Oriente", "Lechería", "Vidriera",
        "Ciudad Labor", "Chilpan", "Recursos Hidráulicos", "COCEM",
        "Buenavista", "Bandera Tultitlán", "Bello Horizonte", "Cartagena",
        "De la Cruz San Mateo", "Fuentes del Valle", "Mariscala Real del Bosque",
        "Villas de San José", "Santa María", "Coacalco Berriozábal",
        "Bosques del Valle", "Ex Hacienda San Felipe", "Coacalco Tultepec",
        "Héroes Canosas", "San Francisco", "Las Flores Zacuatitla",
        "1a de Villa", "Eje 8", "Parque Residencial", "La Laguna",
        "San Carlos", "FOVISSSTE", "Venustiano Carranza", "Guadalupe Victoria",
        "DIF", "Ecatepec", "El Carmen", "ISSEMYM", "Agricultura",
        "San Cristóbal", "UPE", "Casa de Morelos", "Puente de Fierro",
        "San Martín", "1o de Mayo", "Las Américas",
    ],
    "3": [
        "Pantitlán", "Calle 6", "El Barquito", "Maravillas",
        "Vicente Riva Palacio", "Virgencitas", "Nezahualcóyotl",
        "Lago de Chapala", "Adolfo López Mateos", "Palacio Municipal",
        "Sor Juana Inés de la Cruz", "El Castillito", "General Vicente Villada",
        "Rayito de Sol", "Las Mañanitas", "Rancho Grande", "Bordo de Xochiaca",
        "Las Torres", "Guerrero Chimalli", "Las Flores", "Canteros",
        "La Presa", "Embarcadero", "Santa Elena", "Ignacio Manuel Altamirano",
        "San Pablo", "Los Patos", "Refugio", "Acuitlapilco", "Chimalhuacán",
    ],
    "4": [
        "Terminal La Raza", "Indios Verdes", "Periférico",
        "Puente Martin Carrera", "Clínica 76", "Vía Morelos",
        "Monumento a Morelos", "5 de Febrero", "Santa Clara", "Cerro Gordo",
        "Servicios Administrativos", "Clínica 93", "Industrial",
        "La 5a Aparición", "Tulpetlac", "Siervo de la Nación",
        "Nuevo Laredo", "Laureles", "La Viga", "San Cristóbal",
        "Puente de Fierro", "Izcalli Palomas", "Central de Abastos",
        "Santo Tomas Chiconautla", "Ejido Santo Tomás", "Revolución",
        "Margarito F. Ayala", "Las Flores", "Bosques", "Terminal UMB",
    ],
}

HEADERS = {"User-Agent": "CronoMX-SIGMA-proyecto-escolar-ESCOM-IPN"}


def geocodificar(nombre_estacion):
    query = f"{nombre_estacion}, Mexibús, Estado de México, México"
    resp = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": query, "format": "json", "limit": 1},
        headers=HEADERS,
    )
    resultados = resp.json()
    if resultados:
        return float(resultados[0]["lat"]), float(resultados[0]["lon"])
    return None, None


filas = []
for linea, estaciones in LINEAS_MEXIBUS.items():
    for nombre in estaciones:
        lat, lon = geocodificar(nombre)
        estado = "OK" if lat else "NO ENCONTRADA"
        print(f"[{estado}] Línea {linea} — {nombre}")
        filas.append({"linea": linea, "nombre": nombre, "lat": lat, "lon": lon})
        time.sleep(1.1)  # respeta el límite de 1 petición/segundo de Nominatim

with open("mexibus_estaciones_geocodificadas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["linea", "nombre", "lat", "lon"])
    writer.writeheader()
    writer.writerows(filas)

no_encontradas = [f for f in filas if f["lat"] is None]
print(f"\nListo. {len(filas) - len(no_encontradas)}/{len(filas)} estaciones geocodificadas.")
print("Guardado en 'mexibus_estaciones_geocodificadas.csv'")
if no_encontradas:
    print(f"\n{len(no_encontradas)} no se encontraron — revísalas a mano después:")
    for f in no_encontradas:
        print(f"  - Línea {f['linea']}: {f['nombre']}")