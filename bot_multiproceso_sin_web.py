import googlemaps
import time
import pandas as pd
import signal
import sys
from multiprocessing import Pool, cpu_count

API_KEY = ""
gmaps = googlemaps.Client(key=API_KEY)

CIUDAD = "Independencia, Santiago de Chile"

# Ignorar Ctrl+C en los workers
def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

# Procesa un solo tipo de negocio
def procesar_tipo(tipo):
    print(f"🔍 Buscando: {tipo}")
    datos_locales = []
    query = f"{tipo} en {CIUDAD}"
    next_page_token = None

    while True:
        try:
            if next_page_token:
                time.sleep(2)  # Delay necesario por token
                results = gmaps.places(query=query, page_token=next_page_token)
            else:
                results = gmaps.places(query=query)

            for lugar in results.get("results", []):
                nombre = lugar.get("name")
                direccion = lugar.get("formatted_address")
                place_id = lugar.get("place_id")

                # Detalles: teléfono y sitio web
                detalles = gmaps.place(place_id=place_id, fields=["formatted_phone_number", "website"])
                telefono = detalles.get("result", {}).get("formatted_phone_number", "")
                sitio_web = detalles.get("result", {}).get("website", None)

                if telefono and telefono.startswith("9") and not sitio_web:
                    print(f"✔ Sin web: {nombre} - {telefono}")
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

if __name__ == "__main__":
    # Leer lista de tipos de negocios
    with open("tipos_negocios.txt", "r", encoding="utf-8") as f:
        tipos = [line.strip() for line in f if line.strip()]

    print(f"🧠 Procesando {len(tipos)} tipos de negocios con hasta {min(4, cpu_count())} procesos (Ctrl+C para detener)...")

    pool = Pool(processes=min(4, cpu_count()), initializer=init_worker)

    try:
        async_result = pool.map_async(procesar_tipo, tipos)
        resultados = async_result.get(timeout=None)
    except KeyboardInterrupt:
        print("\n🛑 Interrupción detectada. Terminando procesos...")
        pool.terminate()
        pool.join()
        sys.exit(1)
    else:
        pool.close()
        pool.join()

    # Unir resultados
    datos = [item for sublist in resultados for item in sublist]

    if datos:
        df = pd.DataFrame(datos)
        df.to_excel("negocios_sin_web.xlsx", index=False)
        print("✅ Archivo generado: negocios_sin_web.xlsx")
    else:
        print("⚠️ No se encontraron negocios sin sitio web con teléfono 9.")
