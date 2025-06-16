import requests
import pandas as pd
import os
import time
from pathlib import Path

API_KEY = "AIzaSyCgtdzp165f4fSBTyqgyVFthJ8cXT7QSxY"
""" TIPOS_NEGOCIOS = [
    "Restaurantes", "Cafeterías", "Panaderías", "Bares", "Heladerías", "Abarrotes", "Supermercados",
    "Carnicerías", "Verdulerías", "Botillerías", "Food", "Suplementos", "Delivery", "Ropa", "Zapaterías",
    "Librerías", "Jugueterías", "Electrónica", "Ferreterías", "Farmacias", "Perfumerías", "Deportivos",
    "Mascotas", "Florerías", "Tabaquerías", "Ópticas", "Regalos", "Bazares", "Muebles", "Peluquerías",
    "Belleza", "Spas", "Lavanderías", "Costurerías", "Reparación", "Fotografía", "Niños", "Adultos",
    "Consultas", "Dentales", "Kinesiología", "Laboratorios", "Psicología", "Gimnasios", "Yoga", "Colegios",
    "Idiomas", "Tutoría", "Música", "Capacitación", "Abogados", "Consultorías", "Diseño", "Contables",
    "Viajes", "Notarías", "Propiedades", "Copiado", "Informática", "Empleo", "Bencineras", "Mecánicos",
    "Lavado", "Repuestos", "Taxi", "Mudanzas", "Cines", "Teatros", "Conciertos", "Eventos", "Juegos",
    "Parques", "Bancos", "Correo", "Veterinarios", "Cerrajeros", "Limpieza", "Jardinería", "Funerarias"
] """

TIPOS_NEGOCIOS = [
    "Restaurantes"
]

LOCATION = "-33.4058,-70.641"
RADIUS = 5000

resultados = []

def buscar_negocios(tipo):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{tipo} en Independencia, Santiago",
        "location": LOCATION,
        "radius": RADIUS,
        "key": API_KEY
    }

    while True:
        res = requests.get(url, params=params)
        data = res.json()

        for lugar in data.get("results", []):
            place_id = lugar["place_id"]
            detalles = obtener_detalles(place_id)
            if detalles:
                resultados.append(detalles)
                crear_sitio_web(detalles)

        if "next_page_token" in data:
            time.sleep(2)
            params = {"pagetoken": data["next_page_token"], "key": API_KEY}
        else:
            break

def obtener_detalles(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,place_id,photos",
        "key": API_KEY
    }
    res = requests.get(url, params=params)
    data = res.json().get("result", {})

    telefono = data.get("formatted_phone_number", "").replace(" ", "")
    if data.get("website") is None and telefono.startswith("9"):
        return {
            "nombre": data.get("name"),
            "direccion": data.get("formatted_address"),
            "telefono": telefono,
            "place_id": data.get("place_id")
        }
    return None

def crear_sitio_web(negocio):
    nombre = negocio['nombre'].strip().replace("/", "-").replace("\\", "-")
    ruta_directorio = Path("sitios") / nombre
    ruta_directorio.mkdir(parents=True, exist_ok=True)

    telefono_formateado = f"569{negocio['telefono'][1:]}"
    html = f"""
    <!DOCTYPE html>
    <html lang='es'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>{negocio['nombre']}</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 0; background: #fff; color: #333; }}
            header {{ background: #000; color: #fff; padding: 1rem; text-align: center; }}
            main {{ padding: 2rem; }}
            .btn {{ display: inline-block; margin-top: 1rem; padding: 0.75rem 1.5rem; background: #007aff; color: white; border-radius: 10px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <header><h1>{negocio['nombre']}</h1></header>
        <main>
            <p><strong>Dirección:</strong> {negocio['direccion']}</p>
            <p><strong>Teléfono:</strong> +56 {negocio['telefono']}</p>
            <a class='btn' href='https://wa.me/{telefono_formateado}' target='_blank'>Contáctanos</a>
        </main>
    </body>
    </html>
    """

    with open(ruta_directorio / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    for tipo in TIPOS_NEGOCIOS:
        print(f"Buscando: {tipo}")
        buscar_negocios(tipo)
        time.sleep(1)

    df = pd.DataFrame(resultados)
    df.to_excel("negocios_sin_web_independencia.xlsx", index=False)
    print("\nArchivo generado con", len(df), "negocios sin web y sitios creados.")
