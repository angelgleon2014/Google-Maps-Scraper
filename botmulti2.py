import googlemaps
import time
import pandas as pd
from multiprocessing import Pool, cpu_count

API_KEY = ""
gmaps = googlemaps.Client(key=API_KEY)

CIUDAD = "conchali, Santiago de Chile"

# Función que procesa un solo tipo de negocio
def procesar_tipo(tipo):
    print(f"🔍 Buscando: {tipo}")
    datos_locales = []
    query = f"{tipo} en {CIUDAD}"
    next_page_token = None

    while True:
        try:
            if next_page_token:
                time.sleep(2)  # necesario antes de usar el next_page_token
                results = gmaps.places(query=query, page_token=next_page_token)
            else:
                results = gmaps.places(query=query)

            for lugar in results.get("results", []):
                nombre = lugar.get("name")
                direccion = lugar.get("formatted_address")
                place_id = lugar.get("place_id")

                # Detalles para extraer teléfono
                detalles = gmaps.place(place_id=place_id, fields=["formatted_phone_number"])
                telefono = detalles.get("result", {}).get("formatted_phone_number", "")

                if telefono and telefono.startswith("9"):
                    print(f"✔ Guardando: {nombre} - {telefono} - {direccion}")
                    datos_locales.append({
                        "Negocio": nombre,
                        "Dirección": direccion,
                        "Teléfono": telefono,
                        "Tipo": tipo
                    })

            next_page_token = results.get("next_page_token")
            if not next_page_token:
                break

        except Exception as e:
            print(f"❌ Error con {tipo}: {e}")
            break

    return datos_locales

import signal
import sys

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == "__main__":
    with open("tipos_negocios.txt", "r", encoding="utf-8") as f:
        tipos = [line.strip() for line in f if line.strip()]

    print(f"🧠 Iniciando procesamiento con {min(4, cpu_count())} procesos... (Ctrl+C para detener)")

    pool = Pool(processes=min(4, cpu_count()), initializer=init_worker)

    try:
        async_result = pool.map_async(procesar_tipo, tipos)
        resultados = async_result.get(timeout=None)
    except KeyboardInterrupt:
        print("\n🛑 Interrupción detectada. Cerrando procesos...")
        pool.terminate()
        pool.join()
        sys.exit(1)
    else:
        pool.close()
        pool.join()

    datos = [item for sublist in resultados for item in sublist]

    if datos:
        df = pd.DataFrame(datos)
        print(f"Total de negocios con teléfono que comiencen por 9 encontrados: {len(datos)}")
        df.to_excel("negocios_conchali.xlsx", index=False)
        print("✅ Archivo generado: negocios_conchali.xlsx")
    else:
        print("⚠️ No se encontraron negocios con teléfono 9.")
