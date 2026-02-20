# ML Scraper – Pipeline Web scraping → PostgreSQL → SQL

Pipeline completo de extracción, almacenamiento y análisis de productos de **MercadoLibre Argentina** en tres categorías: Laptops, Celulares y Televisores.

## Estructura del proyecto

```
ml_scraper/
├── main.py                  # Orquestador: scraping → DB → análisis
├── scrapy.cfg
├── requirements.txt
├── .env.example             # Plantilla de variables de entorno
├── productos.csv            # Generado al correr el scraper (ignorado por git)
│
├── scraper/                 # Scrapy project
│   ├── settings.py
│   ├── items.py
│   ├── pipelines.py
│   └── spiders/
│       ├── base_spider.py   # Lógica común + paginación
│       ├── laptops_spider.py
│       ├── celulares_spider.py
│       └── televisores_spider.py
│
├── database/
│   ├── connection.py        # get_connection() usando variables de entorno
│   ├── schema.py            # Crea DB y tabla productos
│   └── loader.py            # Carga el CSV → PostgreSQL
│
└── analysis/
    └── queries.py           # 9 consultas SQL analíticas
```

## Requisitos

- Python 3.10+
- PostgreSQL corriendo en Docker (u otra instancia local)
- Las dependencias de `requirements.txt`

## Setup

```bash
# 1. Activar el entorno virtual
.\venv\Scripts\Activate.ps1        # PowerShell (Windows)
# source venv/bin/activate          # bash/macOS/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de PostgreSQL
```

**Ejemplo de `.env`:**
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ml_scraper
DB_USER=postgres
DB_PASSWORD=tu_password
```

Si usás Docker:
```bash
docker run --name pg-ml -e POSTGRES_PASSWORD=tu_password -p 5432:5432 -d postgres
```

## Uso

```bash
# Pipeline completo: scraping + carga + análisis
python main.py

# Saltear el scraping (ya tenés productos.csv)
python main.py --skip-scrape

# Solo correr el análisis SQL (la DB ya tiene datos)
python main.py --only-analysis
```

También podés correr los spiders de Scrapy individualmente:
```bash
scrapy crawl laptops
scrapy crawl celulares
scrapy crawl televisores
```

## Tabla `productos`

| Campo             | Tipo          | Descripción                        |
|-------------------|---------------|------------------------------------|
| id                | SERIAL PK     | Clave primaria auto-incremental    |
| nombre            | TEXT          | Título del producto                |
| precio_actual     | NUMERIC(15,2) | Precio de venta actual             |
| precio_anterior   | NUMERIC(15,2) | Precio antes del descuento         |
| descuento         | INTEGER       | % de descuento (ej: 23)            |
| ubicacion         | VARCHAR(200)  | Ciudad/provincia del vendedor      |
| cuotas            | VARCHAR(200)  | Texto con info de cuotas           |
| envio_gratis      | BOOLEAN       | True si el envío es gratuito       |
| enlace            | TEXT          | URL del producto                   |
| categoria         | VARCHAR(100)  | laptops / celulares / televisores  |
| fecha_extraccion  | TIMESTAMP     | Fecha y hora del scraping (UTC)    |

## Consultas SQL incluidas

1. Precio promedio por categoría
2. Producto más costoso en cada categoría
3. Cantidad de productos con envío gratis
4. Ubicaciones con mayor número de publicaciones
5. Descuento promedio por categoría
6. Productos por encima del precio promedio general
7. Los 5 más económicos en cada categoría
8. Ahorro promedio cuando existe precio anterior
9. Distribución por rango de precio (bajo / medio / alto)

## Buenas prácticas aplicadas

- **`ROBOTSTXT_OBEY = True`**: Se respeta el `robots.txt` del sitio.
- **AutoThrottle** (2–8 seg): Una petición por vez para no saturar el servidor.
- **Sin credenciales en el código**: Todo via `.env` con `python-dotenv`.
- **User-Agent realista**: El bot se identifica como un browser normal y no como un bot de IA (los cuales están en el Disallow del robots.txt de MercadoLibre).
