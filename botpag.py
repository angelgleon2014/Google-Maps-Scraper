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

    # Iniciar la búsqueda con la consulta
    next_page_token = None
    while True:
        try:
            # Hacer la consulta inicial o con el token de la página siguiente
            if next_page_token:
                results = gmaps.places(query=query, page_token=next_page_token)
            else:
                results = gmaps.places(query=query)
            
            print(f"Resultados encontrados: {len(results.get('results', []))}")

            # Iterar sobre los resultados
            for lugar in results.get("results", []):
                nombre = lugar.get("name")
                direccion = lugar.get("formatted_address")
                place_id = lugar.get("place_id")

                # Obtener el teléfono mediante la consulta detallada
                detalles = gmaps.place(place_id=place_id, fields=["formatted_phone_number"])
                telefono = detalles.get("result", {}).get("formatted_phone_number", "")

                

                if telefono and telefono.startswith("9"):
                    # print(f"Guardando: {nombre}, {telefono}")
                    # Mostrar para depuración
                    print("---- Lugar ----")
                    print("Nombre:", nombre)
                    print("Dirección:", direccion)
                    print("Teléfono:", telefono)
                    datos.append({
                        "Negocio": nombre,
                        "Dirección": direccion,
                        "Teléfono": telefono
                    })

            # Si existe un next_page_token, obtenemos la siguiente página
            next_page_token = results.get("next_page_token")

            # Si no hay más resultados, salimos del ciclo
            if not next_page_token:
                break

            # Espera antes de hacer la siguiente solicitud para evitar sobrecargar la API
            time.sleep(2)

        except Exception as e:
            print(f"Error en búsqueda: {e}")
            break

    time.sleep(1.5)  # evitar sobrecarga de la API

# Verifica que haya datos
if datos:
    df = pd.DataFrame(datos)
    print(f"Total de negocios con teléfono que comiencen por 9 encontrados: {len(datos)}")
    df.to_excel("negocios_independencia.xlsx", index=False)
    print("✅ Archivo Excel generado: negocios_independencia.xlsx")
else:
    print("⚠️ No se encontraron negocios con teléfono 9.")
