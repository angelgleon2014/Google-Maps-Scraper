# Scraper de Google Maps 🗺️

business data extraction with custom filters / extracción de negocios con filtros personalizados

Script de scraping automatizado para extraer información de negocios desde Google Maps usando criterios por ubicación y tipo de negocio.

## 🔧 Funcionalidades
- Búsqueda por comuna y categoría de negocio
- Extracción de:
  - Nombre
  - Dirección
  - Teléfono (solo si comienza con 9)
  - Coordenadas
- Guarda resultados en CSV o Excel
- Filtros para evitar duplicados y negocios sin sitio web

## 🧠 Tecnologías
- Python
- Selenium / Playwright
- Pandas
- API de Google Maps (opcional)

## 📂 Estructura


## 🚀 Uso
bash
python maps_scraper.py

## Ejemplo de salida
Nombre, Dirección, Teléfono, Latitud, Longitud
Panadería Don Juan, Av. Matta 1234, 922334455, -33.45, -70.66

## Caso de uso
Lead generation para marketing local
Creación automática de páginas web para negocios sin sitio
