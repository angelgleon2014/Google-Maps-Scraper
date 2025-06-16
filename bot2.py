import googlemaps
import time
import pandas as pd

API_KEY = ""
gmaps = googlemaps.Client(key=API_KEY)

CIUDAD = "Independencia, Santiago de Chile"
archivo_lista = "tipos_negocios.txt"

# Leer tipos de negocios
with open(archivo_lista, "r", encoding="utf-8") as f:
    tipos = [line.strip() for line in f if line.strip()]

# Lista para almacenar resultados
datos = []

for tipo in tipos:
    print(f"Buscando: {tipo}")
    query = f"{tipo} en {CIUDAD}"

    try:
        results = gmaps.places(query=query)
        print(f"Resultados encontrados: {len(results.get('results', []))}")
    except Exception as e:
        print(f"Error en búsqueda: {e}")
        continue

    for lugar in results.get("results", []):
        nombre = lugar.get("name")
        direccion = lugar.get("formatted_address")
        place_id = lugar.get("place_id")

        # Obtener el teléfono mediante la consulta detallada
        detalles = gmaps.place(place_id=place_id, fields=["formatted_phone_number"])
        telefono = detalles.get("result", {}).get("formatted_phone_number", "")        

        if telefono.startswith("9"):
            # Mostrar el teléfono y otros datos para depuración
            print("---- Lugar ----")
            print("Nombre:", nombre)
            print("Dirección:", direccion)
            print("Teléfono:", telefono)
            datos.append({
                "Negocio": nombre,
                "Dirección": direccion,
                "Teléfono": telefono
            })

    time.sleep(1.5)  # evitar sobrecarga de la API

# Guardar en Excel
df = pd.DataFrame(datos)
print(f"Total de negocios con teléfono que comiencen por 9 encontrados: {len(datos)}")
df.to_excel("negocios_independencia2.xlsx", index=False)
print("✅ Archivo Excel generado: negocios_independencia2.xlsx")
